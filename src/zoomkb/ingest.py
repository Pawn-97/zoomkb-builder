"""Ingest raw markdown articles into structured wiki pages.

Pipeline:
  1. prepare  — writes extraction prompt files to extraction-queue/
  2. extract  — Claude Code processes prompts → writes .result.json files
  3. commit   — reads results, deduplicates entities, filters by min_sources, writes wiki pages
"""

import json
import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

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


def _score_entity(entity: "WikiEntity", avg_article_score: float = 8.0) -> float:
    """Score entity quality 0-100. Higher = more substantial, better sourced."""
    source_score = min(len(entity.sources) * 8.0, 40.0)
    summary_score = min(len(entity.summary) / 7.5, 30.0)
    kp_score = min(len(entity.key_points) * 10.0, 20.0)
    article_score = min(avg_article_score, 10.0)
    return source_score + summary_score + kp_score + article_score


def _title_similarity(title_a: str, title_b: str) -> float:
    """Token Jaccard similarity between two titles. 0.0 = no overlap, 1.0 = identical."""
    words_a = set(re.findall(r"[a-z0-9]+", title_a.lower()))
    words_b = set(re.findall(r"[a-z0-9]+", title_b.lower()))
    if not words_a or not words_b:
        return 0.0
    return len(words_a & words_b) / len(words_a | words_b)


def _normalize_slug(slug: str) -> str:
    """Normalize slug for fuzzy dedup: strip trailing 's', common suffixes."""
    s = slug.rstrip("s").strip("-") if not slug.endswith("ss") else slug
    for suffix in ("-admin", "-user", "-setting", "-settings", "-option", "-options"):
        if s.endswith(suffix):
            s = s[:-len(suffix)]
            break
    return s.strip("-") or slug


def _merge_entities(canonical: "WikiEntity", other: "WikiEntity") -> None:
    """Merge other into canonical (mutates canonical)."""
    seen_aids = {s["article_id"] for s in canonical.sources}
    for s in other.sources:
        if s["article_id"] not in seen_aids:
            canonical.sources.append(s)
            seen_aids.add(s["article_id"])
    for p in other.key_points:
        if p not in canonical.key_points:
            canonical.key_points.append(p)
    if len(other.summary) > len(canonical.summary):
        canonical.summary = other.summary
    for r in other.related:
        if r not in canonical.related:
            canonical.related.append(r)
    canonical.related.sort()


def _dedup_entities(entities: list["WikiEntity"]) -> list["WikiEntity"]:
    """Merge near-duplicate entities by normalized slug + title similarity.

    Phase A: exact slug match → merge into one entity.
    Phase B: normalized slug match → merge, keep shortest slug as canonical.
    """
    if not entities:
        return []

    # Phase A: group by exact slug
    slug_groups: dict[str, list[WikiEntity]] = {}
    for e in entities:
        slug_groups.setdefault(e.slug, []).append(e)

    merged: list[WikiEntity] = []
    for slug, group in slug_groups.items():
        if len(group) == 1:
            merged.append(group[0])
        else:
            keeper = group[0]
            for e in group[1:]:
                _merge_entities(keeper, e)
            merged.append(keeper)

    # Phase B: group by normalized slug
    norm_groups: dict[str, list[WikiEntity]] = {}
    for e in merged:
        nk = _normalize_slug(e.slug)
        norm_groups.setdefault(nk, []).append(e)

    after_b: list[WikiEntity] = []
    for _, group in norm_groups.items():
        if len(group) == 1:
            after_b.append(group[0])
        else:
            # Pick canonical: shortest slug (fewest dashes), then most sources
            canonical = min(group, key=lambda e: (e.slug.count("-"), -len(e.sources)))
            for e in group:
                if e is not canonical:
                    _merge_entities(canonical, e)
            after_b.append(canonical)

    # Phase C: merge by title token Jaccard similarity (union-find)
    SIMILARITY_THRESHOLD = 0.75
    n_after_b = len(after_b)
    parent = list(range(n_after_b))

    def _find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def _union(x: int, y: int) -> None:
        px, py = _find(x), _find(y)
        if px != py:
            parent[py] = px

    semantic_merged = 0
    for i in range(n_after_b):
        for j in range(i + 1, n_after_b):
            if _find(i) == _find(j):
                continue
            if _title_similarity(after_b[i].title, after_b[j].title) >= SIMILARITY_THRESHOLD:
                _union(i, j)
                semantic_merged += 1

    # Group by root
    groups: dict[int, list[WikiEntity]] = defaultdict(list)
    for i, e in enumerate(after_b):
        groups[_find(i)].append(e)

    result: list[WikiEntity] = []
    for group in groups.values():
        if len(group) == 1:
            result.append(group[0])
        else:
            canonical = max(group, key=lambda e: _score_entity(e))
            for e in group:
                if e is not canonical:
                    _merge_entities(canonical, e)
            result.append(canonical)

    logger.info(
        "Dedup: %d entities → %d (exact=%d, norm=%d, semantic=%d)",
        len(entities), len(result), len(slug_groups), len(norm_groups), semantic_merged,
    )
    return result


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
    product: str = "",
    force: bool = False,
    article_ids: Optional[List[str]] = None,
) -> dict:
    """Write extraction prompt files for pending articles.

    Creates: <output>/extraction-queue/<article_id>.prompt.md
    Returns stats dict.
    """
    from zoomkb.manifest import load_manifest

    manifest = load_manifest(manifest_path)
    if not product:
        product = manifest.get("product", "zoom-phone")
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

**Product**: {product}
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

def _write_wiki_page(
    entity: WikiEntity, wiki_dir: Path, product: str = "zoom-phone",
    valid_slugs: Optional[set[str]] = None,
) -> tuple[Path, bool, bool]:
    """Write or merge a wiki page. Returns (path, is_new, conflict_flagged).

    If valid_slugs provided, wikilinks to non-existent pages are pruned.
    """
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

    # Prune wikilinks that don't resolve to existing entities
    if valid_slugs is not None:
        related = sorted(r for r in related if r in valid_slugs or r == entity.slug)

    related_links = "\n".join(f"- [[{r}]]" for r in related) if related else "_None yet_"
    key_points_md = "\n".join(f"- {p}" for p in merged_points) if merged_points else "_None yet_"

    # Flag entities with ≥3 different source articles for review
    conflict_flag = ""
    unique_source_aids = {s.get("article_id", "") for s in merged_sources if s.get("article_id")}
    if len(unique_source_aids) >= 3:
        conflict_flag = "multiple-sources"

    page = f"""---
type: {entity.type}
product: {product}
title: {entity.title}
sources:
{sources_yaml}
confidence: high
last_reviewed: {today}
""" + (f"conflict_flag: {conflict_flag}\n" if conflict_flag else "") + """---

# {entity.title}

## Summary

{merged_summary}

## Key points

{key_points_md}

## Related

{related_links}
"""

    path.write_text(page, encoding="utf-8")
    return path, is_new, bool(conflict_flag)


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
    min_sources: int = 1,
    min_quality: float = 20.0,
) -> dict:
    """Read extraction results, deduplicate, filter by min_sources + quality, write wiki pages.

    Three-phase dedup (slug exact → slug normalized → title similarity).
    After dedup, entities are scored 0-100 and filtered below min_quality.
    Wikilinks to non-existent pages are pruned before writing.

    Expects <output>/extraction-queue/<article_id>.result.json files.
    Updates manifest with ingested_at timestamps.
    """
    from zoomkb.manifest import load_manifest, save_manifest

    output_dir = manifest_path.parent
    queue_dir = output_dir / "extraction-queue"

    if not queue_dir.exists():
        logger.error("extraction-queue/ not found. Run 'zoomkb ingest --prepare' first.")
        return {
            "processed": 0, "entities_created": 0, "entities_updated": 0,
            "entities_deduped": 0, "entities_filtered": 0,
            "errors": 1, "skipped": 0,
        }

    manifest = load_manifest(manifest_path)

    # Read queue manifest
    qm_path = queue_dir / "queue-manifest.json"
    if qm_path.exists():
        queue_manifest = json.loads(qm_path.read_text(encoding="utf-8"))
        pending_ids = set(queue_manifest.get("article_ids", []))
    else:
        pending_ids = set()

    stats: dict[str, int] = {
        "processed": 0,
        "entities_created": 0,
        "entities_updated": 0,
        "entities_deduped": 0,
        "entities_filtered": 0,
        "entities_conflict_flagged": 0,
        "errors": 0,
        "skipped": 0,
    }

    # Build lookup for article metadata
    article_lookup: dict[str, dict] = {}
    for a in manifest.get("articles", []):
        article_lookup[a["article_id"]] = a

    # ── Phase 1: Collect all entities from .result.json files ─────────
    all_entities: list[WikiEntity] = []
    processed_articles: list[str] = []
    error_articles: list[tuple[str, str]] = []

    for result_file in sorted(queue_dir.glob("*.result.json")):
        article_id = result_file.stem.replace(".result", "")

        if pending_ids and article_id not in pending_ids:
            continue

        article = article_lookup.get(article_id, {})
        title = article.get("title", article_id)
        source_url = article.get("source_url", "")

        raw_candidates = list(raw_dir.glob(f"{article_id}*.md"))
        if raw_candidates:
            fm, _ = _extract_frontmatter_manual(raw_candidates[0].read_text(encoding="utf-8"))
            title = fm.get("title", title)
            source_url = fm.get("source_url", source_url)

        try:
            result = parse_extraction_result(result_file, article_id, title, source_url)
            raw_count = len(all_entities)
            all_entities.extend(result.entities)

            article_lookup[article_id]["ingested_at"] = datetime.now(timezone.utc).isoformat()
            article_lookup[article_id]["last_ingested_hash"] = article_lookup[article_id].get("content_hash", "")

            stats["processed"] += 1
            processed_articles.append(article_id)

        except Exception as e:
            logger.error("Commit failed for %s: %s", article_id, e)
            stats["errors"] += 1
            error_articles.append((article_id, str(e)))

    # ── Phase 2: Dedup, score, merge with disk, filter, write ──────────
    raw_entity_count = len(all_entities)
    merged_entities = _dedup_entities(all_entities)
    stats["entities_deduped"] = raw_entity_count - len(merged_entities)

    # Compute avg article relevance score for entity scoring
    avg_article_score = 8.0
    article_scores = [
        a.get("relevance_score", 8.0)
        for a in article_lookup.values()
        if isinstance(a.get("relevance_score"), (int, float))
    ]
    if article_scores:
        avg_article_score = sum(article_scores) / len(article_scores)

    type_dir_map: dict[str, str] = {
        "concept": "concepts", "user-role": "user-roles",
        "task-flow": "task-flows", "constraint": "constraints",
        "ux-pattern": "ux-patterns",
    }

    # Score all entities and merge with existing disk pages
    scored: list[tuple[float, WikiEntity]] = []
    quality_buckets = {"0-19": 0, "20-39": 0, "40-59": 0, "60-79": 0, "80-100": 0}

    for entity in merged_entities:
        # Merge with existing page on disk (if any)
        existing_disk_sources: list[dict[str, str]] = []
        subdir = wiki_dir / type_dir_map.get(entity.type, entity.type + "s")
        subdir.mkdir(parents=True, exist_ok=True)
        disk_path = subdir / f"{entity.slug}.md"
        if disk_path.exists():
            existing = _read_wiki_page(disk_path)
            if existing:
                for s in existing.sources:
                    if s["article_id"] not in {x["article_id"] for x in entity.sources}:
                        existing_disk_sources.append(s)

        # Total unique source articles (batch + disk)
        total_source_count = len(entity.sources) + len(existing_disk_sources)

        score = _score_entity(entity, avg_article_score)
        if total_source_count < min_sources:
            stats["entities_filtered"] += 1
            continue
        if score < min_quality:
            stats["entities_filtered"] += 1
            logger.debug("Filtered low-quality entity: %s (score=%.1f)", entity.slug, score)
            continue

        scored.append((score, entity))
        if score < 20:
            quality_buckets["0-19"] += 1
        elif score < 40:
            quality_buckets["20-39"] += 1
        elif score < 60:
            quality_buckets["40-59"] += 1
        elif score < 80:
            quality_buckets["60-79"] += 1
        else:
            quality_buckets["80-100"] += 1

    # Build valid_slugs from entities that will be written
    valid_slugs: set[str] = {e.slug for _, e in scored}

    # Sort by score descending, write wiki pages
    scored.sort(key=lambda x: x[0], reverse=True)
    entity_paths: set[Path] = set()

    for score, entity in scored:
        path, is_new, conflict = _write_wiki_page(entity, wiki_dir, product=product, valid_slugs=valid_slugs)
        if is_new:
            stats["entities_created"] += 1
            entity_paths.add(path)
        else:
            stats["entities_updated"] += 1
        if conflict:
            stats["entities_conflict_flagged"] += 1

    # Count unprocessed as skipped
    if pending_ids:
        processed_set = set(processed_articles)
        stats["skipped"] = len(pending_ids - processed_set)

    manifest["articles"] = list(article_lookup.values())
    save_manifest(manifest_path, manifest)

    _generate_index(wiki_dir, product)
    _write_ingest_report(
        output_dir, stats, processed_articles, error_articles,
        quality_buckets=quality_buckets, avg_score=_avg_score(scored),
    )

    return stats


def _avg_score(scored: list) -> float:
    if not scored:
        return 0.0
    return sum(s for s, _ in scored) / len(scored)


# ── Dry run ────────────────────────────────────────────────────────

def dry_run_ingest(
    manifest_path: Path,
    raw_dir: Path,
    force: bool = False,
    article_ids: Optional[List[str]] = None,
    min_sources: int = 1,
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
        "min_sources": min_sources,
    }


# ── Report & Index generation ──────────────────────────────────────

def _write_ingest_report(
    output_dir: Path,
    stats: dict[str, Any],
    processed: list[str],
    errors: list[tuple[str, str]],
    quality_buckets: Optional[dict[str, int]] = None,
    avg_score: float = 0.0,
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
        f"| Entities deduped | {stats.get('entities_deduped', 0)} |",
        f"| Entities filtered (< min_sources or < min_quality) | {stats.get('entities_filtered', 0)} |",
        f"| Entities conflict-flagged (≥3 source articles) | {stats.get('entities_conflict_flagged', 0)} |",
        f"| Errors | {stats['errors']} |",
        f"| Skipped | {stats['skipped']} |",
    ]

    if avg_score > 0:
        lines.append(f"| Avg entity quality score | {avg_score:.1f}/100 |")

    lines.append("")

    if quality_buckets:
        lines.extend([
            "## Quality Score Distribution",
            "",
            f"| Range | Count |",
            f"|-------|-------|",
            f"| 0-19 | {quality_buckets.get('0-19', 0)} |",
            f"| 20-39 | {quality_buckets.get('20-39', 0)} |",
            f"| 40-59 | {quality_buckets.get('40-59', 0)} |",
            f"| 60-79 | {quality_buckets.get('60-79', 0)} |",
            f"| 80-100 | {quality_buckets.get('80-100', 0)} |",
            "",
        ])

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
    ]

    section_headers = [
        ("Concepts", "concept"),
        ("User Roles", "user-role"),
        ("Task Flows", "task-flow"),
        ("Constraints", "constraint"),
        ("UX Patterns", "ux-pattern"),
    ]
    for header, key in section_headers:
        lines.extend(["", f"## {header}", ""])
        if sections[key]:
            for slug, title in sections[key]:
                lines.append(f"- [[{slug}]] — {title}")
        else:
            lines.append("_No entries yet._")

    lines.append("")

    (wiki_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")
    logger.info("Generated wiki/index.md")
