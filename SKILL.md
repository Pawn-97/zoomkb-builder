---
name: zoomkb
description: Build structured, traceable, design-facing knowledge bases from Zoom Support Center articles. Use when designers want to generate a UX KB for a Zoom product line (Zoom Phone, Zoom Contact Center, etc.).
---

# Zoom Support KB Builder

Build a structured, design-facing knowledge base from official Zoom Support articles. Produces a "wiki layer" with concept pages, user-role descriptions, task-flows, constraints, and UX patterns — all sourced from raw support articles but transformed into design knowledge by an LLM.

## Pipeline

```
sitemap discovery → crawl (JSON-LD) → classify (relevance scoring) → validate → ingest (LLM wiki pages) → lint
```

## Commands

### `/zoomkb:build` — One-shot full pipeline

Runs the entire pipeline: init → discover → crawl → validate → ingest → lint.

```
/zoomkb:build --product "Zoom Phone"
```

Options:
- `--product` — Target product (default: "Zoom Phone")
- `--output` — KB output directory (default: "./zoom-phone-kb")
- `--max-candidates N` — Limit discovery to N candidates
- `--urls URL1 URL2` — Bypass discovery, crawl specific URLs
- `--url-file path.txt` — Bypass discovery, crawl URLs from file
- `--dry-run` — Preview without calling LLM ingest
- `--force` — Re-ingest already processed articles
- `--skip-discover` — Skip discovery (use existing candidates)
- `--skip-crawl` — Skip crawl (use existing raw articles)
- `--fetch-titles` — Enable title-based filtering in discovery
- `--locale en` — Language filter (default: en)

### `/zoomkb:init` — Initialize KB directory

Creates directory structure, manifest.json, log.md, crawl-report.md.

```
/zoomkb:init --product "Zoom Phone" --output "./zoom-phone-kb"
```

### `/zoomkb:discover` — Discover candidate articles

Reads robots.txt → sitemaps → extracts article URLs → filters by relevance signals.

```
/zoomkb:discover --product "Zoom Phone" --max-candidates 300
```

### `/zoomkb:crawl` — Crawl and extract articles

Fetches articles (requests + JSON-LD primary, Trafilatura fallback), generates raw markdown with frontmatter.

```
/zoomkb:crawl --urls "https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060257"
/zoomkb:crawl --url-file candidates.txt
```

### `/zoomkb:validate` — Validate raw articles

Checks frontmatter, content quality, dedup. Optional reclassification with `--reclassify`.

```
/zoomkb:validate --reclassify
```

### `/zoomkb:ingest` — Generate wiki pages via LLM

Reads high-confidence raw articles, calls LLM to extract design-facing entities (concepts, user-roles, task-flows, constraints, UX-patterns). Entities are deduplicated by normalized slug (trailing 's' and common suffixes merged). Use `--min-sources` to filter out thin single-source stubs.

```
/zoomkb:ingest --dry-run              # Preview what would be ingested
/zoomkb:ingest --force                # Re-ingest all accepted articles
/zoomkb:ingest --article-ids KB0060257 KB0069655  # Specific articles only
/zoomkb:ingest --commit --min-sources 3  # Only entities backed by ≥ 3 sources
/zoomkb:ingest --prepare --min-sources 2 --force
```

Requires `pip install zoomkb[llm]` and `OPENAI_API_KEY` environment variable.

### `/zoomkb:lint` — Quality checks

Checks traceability, coverage, consistency, freshness, navigation, and quality.

```
/zoomkb:lint --strict              # Exit non-zero on any issue
/zoomkb:lint --stale-days 60       # Custom stale threshold
```

## Architecture

### Two-layer KB design

```
raw/support-articles/*.md   ← Source of truth (never LLM-rewritten)
  ↓ LLM ingest
wiki/concepts/*.md          ← Design-facing knowledge (LLM-compiled)
wiki/task-flows/*.md
wiki/user-roles/*.md
wiki/constraints/*.md
wiki/ux-patterns/*.md
```

### Extraction strategy

1. **JSON-LD** (primary) — Zoom Support pages embed Schema.org Article JSON-LD with clean `articleBody`
2. **Trafilatura** (fallback 1) — When JSON-LD is missing or empty
3. **Crawl4AI** (fallback 2, optional) — Headless browser extraction, requires `ZOOMKB_CRAWL4AI=1`

### Classification

Rule-based relevance scoring by default. Optional LLM refinement with `ZOOMKB_LLM_CLASSIFIER=1`.

| Score | Confidence | Action |
|-------|-----------|--------|
| ≥ 8 | High | Auto-accept, enters ingest |
| 4–7 | Medium | Review queue |
| < 4 | Low | Rejected |

## Requirements

```
pip install zoomkb        # Core (requests + JSON-LD extraction)
pip install zoomkb[llm]   # + LLM ingest (OpenAI)
pip install zoomkb[dev]   # + pytest, ruff, mypy
```

Environment variables:
- `OPENAI_API_KEY` — Required for ingest
- `ZOOMKB_LLM_MODEL` — Model override (default: `gpt-4o-mini`)
- `ZOOMKB_CRAWL4AI=1` — Enable Crawl4AI fallback
- `ZOOMKB_LLM_CLASSIFIER=1` — Enable LLM classification

## Permissions

This skill requires:
- **Network access** — HTTP requests to `support.zoom.com` (discovery + crawl)
- **File write** — KB output directory (markdown, JSON, reports)
- **Shell execution** — Python subprocess for zoomkb CLI commands
- **LLM API access** — OpenAI API for ingest phase (if using `--no-dry-run`)

## Output structure

```
zoom-phone-kb/
├── manifest.json
├── log.md
├── crawl-report.md
├── ingest-report.md
├── lint-report.md
├── candidate-articles.json
├── raw/
│   └── support-articles/
│       └── KB0060257-getting-started-with-zoom-phone.md
├── review/
│   ├── low-confidence/
│   └── rejected/
└── wiki/
    ├── index.md
    ├── concepts/
    ├── user-roles/
    ├── task-flows/
    ├── constraints/
    └── ux-patterns/
```
