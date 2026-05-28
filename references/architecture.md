# Architecture

## Two-layer KB design

```
raw/support-articles/*.md   ← Source of truth (never LLM-rewritten)
  ↓ LLM ingest
wiki/concepts/*.md          ← Design-facing knowledge (LLM-compiled)
wiki/task-flows/*.md
wiki/user-roles/*.md
wiki/constraints/*.md
wiki/ux-patterns/*.md
10-LLM-Wiki/*.md           ← Taxonomy, master index, full listings, cross references, category pages
30-Agent-Playbooks/*.md    ← Troubleshooting and root-cause playbooks
```

## Extraction strategy

1. **JSON-LD** (primary) — Zoom Support pages embed Schema.org Article JSON-LD with clean `articleBody`
2. **Trafilatura** (fallback 1) — When JSON-LD is missing or empty
3. **Crawl4AI** (fallback 2, optional) — Headless browser extraction, requires `ZOOMKB_CRAWL4AI=1`

## Classification

Rule-based relevance scoring by default. Optional LLM refinement with `ZOOMKB_LLM_CLASSIFIER=1`.

| Score | Confidence | Action |
|-------|-----------|--------|
| >= 8 | High | Auto-accept, enters ingest |
| 4-7 | Medium | Review queue |
| < 4 | Low | Rejected |

## Product taxonomy and navigation

All product KBs use the same design-facing taxonomy layer so Zoom Rooms is not treated as a one-off special case. The taxonomy categories cover deployment, concepts, task workflows, devices/surfaces, scheduling/collaboration, admin policy, integrations, requirements/support, troubleshooting, and AI/automation.

During ingest, each entity receives `primary_category`, actor, surface, source article IDs, and richer type-specific sections. After wiki pages are written, the builder generates:

- `10-LLM-Wiki/Taxonomy.md`
- `10-LLM-Wiki/Master Index.md`
- `10-LLM-Wiki/Full Category Listings.md`
- `10-LLM-Wiki/Feature Cross References.md`
- `10-LLM-Wiki/Category Pages/*.md`
- `30-Agent-Playbooks/Troubleshooting/*.md`

Lint treats these layers as required once wiki pages exist, and flags missing categories, thin bodies, over-merged source sets, incomplete task flows, incomplete UX patterns, low relationship density, and oversized constraints.

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
├── raw/
│   └── support-articles/
│       └── KB0060257-getting-started-with-zoom-phone.md
├── review/
│   ├── candidate-articles.json
│   ├── rejected-articles.json
│   ├── low-confidence/
│   └── rejected/
└── wiki/
    ├── index.md
    ├── concepts/
    ├── user-roles/
    ├── task-flows/
    ├── constraints/
    └── ux-patterns/
├── 10-LLM-Wiki/
│   ├── Master Index.md
│   ├── Taxonomy.md
│   ├── Full Category Listings.md
│   ├── Feature Cross References.md
│   └── Category Pages/
└── 30-Agent-Playbooks/
    └── Troubleshooting/
```

## Requirements

```
pip install zoomkb        # Core (crawl, discover, validate, lint, ingest)
pip install zoomkb[dev]   # Optional: pytest, ruff, mypy
```

Environment variables (all optional):
- `ZOOMKB_CRAWL4AI=1` — Enable Crawl4AI fallback for client-side rendered pages
- `ZOOMKB_LLM_CLASSIFIER=1` — Enable optional OpenAI-backed relevance refinement
- `ZOOMKB_LLM_MODEL` — Override the optional classifier model
- `OPENAI_API_KEY` — Required only when `ZOOMKB_LLM_CLASSIFIER=1`

## Permissions

This skill requires:
- **Network access** — HTTP requests to `support.zoom.com` (discovery + crawl)
- **File write** — KB output directory (markdown, JSON, reports)
- **Shell execution** — Python subprocess for zoomkb CLI commands
