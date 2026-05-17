# Lint Rules

Rules checked by `/zoomkb:lint`. Each rule belongs to a category and has a severity level.

## Traceability

| Rule | Severity | Description |
|------|----------|-------------|
| wiki-has-sources | error | Every wiki page must have a `sources` field in frontmatter |
| source-url-valid | error | Each source must include a valid source_url |
| claim-traceable | warn | Key claims should reference a specific source article |

## Coverage

| Rule | Severity | Description |
|------|----------|-------------|
| no-uningested-high-conf | warn | All high-confidence accepted articles should be ingested |
| no-missing-raw | error | Every manifest entry should have a corresponding raw file |
| index-is-current | warn | wiki/index.md should list all existing wiki pages |

## Consistency

| Rule | Severity | Description |
|------|----------|-------------|
| no-duplicate-slugs | warn | The same slug should not appear in multiple wiki subdirectories |
| product-name-consistent | warn | Product name should be consistent across all pages |
| no-conflicting-claims | error | Two pages should not make contradictory claims |

## Freshness

| Rule | Severity | Description |
|------|----------|-------------|
| last-reviewed-recent | warn | Wiki pages should have `last_reviewed` within `stale_days` (default 30) |
| content-hash-current | warn | Raw article `content_hash` should match stored hash in manifest |
| captured-at-recent | info | Article `captured_at` should not be excessively old |

## Navigation

| Rule | Severity | Description |
|------|----------|-------------|
| index-exists | error | wiki/index.md must exist |
| index-not-empty | warn | wiki/index.md should have substantive content |
| no-broken-wikilinks | error | All `[[wikilinks]]` should resolve to existing pages |
| no-orphan-pages | warn | Every wiki page should be referenced from at least one other page or index |

## Quality

| Rule | Severity | Description |
|------|----------|-------------|
| has-summary-section | warn | Every wiki page should have a `## Summary` section |
| has-key-points-section | warn | Every wiki page should have a `## Key points` section |
| summary-substantial | warn | Summary should be ≥ 50 characters |
| body-substantial | warn | Body should be ≥ 50 words |
| no-hallucination-markers | warn | Avoid phrases like "based on my training data" or unsourced claims |

## Severity levels

- **error**: Blocks CI in strict mode
- **warn**: Reported but does not block
- **info**: Informational only, surfaced in lint report
