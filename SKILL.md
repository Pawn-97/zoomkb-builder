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

This creates a complete KB end-to-end. The skill intentionally exposes only three user-facing actions:

| User goal | Command |
|---|---|
| Create a KB | `/zoomkb:build --product "Zoom Phone"` |
| Update an existing KB | `/zoomkb:refresh --output ./zoom-phone-kb` |
| Validate KB quality | `/zoomkb:lint --output ./zoom-phone-kb` |

Lower-level CLI subcommands exist for debugging and automation, but do not present them as the normal user workflow. See [references/cli-reference.md](references/cli-reference.md) only when you need advanced implementation details.

## Pipeline

```
sitemap discovery → crawl (JSON-LD) → classify (relevance scoring) → validate → ingest-prepare → extract → ingest-commit → lint
```

## User-facing actions

### Create a KB

Run `/zoomkb:build --product "Zoom Phone"`. This initializes the KB, discovers and crawls relevant support articles, validates raw sources, prepares extraction prompts, commits wiki pages, and runs quality checks.

### Update an existing KB

Run `/zoomkb:refresh --output ./zoom-phone-kb`. This re-crawls accepted source articles, compares content hashes, and moves changed articles back to review.

### Validate KB quality

Run `/zoomkb:lint --output ./zoom-phone-kb`. This checks traceability, coverage, consistency, freshness, navigation, and wiki page quality.

## Internal extraction step

During `/zoomkb:build`, the CLI prepares `extraction-queue/*.prompt.md` files. The LLM must process those prompts before commit:

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

To inspect source freshness without changing content, use the advanced CLI reference. Do not expose freshness as a primary skill command.

## Reference files

- [CLI command reference](references/cli-reference.md) — Full command list with all options
- [Architecture details](references/architecture.md) — KB design, extraction strategy, classification table, supported products, output structure, permissions
- [UX-partner integration](references/ux-partner-integration.md) — Detection, classification tags, citation policy
