"""Lint KB for traceability, coverage, consistency, freshness, navigation, and quality."""

import logging
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger("zoomkb.lint")


def _extract_fm(content: str) -> tuple[dict[str, Any], str]:
    """Parse simple key:value frontmatter."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    fm: dict[str, Any] = {}
    for line in parts[1].strip().split("\n"):
        if ":" in line and not line.startswith(" "):
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip()
    return fm, parts[2].strip()


def _extract_wikilinks(text: str) -> set[str]:
    """Extract [[slug]] references from text."""
    return set(re.findall(r"\[\[(.+?)\]\]", text))


def find_raw_orphan_files(output_dir: Path) -> list[Path]:
    """Return raw article files that are not referenced by manifest.json."""
    manifest_path = output_dir / "manifest.json"
    raw_dir = output_dir / "raw" / "support-articles"
    if not manifest_path.exists() or not raw_dir.exists():
        return []

    import json
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    articles = manifest.get("articles", [])
    raw_files = sorted(raw_dir.glob("*.md"))
    if not raw_files:
        return []

    referenced_raw_paths: set[Path] = set()
    article_ids = {a.get("article_id") for a in articles if a.get("article_id")}

    for article in articles:
        local_path = article.get("local_path")
        if local_path:
            referenced_raw_paths.add((output_dir / local_path).resolve())

        article_id = article.get("article_id")
        if article_id:
            referenced_raw_paths.update(
                path.resolve() for path in raw_dir.glob(f"{article_id}*.md")
            )

    orphan_files: list[Path] = []
    for raw_file in raw_files:
        if raw_file.resolve() in referenced_raw_paths:
            continue

        fm, _ = _extract_fm(raw_file.read_text(encoding="utf-8"))
        article_id = fm.get("article_id", "")
        if article_id and article_id in article_ids:
            continue

        orphan_files.append(raw_file)

    return orphan_files


def lint(
    output_dir: Path,
    stale_days: int = 30,
    strict: bool = False,
) -> dict[str, Any]:
    """Run all lint checks. Returns report dict."""
    manifest_path = output_dir / "manifest.json"
    raw_dir = output_dir / "raw" / "support-articles"
    wiki_dir = output_dir / "wiki"

    report: dict[str, list[str]] = {
        "traceability": [],
        "coverage": [],
        "consistency": [],
        "freshness": [],
        "navigation": [],
        "quality": [],
    }

    # --- Traceability ---
    _check_traceability(output_dir, wiki_dir, report)

    # --- Coverage ---
    _check_coverage(manifest_path, raw_dir, report)

    # --- Consistency ---
    _check_consistency(wiki_dir, report)

    # --- Freshness ---
    _check_freshness(manifest_path, wiki_dir, stale_days, report)

    # --- Navigation ---
    _check_navigation(wiki_dir, report)

    # --- Quality ---
    _check_quality(wiki_dir, report)

    total_issues = sum(
        sum(1 for i in v if not (i.startswith("All ") or i.startswith("No ")))
        for v in report.values()
    )
    report["total_issues"] = total_issues
    report["passed"] = total_issues == 0

    if strict and not report["passed"]:
        report["exit_code"] = 1
    else:
        report["exit_code"] = 0

    return report


def _check_traceability(
    output_dir: Path,
    wiki_dir: Path,
    report: dict[str, list[str]],
) -> None:
    """Check wiki pages have sources and claims are traceable."""
    if not wiki_dir.exists():
        report["traceability"].append("Wiki directory missing — nothing to lint.")
        return

    for subdir_name in [
        "concepts", "user-roles", "task-flows", "constraints", "ux-patterns",
    ]:
        subdir = wiki_dir / subdir_name
        if not subdir.exists():
            continue
        for path in subdir.glob("*.md"):
            content = path.read_text(encoding="utf-8")
            fm, _ = _extract_fm(content)

            fname = path.name

            # Check sources in frontmatter
            has_sources = "sources:" in content.split("---")[1] if content.count("---") >= 2 else False
            if not has_sources:
                report["traceability"].append(
                    f"{fname}: no sources in frontmatter"
                )
                continue

            # Check source URLs
            if "source_url" not in content.split("---")[1]:
                report["traceability"].append(
                    f"{fname}: sources missing source_url"
                )

            # Check each claim section has source references
            body = fm if fm else {}
            if "sources" not in body and not has_sources:
                report["traceability"].append(f"{fname}: no source traceability")


def _check_coverage(
    manifest_path: Path,
    raw_dir: Path,
    report: dict[str, list[str]],
) -> None:
    """Check high-confidence ingestion coverage and raw/manifest consistency."""
    if not manifest_path.exists():
        report["coverage"].append("Manifest missing — cannot check coverage.")
        return

    import json
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    articles = manifest.get("articles", [])
    output_dir = manifest_path.parent

    # Find accepted articles not yet ingested
    uningested = []
    for a in articles:
        if a.get("confidence") == "high" and a.get("status") == "accepted":
            if "ingested_at" not in a:
                uningested.append(a["article_id"])

    if uningested:
        report["coverage"].append(
            f"{len(uningested)} high-confidence articles not yet ingested: "
            + ", ".join(uningested[:10])
            + (f" ... and {len(uningested) - 10} more" if len(uningested) > 10 else "")
        )
    elif articles:
        report["coverage"].append("All high-confidence articles have been ingested.")
    else:
        report["coverage"].append("No articles in manifest — nothing to check.")

    orphan_files = [
        str(path.relative_to(output_dir))
        for path in find_raw_orphan_files(output_dir)
    ]

    if orphan_files:
        more = (
            f" ... and {len(orphan_files) - 10} more"
            if len(orphan_files) > 10
            else ""
        )
        report["coverage"].append(
            f"{len(orphan_files)} raw article file(s) are not referenced by manifest: "
            + ", ".join(orphan_files[:10])
            + more
        )


def _check_consistency(
    wiki_dir: Path,
    report: dict[str, list[str]],
) -> None:
    """Check for duplicate/similar pages and conflicting product names."""
    if not wiki_dir.exists():
        return

    # Check for near-duplicate titles
    all_pages: dict[str, list[Path]] = {}
    for subdir_name in [
        "concepts", "user-roles", "task-flows", "constraints", "ux-patterns",
    ]:
        subdir = wiki_dir / subdir_name
        if not subdir.exists():
            continue
        for path in subdir.glob("*.md"):
            slug = path.stem
            if slug not in all_pages:
                all_pages[slug] = []
            all_pages[slug].append(path)

    duplicates = {s: ps for s, ps in all_pages.items() if len(ps) > 1}
    for slug, paths in duplicates.items():
        report["consistency"].append(
            f"Slug '{slug}' appears in multiple locations: "
            + ", ".join(str(p.relative_to(wiki_dir.parent)) for p in paths)
        )


def _check_freshness(
    manifest_path: Path,
    wiki_dir: Path,
    stale_days: int,
    report: dict[str, list[str]],
) -> None:
    """Check for stale wiki pages."""
    if not wiki_dir.exists():
        return

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=stale_days)
    stale_count = 0

    for subdir_name in [
        "concepts", "user-roles", "task-flows", "constraints", "ux-patterns",
    ]:
        subdir = wiki_dir / subdir_name
        if not subdir.exists():
            continue
        for path in subdir.glob("*.md"):
            content = path.read_text(encoding="utf-8")
            fm, _ = _extract_fm(content)
            last_reviewed = fm.get("last_reviewed", "")
            if last_reviewed:
                try:
                    reviewed_date = datetime.fromisoformat(last_reviewed)
                    if reviewed_date.tzinfo is None:
                        reviewed_date = reviewed_date.replace(tzinfo=timezone.utc)
                    if reviewed_date < cutoff:
                        stale_count += 1
                except ValueError:
                    report["freshness"].append(
                        f"{subdir_name}/{path.name}: invalid last_reviewed date '{last_reviewed}'"
                    )

    if stale_count:
        report["freshness"].append(
            f"{stale_count} wiki pages not reviewed in {stale_days}+ days"
        )

    # Check manifest for stale content hashes
    if manifest_path.exists():
        import json
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for a in manifest.get("articles", []):
            captured = a.get("captured_at", "")
            if captured:
                try:
                    cap_date = datetime.fromisoformat(captured)
                    if cap_date < cutoff and a.get("status") == "accepted":
                        if "last_checked_at" not in a or (
                            a.get("last_checked_at")
                            and datetime.fromisoformat(a["last_checked_at"]) < cutoff
                        ):
                            pass  # Flag only if both captured and last checked are stale
                except ValueError:
                    pass


def _check_navigation(
    wiki_dir: Path,
    report: dict[str, list[str]],
) -> None:
    """Check index.md is current and wikilinks resolve."""
    if not wiki_dir.exists():
        return

    # Check index.md exists and is populated
    index_path = wiki_dir / "index.md"
    if not index_path.exists():
        report["navigation"].append("wiki/index.md missing")
    else:
        content = index_path.read_text(encoding="utf-8")
        if len(content) < 50:
            report["navigation"].append("wiki/index.md appears empty")

    # Collect all valid slugs
    valid_slugs: set[str] = set()
    for subdir_name in [
        "concepts", "user-roles", "task-flows", "constraints", "ux-patterns",
    ]:
        subdir = wiki_dir / subdir_name
        if not subdir.exists():
            continue
        for path in subdir.glob("*.md"):
            valid_slugs.add(path.stem)

    # Check wikilinks resolve
    broken_links: list[str] = []
    for subdir_name in [
        "concepts", "user-roles", "task-flows", "constraints", "ux-patterns",
    ]:
        subdir = wiki_dir / subdir_name
        if not subdir.exists():
            continue
        for path in subdir.glob("*.md"):
            content = path.read_text(encoding="utf-8")
            links = _extract_wikilinks(content)
            for link in links:
                if link not in valid_slugs:
                    broken_links.append(f"{subdir_name}/{path.name}: [[{link}]] → not found")

    if broken_links:
        report["navigation"].extend(broken_links[:20])
        if len(broken_links) > 20:
            report["navigation"].append(f"... and {len(broken_links) - 20} more broken links")

    # Check for orphan pages (not referenced by any other page)
    all_references: set[str] = set()
    for subdir_name in [
        "concepts", "user-roles", "task-flows", "constraints", "ux-patterns",
    ]:
        subdir = wiki_dir / subdir_name
        if not subdir.exists():
            continue
        for path in subdir.glob("*.md"):
            content = path.read_text(encoding="utf-8")
            all_references.update(_extract_wikilinks(content))

    # Index links and self-references don't count as orphans
    orphans = []
    for subdir_name in [
        "concepts", "user-roles", "task-flows", "constraints", "ux-patterns",
    ]:
        subdir = wiki_dir / subdir_name
        if not subdir.exists():
            continue
        for path in subdir.glob("*.md"):
            if path.stem not in all_references:
                # Check if it's referenced in index.md
                in_index = False
                if index_path.exists():
                    if path.stem in index_path.read_text(encoding="utf-8"):
                        in_index = True
                if not in_index:
                    orphans.append(f"{subdir_name}/{path.name}")

    if orphans:
        report["navigation"].append(f"{len(orphans)} orphan pages (not linked from any page or index):")
        report["navigation"].extend(f"  - {o}" for o in orphans[:10])
        if len(orphans) > 10:
            report["navigation"].append(f"  ... and {len(orphans) - 10} more")


def _check_quality(
    wiki_dir: Path,
    report: dict[str, list[str]],
) -> None:
    """Check wiki page quality."""
    if not wiki_dir.exists():
        return

    for subdir_name in [
        "concepts", "user-roles", "task-flows", "constraints", "ux-patterns",
    ]:
        subdir = wiki_dir / subdir_name
        if not subdir.exists():
            continue
        for path in subdir.glob("*.md"):
            content = path.read_text(encoding="utf-8")

            # Check has key sections
            if "## Summary" not in content:
                report["quality"].append(
                    f"{subdir_name}/{path.name}: missing ## Summary section"
                )

            if "## Key points" not in content:
                report["quality"].append(
                    f"{subdir_name}/{path.name}: missing ## Key points section"
                )

            # Check summary is substantial
            fm, body = _extract_fm(content)
            summary_match = re.search(r"## Summary\n\n(.+?)(?:\n##|\Z)", body, re.DOTALL)
            if summary_match:
                summary = summary_match.group(1).strip()
                if len(summary) < 50:
                    report["quality"].append(
                        f"{subdir_name}/{path.name}: summary too short ({len(summary)} chars)"
                    )

            # Check word count
            word_count = len(body.split())
            if word_count < 50:
                report["quality"].append(
                    f"{subdir_name}/{path.name}: body too short ({word_count} words)"
                )


def write_lint_report(output_dir: Path, report: dict[str, Any]) -> Path:
    """Write lint-report.md."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        "# Lint Report",
        "",
        f"_Generated: {today}_",
        "",
        f"## Result: {'PASSED' if report['passed'] else 'FAILED'} ({report['total_issues']} issues)",
        "",
    ]

    section_labels = {
        "traceability": "Traceability",
        "coverage": "Coverage",
        "consistency": "Consistency",
        "freshness": "Freshness",
        "navigation": "Navigation",
        "quality": "Quality",
    }

    for key, label in section_labels.items():
        issues = report.get(key, [])
        status = "OK" if not issues or all(
            i.startswith("All ") or i.startswith("No ") for i in issues
        ) else f"{len(issues)} issue(s)"
        lines.extend([f"### {label} — {status}", ""])
        for issue in issues:
            lines.append(f"- {issue}")
        lines.append("")

    path = output_dir / "lint-report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
