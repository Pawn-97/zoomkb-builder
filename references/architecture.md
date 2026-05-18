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
