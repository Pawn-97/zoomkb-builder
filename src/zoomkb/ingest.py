"""Ingest raw markdown articles into structured wiki pages."""

import json
import logging
import os
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


_INGEST_PROMPT = """You are a knowledge extraction engine. Analyze the following Zoom Support article and extract structured entities for a design-facing wiki.

Product: {product}
Article ID: {article_id}
Title: {title}

Article content:
{content}

Extract the following entity types. For each entity, provide a concise, design-facing summary focused on UX implications, not implementation details.

Entity types:
- concept: Product concepts, features, or objects designers need to understand
- user-role: Roles, permissions, and visibility scopes
- task-flow: Tasks users complete, with steps and dependencies
- constraint: Design constraints, limitations, or rules
- ux-pattern: Reusable interaction patterns or design decisions

Respond with JSON only:
{{
  "concepts": [
    {{
      "title": "Human-readable title",
      "summary": "2-3 sentences for designers",
      "key_points": ["bullet 1", "bullet 2"],
      "related": ["slug-of-related-entity"]
    }}
  ],
  "user_roles": [...],
  "task_flows": [...],
  "constraints": [...],
  "ux_patterns": [...]
}}

Rules:
- Only extract entities actually mentioned in the article. Do not hallucinate.
- Keep summaries brief and focused on UX/design implications.
- Use kebab-case for related slugs (derived from title).
- If an entity type has no matches, return an empty array.
"""


def _slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:80]


def _extract_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter from markdown. Returns (frontmatter dict, body)."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        import yaml
        fm = yaml.safe_load(parts[1].strip())
        return fm if isinstance(fm, dict) else {}, parts[2].strip()
    except Exception:
        return {}, content


def _extract_frontmatter_manual(content: str) -> tuple[dict[str, Any], str]:
    """Parse simple key:value frontmatter without yaml dependency."""
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


def _call_llm(prompt: str) -> dict[str, Any]:
    """Call OpenAI API for entity extraction."""
    try:
        import openai

        client = openai.OpenAI()
        resp = client.chat.completions.create(
            model=os.getenv("ZOOMKB_LLM_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0,
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        raise RuntimeError(f"LLM call failed: {e}") from e


def extract_entities(raw_path: Path, product: str) -> IngestResult:
    """Extract wiki entities from a single raw markdown article."""
    content = raw_path.read_text(encoding="utf-8")
    fm, body = _extract_frontmatter_manual(content)

    article_id = fm.get("article_id", raw_path.stem.split("-")[0])
    title = fm.get("title", raw_path.stem)
    source_url = fm.get("source_url", "")

    prompt = _INGEST_PROMPT.format(
        product=product,
        article_id=article_id,
        title=title,
        content=body[:8000],  # Truncate to stay within context limits
    )

    data = _call_llm(prompt)

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


def _write_wiki_page(entity: WikiEntity, wiki_dir: Path) -> Path:
    """Write or merge a wiki page for an entity."""
    subdir = wiki_dir / entity.type.replace("-", "-")  # concepts, user-roles, etc.
    subdir.mkdir(parents=True, exist_ok=True)
    path = subdir / f"{entity.slug}.md"

    # Merge if page already exists
    existing_entities: list[WikiEntity] = []
    if path.exists():
        existing = _read_wiki_page(path)
        if existing:
            existing_entities.append(existing)

    # Simple merge: append new source, keep longer summary
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
    return path


def _read_wiki_page(path: Path) -> Optional[WikiEntity]:
    """Read a wiki page back into an entity (basic parse)."""
    content = path.read_text(encoding="utf-8")
    fm, body = _extract_frontmatter_manual(content)

    etype = fm.get("type", "concept")
    title = fm.get("title", path.stem)

    # Parse sources from frontmatter text
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

    # Extract summary
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

    # Extract key points
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

    # Extract related
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


def ingest_articles(
    manifest_path: Path,
    raw_dir: Path,
    wiki_dir: Path,
    product: str = "zoom-phone",
    force: bool = False,
    dry_run: bool = False,
    article_ids: Optional[List[str]] = None,
) -> dict[str, Any]:
    """Ingest raw articles into wiki. Returns stats dict."""
    from zoomkb.manifest import load_manifest, save_manifest

    manifest = load_manifest(manifest_path)
    articles = manifest.get("articles", [])

    # Filter to accepted articles
    candidates = [
        a for a in articles
        if a.get("status") == "accepted" and a.get("confidence") == "high"
    ]

    if article_ids:
        candidates = [a for a in candidates if a["article_id"] in article_ids]

    # Skip already ingested unless force
    if not force:
        candidates = [
            a for a in candidates
            if "ingested_at" not in a or a.get("content_hash") != a.get("last_ingested_hash")
        ]

    if dry_run:
        return {
            "dry_run": True,
            "candidates": [a["article_id"] for a in candidates],
            "processed": 0,
            "entities_created": 0,
            "entities_updated": 0,
            "errors": 0,
            "skipped": 0,
        }

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

    for article in candidates:
        raw_path = raw_dir.parent.parent / article.get("local_path", f"raw/support-articles/{article['filename']}")
        if not raw_path.exists():
            logger.warning("Raw file not found: %s", raw_path)
            stats["skipped"] += 1
            continue

        try:
            result = extract_entities(raw_path, product)

            for entity in result.entities:
                path = _write_wiki_page(entity, wiki_dir)
                if path in entity_paths:
                    stats["entities_updated"] += 1
                else:
                    stats["entities_created"] += 1
                    entity_paths.add(path)

            # Mark as ingested
            article["ingested_at"] = datetime.now(timezone.utc).isoformat()
            article["last_ingested_hash"] = article.get("content_hash", "")
            stats["processed"] += 1
            processed_articles.append(article["article_id"])

        except Exception as e:
            logger.error("Ingest failed for %s: %s", article["article_id"], e)
            stats["errors"] += 1
            error_articles.append((article["article_id"], str(e)))

    save_manifest(manifest_path, manifest)

    # Generate index.md
    _generate_index(wiki_dir, product)

    # Generate ingest-report.md
    _write_ingest_report(manifest_path.parent, stats, processed_articles, error_articles)

    return stats


def _write_ingest_report(
    output_dir: Path,
    stats: dict[str, Any],
    processed: list[str],
    errors: list[tuple[str, str]],
) -> None:
    """Write ingest-report.md."""
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
    """Generate wiki/index.md from all wiki pages."""
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
