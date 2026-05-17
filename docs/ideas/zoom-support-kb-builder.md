# Zoom Support KB Builder

## Problem Statement
How might we help Zoom product designers quickly build a trustworthy, structured, traceable product knowledge base from official Zoom Support articles — without manually curating hundreds of articles?

## Recommended Direction

**Phase 1: Seed-First Crawl Pipeline (ship first, discover later)**

Build a focused crawl → clean → classify → format pipeline. Designer provides seed URLs. System outputs clean markdown files with frontmatter, manifest, and confidence scores.

Auto-discovery is postponed to Phase 2. The core bet: **proving the crawl→format pipeline works is more valuable than proving discovery works.** Discovery is an optimization; clean article transformation is the product.

Key decisions:
- **No review queue in Phase 1.** Output flat folder of markdown. Designer reviews via file browser. Add queue only if scale demands it.
- **No wiki ingest in Phase 1.** Raw markdown + manifest is the MVP deliverable. UX-partner can ingest raw directly for testing.
- **LLM classifier, not rules.** The +5/-5 scoring rubric in your doc is a good taxonomy but unreliable as pure rules. Use it as prompt context for an LLM classifier. Single API call per article.
- **One fallback, not three.** requests + JSON-LD primary. Trafilatura fallback if JSON-LD missing/empty. Crawl4AI optional fallback (disabled by default). Scrapling is scope creep for Phase 1.

Phase 2 adds auto-discovery (sitemap → seed expansion). Phase 3 adds wiki ingest (raw → concepts/roles/flows). Phase 4 adds multi-product + shared platform.

## Key Assumptions to Validate

- [ ] Crawl4AI successfully extracts meaningful content from Zoom ServiceNow article pages (test 5-10 URLs)
- [ ] LLM classifier accurately distinguishes Zoom Phone articles from cross-product articles (test 20-30 articles, aim >90% precision)
- [ ] UX-partner can ingest raw markdown directly and answer design questions with it (test with 10-20 articles)
- [ ] Designer can provide 10-20 seed URLs without significant friction (ask 2-3 designers)

## MVP Scope (Phase 1)

**In:**
- `/zoomkb:init` — create directory structure, manifest template
- `/zoomkb:crawl` — accept seed URL list, crawl with Crawl4AI, fallback to Trafilatura
- `/zoomkb:validate` — check frontmatter, content quality, hash dedup
- Output: flat folder of `.md` files + `manifest.json`

**Out (Phase 2+):**
- Auto-discovery (`/zoomkb:discover`) — sitemap parsing, robots.txt, link expansion
- Review queue UI / file structure — flat output sufficient for <100 articles
- Wiki ingest (`/zoomkb:ingest`) — raw markdown proves value first
- Multi-product support — Zoom Phone only in Phase 1
- Lint rules — manual review sufficient initially
- Scrapling fallback — Crawl4AI + Trafilatura covers 95%+ cases
- Shared platform layer — single product KB first

## Not Doing (and Why)

- **Auto-discovery in Phase 1** — highest uncertainty, easiest to defer. Seed URLs validate pipeline without discovery risk.
- **Review queue file structure** — adds filesystem complexity. For <100 articles, flat folder + manifest is readable.
- **Wiki layer generation** — requires schema stability, ingest rules, page type definitions. Raw markdown lets UX-partner test immediately.
- **Multi-product shared platform** — abstraction before concrete. Build one product KB that works, then generalize.
- **Scrapling as fallback** — Trafilatura is simpler, lighter, purpose-built for article extraction. Scrapling is overkill.
- **Complex rules-based classifier** — LLM classifier is more accurate and simpler to implement. Rules are good taxonomy, bad implementation.
- **/zoomkb:build one-shot command** — 4 separate commands give visibility into failures. One-shot hides which step breaks.

## Open Questions

- Has Crawl4AI been tested against Zoom Support pages? What's the actual output quality?
- What's the per-article cost of LLM classification at scale (e.g., 500 articles)?
- Do designers already have bookmarked/know key support articles, or is discovery genuinely the blocker?
- Should raw markdown include full article body, or truncated/summarized for UX-partner context limits?
- What's the retention/compliance policy for storing Zoom Support content locally?
