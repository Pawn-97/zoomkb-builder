"""CLI entry point for zoomkb."""

import argparse
import copy
import json
import logging

import sys
from pathlib import Path
from typing import List, Optional

from zoomkb.classifier import classify_relevance
from zoomkb.crawler import crawl_article
from zoomkb.discover import discover_articles
from zoomkb.ingest import commit_extraction, dry_run_ingest, prepare_extraction_queue
from zoomkb.manifest import add_article, init_manifest, load_manifest, save_manifest
from zoomkb.refresh import generate_freshness_report, refresh_articles
from zoomkb.lint import lint, write_lint_report
from zoomkb.validator import check_duplicates

logger = logging.getLogger("zoomkb")

# All supported product lines
ALL_PRODUCTS = [
    "Zoom Phone",
    "Zoom Contact Center",
    "Zoom Clips",
    "Zoom Meetings",
    "Zoom Rooms",
    "Shared Zoom Platform",
]


def _default_output(product: str) -> str:
    """Compute default output directory from product name."""
    slug = product.lower().replace(" ", "-")
    return f"./{slug}-kb"


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    fmt = "%(asctime)s %(levelname)s %(name)s: %(message)s"
    logging.basicConfig(level=level, format=fmt, datefmt="%H:%M:%S")


def cmd_discover(args: argparse.Namespace) -> int:
    """Discover candidate articles from sitemaps."""
    output = Path(args.output or _default_output(args.product))
    product = args.product.lower().replace(" ", "-")

    stats = discover_articles(
        source_root=args.source_root,
        product=product,
        output_dir=output,
        fetch_titles=args.fetch_titles,
        max_workers=args.max_workers,
        max_candidates=args.max_candidates,
        locale=args.locale,
    )

    if "error" in stats:
        logger.error("Discovery failed: %s", stats["error"])
        return 1

    print(f"Discovery complete for '{args.product}':")
    print(f"  Sitemaps found: {stats['sitemaps_found']}")
    print(f"  Total URLs: {stats['total_urls']}")
    print(f"  Article URLs: {stats['article_urls']}")
    print(f"  After dedup: {stats['after_dedup']}")
    print(f"  Candidates: {stats['candidates']}")
    print(f"  Rejected: {stats['rejected']}")
    print(f"\nCandidates saved to: {stats['candidate_file']}")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    """Initialize KB directory structure."""
    output = Path(args.output or _default_output(args.product))
    product = args.product.lower().replace(" ", "-")

    dirs = [
        output / "raw" / "support-articles",
        output / "review" / "low-confidence",
        output / "review" / "rejected",
        output / "wiki",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Ensure all five wiki-type subdirectories exist for UX-partner compatibility
    for sub in ["concepts", "task-flows", "user-roles", "constraints", "ux-patterns"]:
        (output / "wiki" / sub).mkdir(parents=True, exist_ok=True)

    manifest_path = init_manifest(product, output)

    # Create placeholder files
    (output / "log.md").write_text(f"# {args.product} KB Log\n\n", encoding="utf-8")
    (output / "crawl-report.md").write_text("# Crawl Report\n\n", encoding="utf-8")

    print(f"Initialized KB for '{args.product}' at {output}")
    print(f"Manifest: {manifest_path}")
    return 0


def cmd_crawl(args: argparse.Namespace) -> int:
    """Crawl seed URLs and save articles."""
    output = Path(args.output)
    manifest_path = output / "manifest.json"
    raw_dir = output / "raw" / "support-articles"

    if not manifest_path.exists():
        logger.error("Manifest not found. Run 'zoomkb init' first.")
        return 1

    urls: list[str] = []
    if args.urls:
        urls = args.urls
    elif args.url_file:
        urls = [line.strip() for line in Path(args.url_file).read_text().splitlines() if line.strip()]
    else:
        logger.error("No URLs provided. Use --urls or --url-file.")
        return 1

    product = load_manifest(manifest_path).get("product", "zoom-phone")
    results = {"success": 0, "failed": 0, "skipped": 0}

    for url in urls:
        try:
            meta = crawl_article(url, raw_dir, product=product)

            # Deduplication check
            if check_duplicates(manifest_path, meta["content_hash"], meta["article_id"]):
                logger.info("Skipping duplicate: %s", meta["article_id"])
                results["skipped"] += 1
                continue

            add_article(manifest_path, meta)
            results["success"] += 1
        except Exception as e:
            logger.error("Failed to crawl %s: %s", url, e)
            results["failed"] += 1

    print(f"\nCrawl complete: {results['success']} success, {results['failed']} failed, {results['skipped']} skipped")
    return 0 if results["failed"] == 0 else 1


def cmd_ingest(args: argparse.Namespace) -> int:
    """Ingest accepted raw articles into wiki.

    Pipeline:
      1. --prepare: write extraction prompt files
      2. Claude Code processes prompts → .result.json files
      3. --commit: read results, write wiki pages, update manifest
    """
    output = Path(args.output)
    manifest_path = output / "manifest.json"
    raw_dir = output / "raw" / "support-articles"
    wiki_dir = output / "wiki"

    if not manifest_path.exists():
        logger.error("Manifest not found. Run 'zoomkb init' first.")
        return 1

    # Dry run mode
    if args.dry_run:
        stats = dry_run_ingest(
            manifest_path=manifest_path,
            raw_dir=raw_dir,
            force=args.force,
            article_ids=args.article_ids or None,
            min_sources=args.min_sources,
        )
        print(f"\nDry run — would prepare {stats['total']} articles for extraction:")
        for aid in stats["candidates"]:
            print(f"  - {aid}")
        if stats["missing_raw_files"]:
            print(f"\nWarning: {stats['missing_raw_files']} articles have missing raw files")
        print(f"\nMin sources filter: {stats['min_sources']}")
        print(f"Wiki output would go to: {wiki_dir}")
        return 0

    # Prepare mode: write extraction prompts
    if args.prepare:
        manifest = load_manifest(manifest_path)
        product = manifest.get("product", "zoom-phone")

        qm = prepare_extraction_queue(
            manifest_path=manifest_path,
            raw_dir=raw_dir,
            product=product,
            force=args.force,
            article_ids=args.article_ids or None,
        )

        print(f"\nExtraction queue prepared:")
        print(f"  Articles ready: {qm['total']}")
        print(f"  Skipped (already ingested): {qm['skipped_ingested']}")
        print(f"  Skipped (missing raw file): {qm['skipped_missing']}")
        print(f"\nNext step: Claude Code processes prompts in extraction-queue/")
        print(f"  For each .prompt.md file, extract entities and save as .result.json")
        print(f"  Then run: zoomkb ingest --output {args.output} --commit --min-sources {args.min_sources}")
        return 0

    # Commit mode: read results, write wiki pages
    if args.commit:
        manifest = load_manifest(manifest_path)
        product = manifest.get("product", "zoom-phone")

        stats = commit_extraction(
            manifest_path=manifest_path,
            raw_dir=raw_dir,
            wiki_dir=wiki_dir,
            product=product,
            min_sources=args.min_sources,
            min_quality=args.min_quality,
        )

        print(f"\nIngest commit complete:")
        print(f"  Articles processed: {stats['processed']}")
        print(f"  Entities created: {stats['entities_created']}")
        print(f"  Entities updated: {stats['entities_updated']}")
        print(f"  Entities deduped: {stats.get('entities_deduped', 0)}")
        filter_reason = f"sources < {args.min_sources} or quality < {args.min_quality}"
        print(f"  Entities filtered ({filter_reason}): {stats.get('entities_filtered', 0)}")
        print(f"  Entities conflict-flagged (>=3 source articles): {stats.get('entities_conflict_flagged', 0)}")
        print(f"  Errors: {stats['errors']}")
        print(f"  Skipped: {stats['skipped']}")
        print(f"\nWiki output: {wiki_dir}")

        return 0 if stats["errors"] == 0 else 1

    # No mode specified
    logger.error("Specify --prepare, --commit, or --dry-run.")
    return 1


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate all raw articles."""
    output = Path(args.output)
    manifest_path = output / "manifest.json"
    raw_dir = output / "raw" / "support-articles"

    if not manifest_path.exists():
        logger.error("Manifest not found.")
        return 1

    manifest = load_manifest(manifest_path)
    issues = []

    for article in manifest.get("articles", []):
        md_path = output / article.get("local_path", f"raw/support-articles/{article['article_id']}.md")
        if not md_path.exists():
            issues.append(f"Missing file: {article['article_id']}")
            continue

        content = md_path.read_text(encoding="utf-8")
        if "---" not in content:
            issues.append(f"Missing frontmatter: {article['article_id']}")

        # Re-check relevance if requested
        if args.reclassify:
            lines = content.split("\n")
            title = article.get("title", "")
            body = "\n".join(lines[lines.index("---", 1) + 1:] if "---" in lines else lines)
            score, confidence = classify_relevance(body, title, manifest.get("product", "zoom-phone"))
            if confidence != article.get("confidence"):
                logger.info("Reclassified %s: %s -> %s (score=%d)",
                            article["article_id"], article.get("confidence"), confidence, score)
                article["relevance_score"] = score
                article["confidence"] = confidence
                article["status"] = "accepted" if confidence == "high" else ("review" if confidence == "medium" else "rejected")

    # Recalculate and save if reclassifying
    if args.reclassify:
        stats = {"total": 0, "accepted": 0, "review": 0, "rejected": 0}
        for a in manifest["articles"]:
            stats["total"] += 1
            s = a.get("status", "review")
            if s in stats:
                stats[s] += 1
        manifest["stats"] = stats
        save_manifest(manifest_path, manifest)
        print(f"Reclassified. Updated stats: {stats}")

    if issues:
        print(f"Found {len(issues)} issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("All articles passed validation.")

    return 0


def cmd_lint(args: argparse.Namespace) -> int:
    """Lint the KB for quality, consistency, and completeness."""
    output = Path(args.output)

    report = lint(
        output_dir=output,
        stale_days=args.stale_days,
        strict=args.strict,
    )

    # Print summary
    sections = {
        "traceability": "Traceability",
        "coverage": "Coverage",
        "consistency": "Consistency",
        "freshness": "Freshness",
        "navigation": "Navigation",
        "quality": "Quality",
    }

    for key, label in sections.items():
        issues = report.get(key, [])
        count = sum(1 for i in issues if i and not (i.startswith("All ") or i.startswith("No ")))
        if count:
            print(f"[WARN] {label}: {count} issue(s)")
            for issue in issues:
                if issue and not issue.startswith("All ") and not issue.startswith("No "):
                    print(f"  - {issue}")
        else:
            print(f"[OK]   {label}")

    report_path = write_lint_report(output, report)
    print(f"\nLint report: {report_path}")
    print(f"Result: {'PASSED' if report['passed'] else 'FAILED'} ({report['total_issues']} issues)")
    return report["exit_code"]


def cmd_refresh(args: argparse.Namespace) -> int:
    """Re-crawl accepted articles, diff content hashes, detect changes and staleness."""
    output = Path(args.output)
    manifest_path = output / "manifest.json"
    raw_dir = output / "raw" / "support-articles"

    if not manifest_path.exists():
        logger.error("Manifest not found. Run 'zoomkb init' first.")
        return 1

    manifest = load_manifest(manifest_path)
    product = manifest.get("product", "zoom-phone")

    stats = refresh_articles(
        manifest_path=manifest_path,
        raw_dir=raw_dir,
        product=product,
        article_ids=args.article_ids or None,
        force=args.force,
        max_workers=args.max_workers,
        stale_days=args.stale_days,
    )

    print(f"\nRefresh complete for '{product}':")
    print(f"  Total: {stats['total']}")
    print(f"  Changed: {stats['changed']}")
    print(f"  Unchanged: {stats['unchanged']}")
    print(f"  Stale: {stats['stale']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Skipped: {stats.get('skipped', 0)}")

    if stats["changed"]:
        print(f"\n{stats['changed']} article(s) changed — moved to review queue.")
        print("Run 'zoomkb freshness' for details.")

    print(f"\nReport: {output / 'refresh-report.md'}")
    return 0 if stats["errors"] == 0 else 1


def cmd_freshness(args: argparse.Namespace) -> int:
    """Generate source freshness report."""
    output = Path(args.output)
    manifest_path = output / "manifest.json"

    if not manifest_path.exists():
        logger.error("Manifest not found. Run 'zoomkb init' first.")
        return 1

    report = generate_freshness_report(
        manifest_path=manifest_path,
        stale_days=args.stale_days,
    )

    print(f"\nFreshness report for '{output}':")
    print(f"  Total articles: {report['total']}")
    print(f"  Fresh (checked within {report['stale_days']}d): {report['fresh']}")
    print(f"  Stale (not checked in {report['stale_days']}+d): {report['stale']}")
    print(f"  Review queue: {report['review']}")

    if report["stale"]:
        print(f"\nWarning: {report['stale']} stale articles. Run 'zoomkb refresh' to update.")
    if report["review"]:
        print(f"\n{report['review']} articles in review queue. Review and re-accept or reject.")

    print(f"\nReport: {output / 'freshness-report.md'}")
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    """One-shot: init → discover → crawl → validate → ingest → lint."""
    output = Path(args.output or _default_output(args.product))

    print("=" * 50)
    print("zoomkb:build — full pipeline (7 steps)")
    print("=" * 50)

    # Step 1: init
    print("\n[1/7] init...")
    rc = cmd_init(args)
    if rc != 0:
        print("init failed — aborting.")
        return rc

    # Step 2: discover
    if args.skip_discover:
        print("\n[2/7] discover... (skipped)")
        rc = 0
    else:
        print("\n[2/7] discover...")
        disc_args = copy.copy(args)
        disc_args.func = None
        rc = cmd_discover(disc_args)
        if rc != 0:
            print("discover failed — aborting.")
            return rc

    # Step 3: crawl
    if args.skip_crawl:
        print("\n[3/7] crawl... (skipped)")
        rc = 0
    elif args.urls or args.url_file:
        print("\n[3/7] crawl (manual URLs)...")
        crawl_args = copy.copy(args)
        crawl_args.func = None
        rc = cmd_crawl(crawl_args)
    else:
        print("\n[3/7] crawl...")
        candidate_file = output / "review" / "candidate-articles.json"
        if candidate_file.exists():
            data = json.loads(candidate_file.read_text(encoding="utf-8"))
            candidates = data if isinstance(data, list) else data.get("candidates", [])
            urls = [c["url"] for c in candidates]
            crawl_args = copy.copy(args)
            crawl_args.func = None
            crawl_args.urls = urls
            crawl_args.url_file = None
            rc = cmd_crawl(crawl_args)
        else:
            print("No candidate file found — skipping crawl.")
            rc = 0

    if rc != 0:
        print("crawl had failures — continuing with validate.")

    # Step 4: validate
    print("\n[4/7] validate...")
    val_args = copy.copy(args)
    val_args.func = None
    val_args.reclassify = True
    rc = cmd_validate(val_args)
    if rc != 0:
        print("validate had issues — continuing.")

    # Step 5: ingest (prepare extraction prompts)
    print("\n[5/7] ingest (prepare)...")
    if args.dry_run:
        print("Skipping ingest (dry-run mode).")
        rc = 0
    else:
        ing_args = copy.copy(args)
        ing_args.func = None
        ing_args.force = args.force
        ing_args.article_ids = None
        ing_args.prepare = True
        rc = cmd_ingest(ing_args)
        if rc != 0:
            print("ingest prepare had issues — continuing.")

    # Step 6: extract — Claude Code processes .prompt.md files
    # (handled by the /zoomkb:build skill command in SKILL.md)
    print("\n[6/7] extract... (Claude Code processes extraction-queue/*.prompt.md)")

    # Step 7: ingest (commit results to wiki)
    print("\n[7/7] ingest (commit)...")
    if args.dry_run:
        print("Skipping commit (dry-run mode).")
        rc = 0
    else:
        ing_args = copy.copy(args)
        ing_args.func = None
        ing_args.force = False
        ing_args.article_ids = None
        ing_args.prepare = False
        ing_args.commit = True
        rc = cmd_ingest(ing_args)
        if rc != 0:
            print("ingest commit had issues — continuing.")

    # Step 8: lint
    print("\nLint...")
    rc = cmd_lint(args)

    print("\n" + "=" * 50)
    print("Build complete.")
    print(f"Output: {output}")
    print("=" * 50)
    return rc


def cmd_build_all(args: argparse.Namespace) -> int:
    """Initialize KB directories for all supported Zoom product lines."""
    print("=" * 50)
    print("zoomkb:build-all — multi-product setup")
    print("=" * 50)
    print(f"\nProducts: {', '.join(ALL_PRODUCTS)}\n")

    results: list[tuple[str, int, str]] = []

    for product in ALL_PRODUCTS:
        print(f"\n{'─' * 40}")
        print(f"[{product}] init...")

        init_args = copy.copy(args)
        init_args.product = product
        init_args.output = ""
        init_args.func = None

        rc = cmd_init(init_args)
        output_dir = _default_output(product)
        results.append((product, rc, output_dir))

        if rc != 0:
            print(f"[{product}] init FAILED")
        else:
            print(f"[{product}] init OK → {output_dir}")

    # Summary
    print("\n" + "=" * 50)
    print("build-all summary")
    print("=" * 50)
    ok = sum(1 for _, rc, _ in results if rc == 0)
    fail = sum(1 for _, rc, _ in results if rc != 0)
    print(f"  OK: {ok}, Failed: {fail}")
    for product, rc, output_dir in results:
        status = "OK" if rc == 0 else "FAIL"
        print(f"  [{status}] {product} → {output_dir}")

    return 0 if fail == 0 else 1


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="zoomkb", description="Zoom Support KB Builder")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    sub = parser.add_subparsers(dest="command", required=True)

    # discover
    p_disc = sub.add_parser("discover", help="Discover candidate articles from sitemaps")
    p_disc.add_argument("--product", default="Zoom Phone", help="Target product")
    p_disc.add_argument("--source-root", default="https://support.zoom.com/hc/en", help="Zoom Support root URL")
    p_disc.add_argument("--output", default="", help="KB output directory (default: derived from --product)")
    p_disc.add_argument("--fetch-titles", action="store_true", help="Fetch page titles for better filtering")
    p_disc.add_argument("--max-workers", type=int, default=5, help="Parallel title fetch workers (default: 5)")
    p_disc.add_argument("--max-candidates", type=int, default=0, help="Stop after N candidates (0 = no limit)")
    p_disc.add_argument("--locale", default="en", help="Filter by language path, e.g. 'en'. Use '' for all (default: en)")
    p_disc.set_defaults(func=cmd_discover)

    # init
    p_init = sub.add_parser("init", help="Initialize KB directory structure")
    p_init.add_argument("--product", default="Zoom Phone", help="Target product")
    p_init.add_argument("--output", default="", help="Output directory (default: derived from --product)")
    p_init.set_defaults(func=cmd_init)

    # crawl
    p_crawl = sub.add_parser("crawl", help="Crawl seed URLs")
    p_crawl.add_argument("--urls", nargs="+", help="Space-separated URLs")
    p_crawl.add_argument("--url-file", help="File containing one URL per line")
    p_crawl.add_argument("--output", default="./zoom-phone-kb", help="KB output directory")
    p_crawl.set_defaults(func=cmd_crawl)

    # validate
    p_val = sub.add_parser("validate", help="Validate raw articles")
    p_val.add_argument("--output", default="./zoom-phone-kb", help="KB output directory")
    p_val.add_argument("--reclassify", action="store_true", help="Re-run classification")
    p_val.set_defaults(func=cmd_validate)

    # ingest
    p_ing = sub.add_parser("ingest", help="Ingest raw articles into wiki (prepare → Claude extract → commit)")
    p_ing.add_argument("--output", default="./zoom-phone-kb", help="KB output directory")
    p_ing.add_argument("--prepare", action="store_true", help="Step 1: write extraction prompt files to extraction-queue/")
    p_ing.add_argument("--commit", action="store_true", help="Step 3: read .result.json files and write wiki pages")
    p_ing.add_argument("--force", action="store_true", help="Re-process already ingested articles")
    p_ing.add_argument("--dry-run", action="store_true", help="Preview what would be prepared")
    p_ing.add_argument("--article-ids", nargs="+", help="Process specific articles by ID")
    p_ing.add_argument("--min-sources", type=int, default=2, help="Minimum source articles per wiki entity (default: 2)")
    p_ing.add_argument("--min-quality", type=float, default=20.0, help="Minimum entity quality score 0-100 (default: 20)")
    p_ing.set_defaults(func=cmd_ingest)

    # lint
    p_lint = sub.add_parser("lint", help="Lint KB for quality, consistency, and completeness")
    p_lint.add_argument("--output", default="./zoom-phone-kb", help="KB output directory")
    p_lint.add_argument("--stale-days", type=int, default=30, help="Days after which content is considered stale (default: 30)")
    p_lint.add_argument("--strict", action="store_true", help="Exit non-zero on any issue")
    p_lint.set_defaults(func=cmd_lint)

    # extract step is handled by Claude Code (see SKILL.md /zoomkb:build)
    # The CLI no longer includes a separate extract command since Claude Code
    # reads .prompt.md files and writes .result.json files directly.

    # refresh
    p_refresh = sub.add_parser("refresh", help="Re-crawl accepted articles, diff content hashes, detect changes")
    p_refresh.add_argument("--output", default="./zoom-phone-kb", help="KB output directory")
    p_refresh.add_argument("--article-ids", nargs="+", help="Refresh specific articles")
    p_refresh.add_argument("--force", action="store_true", help="Force refresh even if recently checked")
    p_refresh.add_argument("--max-workers", type=int, default=3, help="Parallel workers (default: 3)")
    p_refresh.add_argument("--stale-days", type=int, default=30, help="Days after which unreachable source is stale (default: 30)")
    p_refresh.set_defaults(func=cmd_refresh)

    # freshness
    p_fresh = sub.add_parser("freshness", help="Generate source freshness report")
    p_fresh.add_argument("--output", default="./zoom-phone-kb", help="KB output directory")
    p_fresh.add_argument("--stale-days", type=int, default=30, help="Days after which content is considered stale (default: 30)")
    p_fresh.set_defaults(func=cmd_freshness)

    # build
    p_build = sub.add_parser("build", help="One-shot full pipeline: init → discover → crawl → validate → ingest-prepare → ingest-commit → lint")
    p_build.add_argument("--product", default="Zoom Phone", help="Target product")
    p_build.add_argument("--source-root", default="https://support.zoom.com/hc/en", help="Zoom Support root URL")
    p_build.add_argument("--output", default="", help="KB output directory (default: derived from --product)")
    p_build.add_argument("--fetch-titles", action="store_true", help="Fetch page titles for better filtering")
    p_build.add_argument("--max-workers", type=int, default=5, help="Parallel title fetch workers (default: 5)")
    p_build.add_argument("--max-candidates", type=int, default=0, help="Stop after N candidates (0 = no limit)")
    p_build.add_argument("--locale", default="en", help="Filter by language path (default: en)")
    p_build.add_argument("--urls", nargs="+", help="Override: space-separated URLs to crawl instead of discover results")
    p_build.add_argument("--url-file", help="Override: file containing URLs to crawl instead of discover results")
    p_build.add_argument("--dry-run", action="store_true", help="Preview without calling LLM ingest")
    p_build.add_argument("--force", action="store_true", help="Re-ingest already processed articles")
    p_build.add_argument("--stale-days", type=int, default=30, help="Days after which content is considered stale (default: 30)")
    p_build.add_argument("--strict", action="store_true", help="Exit non-zero on lint issues")
    p_build.add_argument("--skip-discover", action="store_true", help="Skip discovery, use existing candidate URLs")
    p_build.add_argument("--skip-crawl", action="store_true", help="Skip crawl, use existing raw articles")
    p_build.add_argument("--min-sources", type=int, default=2, help="Minimum source articles per wiki entity (default: 2)")
    p_build.add_argument("--min-quality", type=float, default=20.0, help="Minimum entity quality score 0-100 (default: 20)")
    p_build.set_defaults(func=cmd_build)

    # build-all
    p_ball = sub.add_parser("build-all", help="Initialize KB directories for all supported Zoom product lines")
    p_ball.set_defaults(func=cmd_build_all)

    args = parser.parse_args(argv)
    _setup_logging(args.verbose)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
