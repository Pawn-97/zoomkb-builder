---
name: zoomkb
description: Build structured, traceable, design-facing knowledge bases from Zoom Support Center articles. Use when designers request a UX KB, support article extraction, knowledge base generation, or domain research for Zoom products (Zoom Phone, Zoom Contact Center, Zoom Clips, Zoom Meetings, Zoom Rooms, Shared Zoom Platform).
license: MIT
compatibility: Requires Python 3.9+, network access to support.zoom.com
---

# Zoom Support KB Builder

Build a "wiki layer" from official Zoom Support articles — concept pages, user-role descriptions, task-flows, constraints, and UX patterns. All sourced from raw support articles, transformed into design knowledge by you (the LLM).

## Quick start

```
/zoomkb:build --product "Zoom Phone"
```

This runs the full pipeline end-to-end. For a complete list of commands and options, see [references/cli-reference.md](references/cli-reference.md).

## Pipeline

```
sitemap discovery → crawl (JSON-LD) → classify (relevance scoring) → validate → ingest-prepare → extract → ingest-commit → lint
```

## How to run each step

### 1. Init — Create KB directory

Run `/zoomkb:init --product "Zoom Phone"` via the CLI. Creates the directory structure, manifest.json, and log.

### 2. Discover — Find candidate articles

Run `/zoomkb:discover --product "Zoom Phone"`. Reads robots.txt, follows sitemaps, filters by product-relevance signals. Outputs `candidate-articles.json`.

### 3. Crawl — Fetch article content

Run `/zoomkb:crawl`. Fetches each candidate URL, extracts content via JSON-LD (primary) or Trafilatura (fallback). Writes raw markdown with frontmatter to `raw/support-articles/`.

### 4. Validate — Check article quality

Run `/zoomkb:validate`. Checks frontmatter completeness, content quality, and deduplication. Articles below the quality threshold move to `review/rejected/`.

### 5. Classify — Score relevance

Rule-based scoring by default (keyword matching, title signals, product mentions). If the user sets `ZOOMKB_LLM_CLASSIFIER=1`, an optional LLM refinement pass runs. See [references/architecture.md](references/architecture.md) for the scoring table.

### 6. Ingest — Prepare extraction prompts

Run `/zoomkb:ingest --prepare`. Groups accepted articles by entity (feature, user role, task, etc.) and writes `.prompt.md` files to `extraction-queue/`. Each prompt asks you to extract structured entities from the grouped source articles.

### 7. Extract — YOU do this step

This step is your job. No CLI command — you read and process the files directly:

1. Read each `extraction-queue/*.prompt.md` file
2. For each prompt, analyze the source article content and extract entities (concepts, task-flows, user-roles, constraints, ux-patterns)
3. Write structured JSON to `extraction-queue/*.result.json`

Each result.json should follow this schema:
```json
{
  "entities": [
    {
      "type": "concept|task-flow|user-role|constraint|ux-pattern",
      "title": "Entity title (sentence case)",
      "description": "Concise description from source articles",
      "source_article_ids": ["KB0060257"],
      "quality_score": 85
    }
  ]
}
```

Quality scoring guidelines:
- **80-100**: Entity backed by 3+ articles with clear, consistent descriptions
- **50-79**: Entity backed by 1-2 articles, descriptions mostly clear
- **20-49**: Entity inferred from fragments, low confidence
- **< 20**: Do not emit — below minimum quality threshold

### 8. Commit — Write wiki pages

Run `/zoomkb:ingest --commit`. Reads all `.result.json` files, deduplicates entities across extraction batches, filters by `--min-quality` and `--min-sources`, then writes markdown pages to `wiki/`.

### 9. Lint — Quality check

Run `/zoomkb:lint`. Checks traceability (every wiki claim links to a raw source), coverage (no orphan entities), consistency, freshness, and navigation.

## Decision rules

- **Score >= 8**: Auto-accept. These articles clearly match the target product.
- **Score 4-7**: Move to `review/low-confidence/`. Flag for human review.
- **Score < 4**: Reject. Move to `review/rejected/`.
- **Score 0**: Article has zero relevance signals. Always reject.
- **Shorter than 100 words after extraction**: Reject regardless of score.

## Validation checklist

After each `/zoomkb:build` run, verify:

- [ ] `manifest.json` exists with valid `kb_type: "zoomkb"` and `kb_version`
- [ ] `wiki/index.md` covers all five subdirectories (concepts, task-flows, user-roles, constraints, ux-patterns)
- [ ] Every wiki page has frontmatter with `type`, `source_article_ids`, `quality_score`
- [ ] No orphan entities — each wiki entity references at least one raw article
- [ ] `lint-report.md` shows zero critical issues
- [ ] At least 2 source articles back each wiki entity (unless `--min-sources` is lowered)
- [ ] All raw articles in manifest have a status (`accepted`, `review`, or `rejected`)

## Refresh and maintenance

To detect outdated content: run `/zoomkb:refresh` which re-crawls accepted articles and compares content hashes. Changed articles move to `status: review`.

To check freshness without re-crawling: run `/zoomkb:freshness` which generates a staleness report based on `manifest.json` timestamps.

## Reference files

- [CLI command reference](references/cli-reference.md) — Full command list with all options
- [Architecture details](references/architecture.md) — KB design, extraction strategy, classification table, supported products, output structure, permissions
- [UX-partner integration](references/ux-partner-integration.md) — Detection, classification tags, citation policy
