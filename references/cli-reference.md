# CLI Command Reference

## `/zoomkb:build` — One-shot full pipeline

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
- `--dry-run` — Preview without LLM ingest
- `--force` — Re-ingest already processed articles
- `--skip-discover` — Skip discovery (use existing candidates)
- `--skip-crawl` — Skip crawl (use existing raw articles)
- `--fetch-titles` — Enable title-based filtering in discovery
- `--locale en` — Language filter (default: en)
- `--min-sources N` — Minimum source articles per wiki entity (default: 2)
- `--min-quality N` — Minimum entity quality score 0-100 (default: 20)

## `/zoomkb:build-all` — Initialize all product KBs

Creates KB directory structures for all supported Zoom product lines.

```
/zoomkb:build-all
```

## `/zoomkb:init` — Initialize KB directory

Creates directory structure, manifest.json, log.md, crawl-report.md.

```
/zoomkb:init --product "Zoom Phone" --output "./zoom-phone-kb"
```

## `/zoomkb:discover` — Discover candidate articles

Reads robots.txt → sitemaps → extracts article URLs → filters by relevance signals.

```
/zoomkb:discover --product "Zoom Phone" --max-candidates 300
```

## `/zoomkb:crawl` — Crawl and extract articles

Fetches articles (requests + JSON-LD primary, Trafilatura fallback), generates raw markdown with frontmatter.

```
/zoomkb:crawl --urls "https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060257"
/zoomkb:crawl --url-file candidates.txt
```

## `/zoomkb:validate` — Validate raw articles

Checks frontmatter, content quality, dedup. Optional reclassification with `--reclassify`.

```
/zoomkb:validate --reclassify
```

## `/zoomkb:ingest` — Prepare and commit wiki pages

Three-stage pipeline:
1. `--prepare` — writes `.prompt.md` files to `extraction-queue/`
2. Claude Code — reads prompts, extracts entities, writes `.result.json`
3. `--commit` — reads results, deduplicates, filters by quality, writes wiki pages

```
/zoomkb:ingest --dry-run              # Preview what would be ingested
/zoomkb:ingest --force                # Re-ingest all accepted articles
/zoomkb:ingest --article-ids KB0060257 KB0069655  # Specific articles only
/zoomkb:ingest --commit --min-sources 3  # Only entities backed by >= 3 sources
/zoomkb:ingest --prepare --min-sources 2 --force
```

## `/zoomkb:refresh` — Re-crawl and detect changes

Re-crawls accepted articles, compares content hashes, flags changed/stale content.

```
/zoomkb:refresh --output ./zoom-phone-kb
/zoomkb:refresh --force                 # Force refresh even if recently checked
/zoomkb:refresh --article-ids KB0060257 # Specific articles only
/zoomkb:refresh --stale-days 14         # Custom stale threshold
```

## `/zoomkb:freshness` — Source freshness report

Generates a source freshness report showing article status.

```
/zoomkb:freshness --output ./zoom-phone-kb
/zoomkb:freshness --stale-days 60       # Custom stale threshold
```

## `/zoomkb:lint` — Quality checks

Checks traceability, coverage, consistency, freshness, navigation, and quality.

```
/zoomkb:lint --strict              # Exit non-zero on any issue
/zoomkb:lint --stale-days 60       # Custom stale threshold
```
