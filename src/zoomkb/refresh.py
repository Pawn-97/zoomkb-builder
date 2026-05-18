"""Refresh: re-crawl accepted articles, diff content hashes, detect staleness."""

import hashlib
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

from zoomkb.crawler import crawl_article
from zoomkb.manifest import load_manifest, save_manifest

logger = logging.getLogger("zoomkb.refresh")


def _compute_hash(content: str) -> str:
    return "sha256:" + hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def _refresh_one(
    article: dict,
    raw_dir: Path,
    stale_days: int,
    force: bool,
) -> dict:
    """Refresh single article. Returns result dict."""
    aid = article["article_id"]
    source_url = article.get("source_url", "")
    old_hash = article.get("content_hash", "")

    if not source_url:
        return {"article_id": aid, "status": "error", "error": "No source_url"}

    # Check if already checked recently
    last_checked = article.get("last_checked_at", "")
    if last_checked and not force:
        try:
            lc = datetime.fromisoformat(last_checked)
            if (datetime.now(timezone.utc) - lc) < timedelta(hours=1):
                return {"article_id": aid, "status": "skipped", "reason": "Recently checked"}
        except ValueError:
            pass

    try:
        meta = crawl_article(source_url, raw_dir, product=article.get("product", ""))
        new_hash = meta.get("content_hash", "")

        if not new_hash:
            return {"article_id": aid, "status": "error", "error": "Empty content from crawl"}

        result: dict[str, Any] = {
            "article_id": aid,
            "title": article.get("title", ""),
            "old_hash": old_hash,
            "new_hash": new_hash,
            "last_checked_at": datetime.now(timezone.utc).isoformat(),
        }

        if old_hash and old_hash != new_hash:
            result["status"] = "changed"
            result["previous_hash"] = old_hash
        else:
            result["status"] = "unchanged"

        return result

    except Exception as e:
        logger.error("Refresh failed for %s: %s", aid, e)
        cutoff = datetime.now(timezone.utc) - timedelta(days=stale_days)
        captured = article.get("captured_at", "")
        is_stale = False
        if captured:
            try:
                cap_date = datetime.fromisoformat(captured)
                if cap_date < cutoff:
                    is_stale = True
            except ValueError:
                pass
        return {
            "article_id": aid,
            "status": "stale" if is_stale else "error",
            "error": str(e),
        }


def refresh_articles(
    manifest_path: Path,
    raw_dir: Path,
    product: str = "",
    article_ids: Optional[list[str]] = None,
    force: bool = False,
    max_workers: int = 3,
    stale_days: int = 30,
) -> dict:
    """Re-crawl accepted articles, diff hashes, update manifest.

    Returns stats dict. Writes refresh-report.md.
    """
    manifest = load_manifest(manifest_path)
    articles = manifest.get("articles", [])
    output_dir = manifest_path.parent

    # Filter to accepted articles
    candidates = [a for a in articles if a.get("status") == "accepted"]
    if article_ids:
        candidates = [a for a in candidates if a["article_id"] in article_ids]

    if not candidates:
        logger.info("No accepted articles to refresh")
        return {"total": 0, "checked": 0, "changed": 0, "unchanged": 0, "stale": 0, "errors": 0}

    stats: dict[str, int] = {
        "total": len(candidates),
        "changed": 0,
        "unchanged": 0,
        "stale": 0,
        "errors": 0,
        "skipped": 0,
    }

    results: list[dict] = []
    changed_articles: list[dict] = []
    stale_articles: list[dict] = []
    error_articles: list[dict] = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(_refresh_one, a, raw_dir, stale_days, force): a["article_id"]
            for a in candidates
        }
        for future in as_completed(futures):
            try:
                result = future.result()
            except Exception as e:
                aid = futures[future]
                result = {"article_id": aid, "status": "error", "error": str(e)}

            results.append(result)
            status = result["status"]
            if status in stats:
                stats[status] += 1

            # Update article in manifest
            aid = result["article_id"]
            for a in articles:
                if a["article_id"] == aid:
                    a["last_checked_at"] = result.get("last_checked_at", a.get("last_checked_at", ""))
                    if status == "changed":
                        a["previous_hash"] = result.get("old_hash", "")
                        a["content_hash"] = result.get("new_hash", "")
                        a["status"] = "review"
                        changed_articles.append(result)
                    elif status == "stale":
                        a["stale"] = True
                        stale_articles.append(result)
                    elif status == "error":
                        error_articles.append(result)
                    break

    save_manifest(manifest_path, manifest)

    _write_refresh_report(output_dir, stats, changed_articles, stale_articles, error_articles)

    logger.info(
        "Refresh done: %d total, %d changed, %d unchanged, %d stale, %d errors",
        stats["total"], stats["changed"], stats["unchanged"], stats["stale"], stats["errors"],
    )
    return stats


def _write_refresh_report(
    output_dir: Path,
    stats: dict,
    changed: list[dict],
    stale: list[dict],
    errors: list[dict],
) -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "# Refresh Report",
        "",
        f"_Generated: {today}_",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total | {stats['total']} |",
        f"| Changed | {stats['changed']} |",
        f"| Unchanged | {stats['unchanged']} |",
        f"| Stale | {stats['stale']} |",
        f"| Errors | {stats['errors']} |",
        f"| Skipped | {stats.get('skipped', 0)} |",
        "",
    ]

    if changed:
        lines.extend([
            "## Changed Articles",
            "",
            "These articles have changed since last crawl and need review:",
            "",
            "| Article ID | Title | Old Hash | New Hash |",
            "|------------|-------|----------|----------|",
        ])
        for r in changed:
            lines.append(
                f"| {r['article_id']} | {r.get('title', '')} | {r.get('old_hash', '')[:18]} | {r.get('new_hash', '')[:18]} |"
            )
        lines.append("")

    if stale:
        lines.extend([
            "## Stale Articles",
            "",
            "These articles could not be reached during refresh:",
            "",
        ])
        for r in stale:
            lines.append(f"- **{r['article_id']}**: {r.get('error', 'Unreachable')}")
        lines.append("")

    if errors:
        lines.extend([
            "## Errors",
            "",
        ])
        for r in errors:
            lines.append(f"- **{r['article_id']}**: {r.get('error', 'Unknown error')}")
        lines.append("")

    (output_dir / "refresh-report.md").write_text("\n".join(lines), encoding="utf-8")
    logger.info("Generated refresh-report.md")


def generate_freshness_report(
    manifest_path: Path,
    stale_days: int = 30,
) -> dict:
    """Generate a comprehensive source freshness report.

    Returns report dict with sections: summary, stale_articles, review_queue, freshness_distribution.
    Writes freshness-report.md.
    """
    manifest = load_manifest(manifest_path)
    articles = manifest.get("articles", [])
    output_dir = manifest_path.parent
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=stale_days)

    # Classify each article by freshness
    fresh: list[dict] = []
    stale: list[dict] = []
    review: list[dict] = []

    for a in articles:
        recorded = False
        last_checked = a.get("last_checked_at", "")
        captured = a.get("captured_at", "")

        if a.get("status") == "review":
            review.append(a)
            continue

        check_date = last_checked or captured
        if check_date:
            try:
                cd = datetime.fromisoformat(check_date)
                if cd < cutoff:
                    stale.append(a)
                    recorded = True
            except ValueError:
                pass

        if not recorded and a.get("status") != "review":
            fresh.append(a)

    # Build report
    today = now.strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "# Freshness Report",
        "",
        f"_Generated: {today}_",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total articles | {len(articles)} |",
        f"| Fresh (checked within {stale_days}d) | {len(fresh)} |",
        f"| Stale (not checked in {stale_days}+d) | {len(stale)} |",
        f"| Review queue | {len(review)} |",
        "",
    ]

    if stale:
        lines.extend([
            "## Stale Articles",
            "",
            "| Article ID | Title | Status | Last Checked |",
            "|------------|-------|--------|-------------|",
        ])
        for a in stale:
            last = a.get("last_checked_at") or a.get("captured_at", "N/A")
            lines.append(
                f"| {a['article_id']} | {a.get('title', '')} | {a.get('status', '')} | {last} |"
            )
        lines.append("")

    if review:
        lines.extend([
            "## Review Queue",
            "",
            "Articles needing human review (status=review or changed after refresh):",
            "",
            "| Article ID | Title | Confidence | Previous Status |",
            "|------------|-------|------------|----------------|",
        ])
        for a in review:
            lines.append(
                f"| {a['article_id']} | {a.get('title', '')} | {a.get('confidence', '')} | {a.get('previous_hash', 'N/A')[:18]} |"
            )
        lines.append("")

    lines.extend([
        "## All Articles",
        "",
        "| Article ID | Title | Status | Confidence | Captured | Last Checked |",
        "|------------|-------|--------|------------|----------|-------------|",
    ])
    for a in articles:
        lines.append(
            f"| {a['article_id']} | {a.get('title', '')} | {a.get('status', '')} | {a.get('confidence', '')} | {a.get('captured_at', 'N/A')[:10]} | {a.get('last_checked_at', 'N/A')[:10]} |"
        )

    (output_dir / "freshness-report.md").write_text("\n".join(lines), encoding="utf-8")
    logger.info("Generated freshness-report.md")

    return {
        "total": len(articles),
        "fresh": len(fresh),
        "stale": len(stale),
        "review": len(review),
        "stale_days": stale_days,
    }
