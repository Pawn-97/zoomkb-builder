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

Runs the entire pipeline: init → discover → crawl → validate → ingest-prepare → extract → ingest-commit → lint.

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
- `--auto-extract` — Auto-run extract step via OpenAI API
- `--extract-model MODEL` — Model for auto-extract (default: gpt-4o-mini)
- `--extract-workers N` — Parallel extract workers (default: 3)

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

### `/zoomkb:ingest` — Prepare and commit wiki pages

Three-stage pipeline:
1. `--prepare` — writes `.prompt.md` files to `extraction-queue/`
2. `zoomkb extract` — processes prompts via OpenAI API → `.result.json`
3. `--commit` — reads results, deduplicates, filters by quality, writes wiki pages

```
/zoomkb:ingest --dry-run              # Preview what would be ingested
/zoomkb:ingest --force                # Re-ingest all accepted articles
/zoomkb:ingest --article-ids KB0060257 KB0069655  # Specific articles only
/zoomkb:ingest --commit --min-sources 3  # Only entities backed by ≥ 3 sources
/zoomkb:ingest --prepare --min-sources 2 --force
```

### `/zoomkb:extract` — Batch LLM extraction

Processes `.prompt.md` files in `extraction-queue/` via OpenAI API. Skips articles that already have `.result.json` files (use `--force` to re-extract).

```
/zoomkb:extract --dry-run             # Preview what would be extracted
/zoomkb:extract --force               # Re-extract all (ignore existing results)
/zoomkb:extract --max-workers 5       # Parallel extraction with 5 workers
/zoomkb:extract --model gpt-4o       # Use specific model
/zoomkb:extract --article-ids KB0060257 KB0069655  # Specific articles only
```

Requires `OPENAI_API_KEY` env var. Model defaults to `gpt-4o-mini` (override with `ZOOMKB_LLM_MODEL`).

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
pip install zoomkb        # Core (crawl, discover, validate, lint)
pip install zoomkb[llm]   # Optional: LLM-based relevance classifier (OpenAI)
pip install zoomkb[dev]   # Optional: pytest, ruff, mypy
```

Environment variables (all optional):
- `ZOOMKB_CRAWL4AI=1` — Enable Crawl4AI fallback
- `ZOOMKB_LLM_CLASSIFIER=1` — Enable LLM classification (requires `[llm]` + `OPENAI_API_KEY`)
- `ZOOMKB_LLM_MODEL` — Model override for classifier (default: `gpt-4o-mini`)
- `OPENAI_API_KEY` — Required only with `ZOOMKB_LLM_CLASSIFIER=1`

## Permissions

This skill requires:
- **Network access** — HTTP requests to `support.zoom.com` (discovery + crawl)
- **File write** — KB output directory (markdown, JSON, reports)
- **Shell execution** — Python subprocess for zoomkb CLI commands
- **LLM API access** — OpenAI API for optional LLM classifier (`ZOOMKB_LLM_CLASSIFIER=1`)

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
