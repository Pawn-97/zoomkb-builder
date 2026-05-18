---
name: zoomkb
description: Build structured, traceable, design-facing knowledge bases from Zoom Support Center articles. Use when designers want to generate a UX KB for a Zoom product line (Zoom Phone, Zoom Contact Center, etc.).
---

# Zoom Support KB Builder

Build a structured, design-facing knowledge base from official Zoom Support articles. Produces a "wiki layer" with concept pages, user-role descriptions, task-flows, constraints, and UX patterns — all sourced from raw support articles but transformed into design knowledge by an LLM.

## Pipeline

```
sitemap discovery → crawl (JSON-LD) → classify (relevance scoring) → validate → ingest-prepare → Claude Code extract → ingest-commit → lint
```

## Commands

### `/zoomkb:build` — One-shot full pipeline

Runs the entire pipeline: init → discover → crawl → validate → ingest-prepare → extract → ingest-commit → lint.

**Extract step** (step 6) is handled by Claude Code: it reads `extraction-queue/*.prompt.md` files, extracts entities, and writes `extraction-queue/*.result.json` files. No external API required.

```
/zoomkb:build --product "Zoom Phone"
```

Options:
- `--product` — Target product (default: "Zoom Phone")
- `--output` — KB output directory (default: "./zoom-phone-kb")
- `--max-candidates N` — Limit discovery to N candidates
- `--urls URL1 URL2` — Bypass discovery, crawl specific URLs
- `--url-file path.txt` — Bypass discovery, crawl URLs from file
- `--dry-run` — Preview without LLM ingest
- `--force` — Re-ingest already processed articles
- `--skip-discover` — Skip discovery (use existing candidates)
- `--skip-crawl` — Skip crawl (use existing raw articles)
- `--fetch-titles` — Enable title-based filtering in discovery
- `--locale en` — Language filter (default: en)
- `--min-sources N` — Minimum source articles per wiki entity (default: 2)
- `--min-quality N` — Minimum entity quality score 0-100 (default: 20)

### `/zoomkb:build-all` — Initialize all product KBs

Creates KB directory structures for all supported Zoom product lines in one shot.

```
/zoomkb:build-all
```

This initializes KBs for: Zoom Phone, Zoom Contact Center, Zoom Clips, Zoom Meetings, Zoom Rooms, and Shared Zoom Platform. Each product gets its own directory (e.g., `./zoom-phone-kb/`, `./zoom-contact-center-kb/`, etc.).

After `build-all`, run `/zoomkb:build --product "Zoom Phone"` (or any other product) to run the full pipeline for that product line.

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
2. Claude Code — reads prompts, extracts entities, writes `.result.json`
3. `--commit` — reads results, deduplicates, filters by quality, writes wiki pages

```
/zoomkb:ingest --dry-run              # Preview what would be ingested
/zoomkb:ingest --force                # Re-ingest all accepted articles
/zoomkb:ingest --article-ids KB0060257 KB0069655  # Specific articles only
/zoomkb:ingest --commit --min-sources 3  # Only entities backed by ≥ 3 sources
/zoomkb:ingest --prepare --min-sources 2 --force
```

### `/zoomkb:extract` — Claude Code entity extraction

Not a CLI command. When `/zoomkb:build` reaches the extract step, Claude Code reads each `extraction-queue/*.prompt.md` file, analyzes the article content, and writes structured entity JSON to `extraction-queue/*.result.json`.

If running extract standalone (e.g., after adding new raw articles to an existing KB), tell Claude Code:
```
Process extraction-queue/*.prompt.md files, write .result.json files
```

### `/zoomkb:refresh` — Re-crawl and detect changes

Re-crawls accepted articles, compares content hashes, and flags changed or stale content for review.

```
/zoomkb:refresh --output ./zoom-phone-kb
/zoomkb:refresh --force                 # Force refresh even if recently checked
/zoomkb:refresh --article-ids KB0060257 # Specific articles only
/zoomkb:refresh --stale-days 14         # Custom stale threshold
```

Output: refreshes `manifest.json` (updates `last_checked_at`, changed articles move to `status: review`). Generates `refresh-report.md`.

### `/zoomkb:freshness` — Source freshness report

Generates a comprehensive source freshness report showing which articles are fresh, stale, or in the review queue.

```
/zoomkb:freshness --output ./zoom-phone-kb
/zoomkb:freshness --stale-days 60       # Custom stale threshold
```

Output: `freshness-report.md` with per-article table, stale article list, and review queue.

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

## Supported Products

| Product | CLI key | KB directory |
|---|---|---|
| Zoom Phone | `"Zoom Phone"` | `./zoom-phone-kb/` |
| Zoom Contact Center | `"Zoom Contact Center"` | `./zoom-contact-center-kb/` |
| Zoom Clips | `"Zoom Clips"` | `./zoom-clips-kb/` |
| Zoom Meetings | `"Zoom Meetings"` | `./zoom-meetings-kb/` |
| Zoom Rooms | `"Zoom Rooms"` | `./zoom-rooms-kb/` |
| Shared Zoom Platform | `"Shared Zoom Platform"` | `./shared-zoom-platform-kb/` |

**Shared Platform KB** is for cross-cutting knowledge that applies to all products: account management, user profiles, admin dashboard, billing, SSO, accessibility, desktop/mobile clients, etc. Individual product KBs reference shared platform concepts via wikilinks.

## Requirements

```
pip install zoomkb        # Core (crawl, discover, validate, lint, ingest)
pip install zoomkb[dev]   # Optional: pytest, ruff, mypy
```

Environment variables (all optional):
- `ZOOMKB_CRAWL4AI=1` — Enable Crawl4AI fallback for client-side rendered pages

## Permissions

This skill requires:
- **Network access** — HTTP requests to `support.zoom.com` (discovery + crawl)
- **File write** — KB output directory (markdown, JSON, reports)
- **Shell execution** — Python subprocess for zoomkb CLI commands

## Output structure

```
zoom-phone-kb/
├── manifest.json
├── log.md
├── crawl-report.md
├── ingest-report.md
├── lint-report.md
├── refresh-report.md
├── freshness-report.md
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

## UX-partner Integration

After building a KB with `/zoomkb:build`, the output is directly consumable by
UX-partner via its `setup-kb` command:

```bash
# 1. Build the KB
/zoomkb:build --product "Zoom Phone" --output ./zoom-phone-kb

# 2. In UX-partner, index it for design sessions
/ux-project:setup-kb ./zoom-phone-kb
```

### Detection

UX-partner's `setup-kb` detects zoomkb-builder output by checking
`manifest.json` for `"kb_type": "zoomkb"` (fallback: verifies `wiki/index.md`
and the five standard wiki subdirectories exist).

### Classification tags

Each wiki page is tagged by its source directory when indexed into
context-mode FTS5:

| Wiki path | UX-partner tag | Usage |
|---|---|---|
| `wiki/concepts/` | CONCEPT | Product concepts and features |
| `wiki/task-flows/` | TASK-FLOW | User task steps and dependencies |
| `wiki/user-roles/` | USER-ROLE | Role definitions and permissions |
| `wiki/constraints/` | CONSTRAINT | Design limitations and rules |
| `wiki/ux-patterns/` | UX-PATTERN | Reusable interaction patterns |
| `raw/support-articles/` | RAW-SOURCE | Ground truth — always cite |
| `wiki/index.md` | META | Navigation index |

### Citation policy

UX-partner applies a cite-or-die policy: every UX claim must reference a KB
page. Citation priority order (from SKILL.md §cite-or-die):

1. PRD / PM requirement document
2. KB wiki pages (concepts, task-flows, constraints, user-roles, ux-patterns)
3. KB raw articles (support articles — ultimate authority)
4. Project memory files
5. Assumptions (explicitly marked)

Raw articles are never LLM-rewritten, making them the most authoritative
source for fact-checking wiki claims.
