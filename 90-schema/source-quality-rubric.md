# Source Quality Rubric

Criteria for evaluating whether a Zoom Support article is suitable for KB inclusion.

## Article quality scoring

### High quality (score 4–5)
- Clear, accurate, up-to-date information
- Well-structured with headings, steps, and tables
- Specific to the target product line
- Contains actionable information for designers
- Published or updated within the last 2 years

### Medium quality (score 2–3)
- Generally accurate but may have minor gaps
- Somewhat relevant but includes cross-product content
- Older but not obsolete
- Lacks detailed steps or examples

### Low quality (score 0–1)
- Outdated or superseded by newer articles
- Primarily about a different product
- Very short or generic content
- Marketing content, not instructional

## Extraction quality signals

| Signal | Good | Bad |
|--------|------|-----|
| articleBody in JSON-LD | Present and >1000 chars | Missing or <200 chars |
| Trafilatura fallback | Clean extraction, >500 chars | Navigation/cookie content mixed in |
| Frontmatter completeness | All required fields present | Missing article_id or source_url |
| Word count | >200 words | <50 words |

## Rejection criteria

Articles are rejected (not candidates) when:
- Not in English and no locale override configured
- Primarily about a different Zoom product (negative signals dominate)
- Purely marketing or release-notes content
- Duplicate of an already-accepted article (same content_hash)
- Behind login or requires authentication

## Re-evaluation

Articles in the review queue should be re-evaluated when:
- New relevance signals are added to the classifier
- Product aliases are updated in constants.py
- A human reviewer confirms or rejects the classification
