# KB Schema

This document defines the structure and conventions for the Zoom product line knowledge base.

## Directory layout

```
{product-slug}/
├── manifest.json           # Registry of all articles and their status
├── log.md                  # Human-readable change log
├── crawl-report.md         # Crawl statistics and extraction summary
├── ingest-report.md        # Ingest statistics and entity summary
├── lint-report.md          # Latest lint results
├── candidate-articles.json # Discovery output: candidate URLs with metadata
├── raw/
│   └── support-articles/   # Source of truth — never LLM-rewritten
│       └── {article_id}-{slug}.md
├── review/
│   ├── low-confidence/     # Articles flagged for manual review
│   └── rejected/           # Articles excluded from KB
└── wiki/
    ├── index.md            # Master index of all wiki pages
    ├── concepts/           # Product concepts and features
    ├── user-roles/         # Roles, permissions, visibility scopes
    ├── task-flows/         # User tasks with steps and dependencies
    ├── constraints/        # Design constraints and limitations
    └── ux-patterns/        # Reusable interaction patterns
```

## Naming conventions

- **Directory names**: kebab-case, plural for collections (`concepts/`, `user-roles/`)
- **File names**: `{article_id}-{slug}.md` for raw articles, `{slug}.md` for wiki pages
- **Slugs**: lowercase, hyphen-separated, max 80 chars, derived from title
- **Product identifiers**: kebab-case (`zoom-phone`, `zoom-contact-center`)

## Article lifecycle

```
discovered → crawled → classified → accepted/review/rejected → ingested → stale
```

Status values in manifest:
- `accepted` — High confidence, auto-ingested
- `review` — Medium confidence, needs human review
- `rejected` — Low confidence or off-topic
- `ingested` — Has been processed into wiki pages

## Freshness policy

- Raw articles: re-check source URL monthly
- Wiki pages: review at least every 90 days
- Stale detection: compare `content_hash` with fresh crawl
- `last_reviewed` field tracks wiki review date
