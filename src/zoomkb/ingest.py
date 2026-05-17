"""Ingest raw markdown articles into structured wiki pages.

Pipeline:
  1. prepare  — writes extraction prompt files to extraction-queue/
  2. extract  — Claude Code processes prompts → writes .result.json files
  3. commit   — reads results, writes wiki pages, updates manifest
"""

import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List, Optional

logger = logging.getLogger("zoomkb.ingest")


@dataclass
class WikiEntity:
    type: str  # concept | user-role | task-flow | constraint | ux-pattern
    title: str
    slug: str
    summary: str
    key_points: list[str] = field(default_factory=list)
    related: list[str] = field(default_factory=list)
    sources: list[dict[str, str]] = field(default_factory=list)


@dataclass
class IngestResult:
    article_id: str
    entities: list[WikiEntity]
    error: Optional[str] = None


_EXTRACTION_SYSTEM = """You are a knowledge extraction engine for Zoom product support articles.
Analyze the article and extract structured entities for a design-facing wiki.

Entity types:
- concept: Product concepts, features, or objects designers need to understand
- user-role: Roles, permissions, and visibility scopes
- task-flow: Tasks users complete, with steps and dependencies
- constraint: Design constraints, limitations, or rules
- ux-pattern: Reusable interaction patterns or design decisions

For each entity provide:
- title: Human-readable title
- summary: 2-3 sentences for designers, focused on UX implications
- key_points: list of 2-5 bullet points
- related: list of related entity slugs in kebab-case (may be empty)

Rules:
- Only extract entities actually mentioned in the article
- Keep summaries focused on UX/design implications, not implementation
- Use kebab-case for related slugs
- Empty array if no matches for an entity type"""


def _slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:80]


def _extract_frontmatter_manual(content: str) -> tuple[dict[str, Any], str]:
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    fm: dict[str, Any] = {}
    for line in parts[1].strip().split("\n"):
        if ":" in line and not line.startswith(" "):
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip()
    return fm, parts[2].strip()


def _resolve_raw_path(article: dict, raw_dir: Path) -> Optional[Path]:
    """Resolve article's raw markdown file path."""
    local = article.get("local_path", "")
    if local:
        # local_path is relative to output dir, e.g. raw/support-articles/KB...md
        raw_path = raw_dir.parent.parent / local
        if raw_path.exists():
            return raw_path
    # Fallback: search by article_id in raw dir
    aid = article["article_id"]
    for f in raw_dir.glob(f"{aid}*.md"):
        return f
    return None


# ── Prepare: write extraction prompts ──────────────────────────────

def prepare_extraction_queue(
    manifest_path: Path,
    raw_dir: Path,
    force: bool = False,
    article_ids: Optional[List[str]] = None,
) -> dict:
    """Write extraction prompt files for pending articles.

    Creates: <output>/extraction-queue/<article_id>.prompt.md
    Returns stats dict.
    """
    from zoomkb.manifest import load_manifest

    manifest = load_manifest(manifest_path)
    articles = manifest.get("articles", [])

    # Filter: high-confidence accepted only
    candidates = [
        a for a in articles
        if a.get("status") == "accepted" and a.get("confidence") == "high"
    ]
    if article_ids:
        candidates = [a for a in candidates if a["article_id"] in article_ids]

    # Skip already ingested unless force
    skipped_ingested = 0
    if not force:
        pending = []
        for a in candidates:
            if "ingested_at" in a and a.get("content_hash") == a.get("last_ingested_hash"):
                skipped_ingested += 1
            else:
                pending.append(a)
        candidates = pending

    output_dir = manifest_path.parent
    queue_dir = output_dir / "extraction-queue"
    queue_dir.mkdir(parents=True, exist_ok=True)

    prepared = 0
    skipped_missing = 0

    for article in candidates:
        raw_path = _resolve_raw_path(article, raw_dir)
        if not raw_path:
            logger.warning("Raw file not found for %s", article["article_id"])
            skipped_missing += 1
            continue

        content = raw_path.read_text(encoding="utf-8")
        fm, body = _extract_frontmatter_manual(content)
        title = fm.get("title", article.get("title", article["article_id"]))
        source_url = fm.get("source_url", article.get("source_url", ""))

        # Truncate body to ~6000 chars for context efficiency
        body_truncated = body[:6000]

        prompt_file = queue_dir / f"{article['article_id']}.prompt.md"
        prompt_content = f"""# Extraction Task: {article['article_id']}

**Product**: zoom-phone
**Article ID**: {article['article_id']}
**Title**: {title}
**Source URL**: {source_url}

## Instructions

{_EXTRACTION_SYSTEM}

## Article Content

{body_truncated}

---

Output your extraction as valid JSON matching this schema:

```json
{{
  "article_id": "{article['article_id']}",
  "concepts": [
    {{"title": "...", "summary": "...", "key_points": ["..."], "related": ["..."]}}
  ],
  "user_roles": [...],
  "task_flows": [...],
  "constraints": [...],
  "ux_patterns": [...]
}}
```
"""
        prompt_file.write_text(prompt_content, encoding="utf-8")
        prepared += 1

    # Write queue manifest
    queue_manifest = {
        "total": prepared,
        "skipped_ingested": skipped_ingested,
        "skipped_missing": skipped_missing,
        "article_ids": [a["article_id"] for a in candidates if _resolve_raw_path(a, raw_dir)],
    }
    (queue_dir / "queue-manifest.json").write_text(
        json.dumps(queue_manifest, indent=2), encoding="utf-8"
    )

    logger.info(
        "Prepared %d extraction prompts (skipped: %d ingested, %d missing)",
        prepared, skipped_ingested, skipped_missing,
    )

    return queue_manifest


# ── Parse: read Claude extraction result ────────────────────────────

def parse_extraction_result(
    result_path: Path,
    article_id: str,
    title: str = "",
    source_url: str = "",
) -> IngestResult:
    """Parse a .result.json file into WikiEntities."""
    data = json.loads(result_path.read_text(encoding="utf-8"))

    entities: list[WikiEntity] = []
    source = {"article_id": article_id, "title": title, "source_url": source_url}

    type_map = {
        "concepts": "concept",
        "user_roles": "user-role",
        "task_flows": "task-flow",
        "constraints": "constraint",
        "ux_patterns": "ux-pattern",
    }

    for key, etype in type_map.items():
        for item in data.get(key, []):
            if not item.get("title"):
                continue
            entities.append(
                WikiEntity(
                    type=etype,
                    title=item["title"],
                    slug=_slugify(item["title"]),
                    summary=item.get("summary", ""),
                    key_points=item.get("key_points", []),
                    related=[_slugify(r) for r in item.get("related", []) if r],
                    sources=[source],
                )
            )

    return IngestResult(article_id=article_id, entities=entities)


# ── Commit: write wiki pages from results ──────────────────────────

def _write_wiki_page(entity: WikiEntity, wiki_dir: Path) -> tuple[Path, bool]:
    """Write or merge a wiki page. Returns (path, is_new)."""
    type_dir_map = {
        "concept": "concepts",
        "user-role": "user-roles",
        "task-flow": "task-flows",
        "constraint": "constraints",
        "ux-pattern": "ux-patterns",
    }
    subdir = wiki_dir / type_dir_map.get(entity.type, entity.type + "s")
    subdir.mkdir(parents=True, exist_ok=True)
    path = subdir / f"{entity.slug}.md"

    is_new = not path.exists()

    existing_entities: list[WikiEntity] = []
    if path.exists():
        existing = _read_wiki_page(path)
        if existing:
            existing_entities.append(existing)

    # Merge: append new sources, keep longer summary
    merged_sources = entity.sources.copy()
    merged_summary = entity.summary
    merged_points = list(entity.key_points)

    for e in existing_entities:
        for s in e.sources:
            if s["article_id"] not in {x["article_id"] for x in merged_sources}:
                merged_sources.append(s)
        if len(e.summary) > len(merged_summary):
            merged_summary = e.summary
        for p in e.key_points:
            if p not in merged_points:
                merged_points.append(p)

    related = sorted(set(entity.related + [r for e in existing_entities for r in e.related]))

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    sources_yaml = "\n".join(
        f"  - article_id: {s['article_id']}\n    title: {s['title']}\n    source_url: {s.get('source_url', '')}"
        for s in merged_sources
    )

    related_links = "\n".join(f"- [[{r}]]" for r in related) if related else "_None yet_"
    key_points_md = "\n".join(f"- {p}" for p in merged_points) if merged_points else "_None yet_"

    page = f"""---
type: {entity.type}
product: zoom-phone
title: {entity.title}
sources:
{sources_yaml}
confidence: high
last_reviewed: {today}
---

# {entity.title}

## Summary

{merged_summary}

## Key points

{key_points_md}

## Related

{related_links}
"""

    path.write_text(page, encoding="utf-8")
    return path, is_new


def _read_wiki_page(path: Path) -> Optional[WikiEntity]:
    """Read a wiki page back into an entity (basic parse)."""
    content = path.read_text(encoding="utf-8")
    fm, body = _extract_frontmatter_manual(content)

    etype = fm.get("type", "concept")
    title = fm.get("title", path.stem)

    sources: list[dict[str, str]] = []
    in_sources = False
    current: dict[str, str] = {}
    for line in content.split("\n")[:30]:
        if line.strip() == "sources:":
            in_sources = True
            continue
        if in_sources:
            if line.strip().startswith("- article_id:"):
                if current:
                    sources.append(current)
                current = {"article_id": line.split(":", 1)[1].strip()}
            elif line.strip().startswith("title:") and current:
                current["title"] = line.split(":", 1)[1].strip()
            elif line.strip().startswith("source_url:") and current:
                current["source_url"] = line.split(":", 1)[1].strip()
            elif line.strip().startswith("type:") or line.strip().startswith("product:"):
                continue
            elif line.strip() == "---" and in_sources:
                if current:
                    sources.append(current)
                break

    summary = ""
    lines = body.split("\n")
    in_summary = False
    for line in lines:
        if line.strip() == "## Summary":
            in_summary = True
            continue
        if in_summary:
            if line.strip().startswith("##"):
                break
            summary += line + " "

    key_points: list[str] = []
    in_points = False
    for line in lines:
        if line.strip() == "## Key points":
            in_points = True
            continue
        if in_points:
            if line.strip().startswith("##"):
                break
            if line.strip().startswith("- "):
                key_points.append(line[2:].strip())

    related: list[str] = []
    in_related = False
    for line in lines:
        if line.strip() == "## Related":
            in_related = True
            continue
        if in_related:
            if line.strip().startswith("##"):
                break
            m = re.match(r"- \[\[(.+?)\]\]", line.strip())
            if m:
                related.append(m.group(1))

    return WikiEntity(
        type=etype,
        title=title,
        slug=path.stem,
        summary=summary.strip(),
        key_points=key_points,
        related=related,
        sources=sources,
    )


def commit_extraction(
    manifest_path: Path,
    raw_dir: Path,
    wiki_dir: Path,
    product: str = "zoom-phone",
) -> dict:
    """Read extraction results and write wiki pages.

    Expects <output>/extraction-queue/<article_id>.result.json files.
    Updates manifest with ingested_at timestamps.
    """
    from zoomkb.manifest import load_manifest, save_manifest

    output_dir = manifest_path.parent
    queue_dir = output_dir / "extraction-queue"

    if not queue_dir.exists():
        logger.error("extraction-queue/ not found. Run 'zoomkb ingest --prepare' first.")
        return {"processed": 0, "entities_created": 0, "entities_updated": 0, "errors": 1, "skipped": 0}

    manifest = load_manifest(manifest_path)

    # Read queue manifest to know what was prepared
    qm_path = queue_dir / "queue-manifest.json"
    if qm_path.exists():
        queue_manifest = json.loads(qm_path.read_text(encoding="utf-8"))
        pending_ids = set(queue_manifest.get("article_ids", []))
    else:
        pending_ids = set()

    stats = {
        "processed": 0,
        "entities_created": 0,
        "entities_updated": 0,
        "errors": 0,
        "skipped": 0,
    }

    entity_paths: set[Path] = set()
    processed_articles: list[str] = []
    error_articles: list[tuple[str, str]] = []

    # Build lookup for article metadata
    article_lookup: dict[str, dict] = {}
    for a in manifest.get("articles", []):
        article_lookup[a["article_id"]] = a

    for result_file in sorted(queue_dir.glob("*.result.json")):
        article_id = result_file.stem.replace(".result", "")

        if pending_ids and article_id not in pending_ids:
            continue

        article = article_lookup.get(article_id, {})
        raw_path = None
        title = article.get("title", article_id)
        source_url = article.get("source_url", "")

        # Try to read title/source_url from raw file
        raw_candidates = list(raw_dir.glob(f"{article_id}*.md"))
        if raw_candidates:
            raw_path = raw_candidates[0]
            fm, _ = _extract_frontmatter_manual(raw_path.read_text(encoding="utf-8"))
            title = fm.get("title", title)
            source_url = fm.get("source_url", source_url)

        try:
            result = parse_extraction_result(result_file, article_id, title, source_url)

            for entity in result.entities:
                path, is_new = _write_wiki_page(entity, wiki_dir)
                if is_new:
                    stats["entities_created"] += 1
                    entity_paths.add(path)
                else:
                    stats["entities_updated"] += 1

            # Mark as ingested in manifest
            if article_id in article_lookup:
                article_lookup[article_id]["ingested_at"] = datetime.now(timezone.utc).isoformat()
                article_lookup[article_id]["last_ingested_hash"] = article_lookup[article_id].get("content_hash", "")

            stats["processed"] += 1
            processed_articles.append(article_id)

        except Exception as e:
            logger.error("Commit failed for %s: %s", article_id, e)
            stats["errors"] += 1
            error_articles.append((article_id, str(e)))

    # Count unprocessed as skipped
    if pending_ids:
        processed_set = set(processed_articles)
        stats["skipped"] = len(pending_ids - processed_set)

    manifest["articles"] = list(article_lookup.values())
    save_manifest(manifest_path, manifest)

    # Generate index.md
    _generate_index(wiki_dir, product)

    # Generate ingest-report.md
    _write_ingest_report(output_dir, stats, processed_articles, error_articles)

    return stats


# ── Dry run ────────────────────────────────────────────────────────

def dry_run_ingest(
    manifest_path: Path,
    raw_dir: Path,
    force: bool = False,
    article_ids: Optional[List[str]] = None,
) -> dict:
    """Preview what would be processed."""
    from zoomkb.manifest import load_manifest

    manifest = load_manifest(manifest_path)
    articles = manifest.get("articles", [])

    candidates = [
        a for a in articles
        if a.get("status") == "accepted" and a.get("confidence") == "high"
    ]
    if article_ids:
        candidates = [a for a in candidates if a["article_id"] in article_ids]

    if not force:
        candidates = [
            a for a in candidates
            if "ingested_at" not in a or a.get("content_hash") != a.get("last_ingested_hash")
        ]

    missing = sum(1 for a in candidates if not _resolve_raw_path(a, raw_dir))

    return {
        "dry_run": True,
        "candidates": [a["article_id"] for a in candidates],
        "total": len(candidates),
        "missing_raw_files": missing,
    }


# ── Report & Index generation ──────────────────────────────────────

def _write_ingest_report(
    output_dir: Path,
    stats: dict[str, Any],
    processed: list[str],
    errors: list[tuple[str, str]],
) -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "# Ingest Report",
        "",
        f"_Generated: {today}_",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Articles processed | {stats['processed']} |",
        f"| Entities created | {stats['entities_created']} |",
        f"| Entities updated | {stats['entities_updated']} |",
        f"| Errors | {stats['errors']} |",
        f"| Skipped | {stats['skipped']} |",
        "",
    ]

    if processed:
        lines.extend(["## Processed Articles", ""])
        for aid in processed:
            lines.append(f"- {aid}")
        lines.append("")

    if errors:
        lines.extend(["## Errors", ""])
        for aid, err in errors:
            lines.append(f"- **{aid}**: {err}")
        lines.append("")

    (output_dir / "ingest-report.md").write_text("\n".join(lines), encoding="utf-8")
    logger.info("Generated ingest-report.md")


def _generate_index(wiki_dir: Path, product: str) -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    sections: dict[str, list[tuple[str, str]]] = {
        "concept": [],
        "user-role": [],
        "task-flow": [],
        "constraint": [],
        "ux-pattern": [],
    }

    for subdir_name, label in [
        ("concepts", "concept"),
        ("user-roles", "user-role"),
        ("task-flows", "task-flow"),
        ("constraints", "constraint"),
        ("ux-patterns", "ux-pattern"),
    ]:
        subdir = wiki_dir / subdir_name
        if not subdir.exists():
            continue
        for path in sorted(subdir.glob("*.md")):
            title = path.stem.replace("-", " ").title()
            sections[label].append((path.stem, title))

    lines = [
        f"# {product.replace('-', ' ').title()} Knowledge Base",
        "",
        f"_Last updated: {today}_",
        "",
        "## Concepts",
        "",
    ]
    for slug, title in sections["concept"]:
        lines.append(f"- [[{slug}]] — {title}")

    lines.extend(["", "## User Roles", ""])
    for slug, title in sections["user-role"]:
        lines.append(f"- [[{slug}]] — {title}")

    lines.extend(["", "## Task Flows", ""])
    for slug, title in sections["task-flow"]:
        lines.append(f"- [[{slug}]] — {title}")

    lines.extend(["", "## Constraints", ""])
    for slug, title in sections["constraint"]:
        lines.append(f"- [[{slug}]] — {title}")

    lines.extend(["", "## UX Patterns", ""])
    for slug, title in sections["ux-pattern"]:
        lines.append(f"- [[{slug}]] — {title}")

    lines.append("")

    (wiki_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")
    logger.info("Generated wiki/index.md")
