"""Generate design-facing navigation and troubleshooting layers for a KB."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from zoomkb.taxonomy import (
    DEFAULT_TAXONOMY,
    category_filename,
    categorize_text,
    get_category,
)


WIKI_SUBDIR_TO_TYPE = {
    "concepts": "concept",
    "user-roles": "user-role",
    "task-flows": "task-flow",
    "constraints": "constraint",
    "ux-patterns": "ux-pattern",
}


def _product_name(product: str) -> str:
    return product.replace("-", " ").title()


def _extract_frontmatter(content: str) -> tuple[dict[str, str], str, str]:
    if not content.startswith("---"):
        return {}, "", content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, "", content
    fm_text = parts[1]
    fm: dict[str, str] = {}
    for line in fm_text.strip().split("\n"):
        if ":" in line and not line.startswith(" "):
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip()
    return fm, fm_text, parts[2].strip()


def _frontmatter_list(fm_text: str, key: str) -> list[str]:
    values: list[str] = []
    in_key = False
    for line in fm_text.splitlines():
        stripped = line.strip()
        if stripped == f"{key}:":
            in_key = True
            continue
        if in_key:
            if line and not line.startswith(" "):
                break
            if stripped.startswith("- "):
                values.append(stripped[2:].strip().strip('"'))
    return values


def _h1_title(body: str, fallback: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def _wiki_page_records(wiki_dir: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for subdir_name, entity_type in WIKI_SUBDIR_TO_TYPE.items():
        subdir = wiki_dir / subdir_name
        if not subdir.exists():
            continue
        for path in sorted(subdir.glob("*.md")):
            content = path.read_text(encoding="utf-8")
            fm, fm_text, body = _extract_frontmatter(content)
            title = fm.get("title") or _h1_title(body, path.stem.replace("-", " ").title())
            category = fm.get("primary_category") or categorize_text(title, body[:2000])
            source_ids = _frontmatter_list(fm_text, "source_article_ids")
            if not source_ids:
                source_ids = re.findall(r"article_id:\s*([A-Za-z0-9_-]+)", fm_text)
            records.append({
                "title": title,
                "slug": path.stem,
                "type": fm.get("type", entity_type),
                "subdir": subdir_name,
                "path": path,
                "relative_path": path.relative_to(wiki_dir.parent),
                "category": category,
                "source_article_ids": sorted(set(source_ids)),
                "links": sorted(set(re.findall(r"\[\[(.+?)\]\]", body))),
                "body": body,
            })
    return records


def _article_records(
    output_dir: Path,
    raw_dir: Path,
    manifest: dict[str, Any],
) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for article in manifest.get("articles", []):
        article_id = article.get("article_id", "")
        local_path = article.get("local_path", "")
        raw_path = output_dir / local_path if local_path else None
        if (not raw_path or not raw_path.exists()) and article_id:
            matches = sorted(raw_dir.glob(f"{article_id}*.md"))
            raw_path = matches[0] if matches else None

        title = article.get("title", article_id)
        body_sample = ""
        source_url = article.get("source_url", "")
        if raw_path and raw_path.exists():
            content = raw_path.read_text(encoding="utf-8")
            fm, _, body = _extract_frontmatter(content)
            title = fm.get("title", title)
            source_url = fm.get("source_url", source_url)
            body_sample = body[:2000]

        records.append({
            "article_id": article_id,
            "title": title,
            "status": article.get("status", ""),
            "confidence": article.get("confidence", ""),
            "raw_path": str(raw_path.relative_to(output_dir)) if raw_path and raw_path.exists() else local_path,
            "source_url": source_url,
            "category": categorize_text(title, source_url, body_sample),
        })
    return records


def _entity_link(record: dict[str, Any], prefix: str = "../") -> str:
    return f"[{record['title']}]({prefix}{record['relative_path']})"


def _article_link(record: dict[str, str], prefix: str = "../") -> str:
    raw_path = record.get("raw_path", "")
    if raw_path:
        return f"[{record['title']}]({prefix}{raw_path})"
    return record["title"]


def generate_knowledge_navigation(
    output_dir: Path,
    wiki_dir: Path,
    raw_dir: Path,
    manifest: dict[str, Any],
    product: str,
) -> None:
    """Write the 10-LLM-Wiki and 30-Agent-Playbooks layers."""
    nav_dir = output_dir / "10-LLM-Wiki"
    category_dir = nav_dir / "Category Pages"
    playbook_dir = output_dir / "30-Agent-Playbooks" / "Troubleshooting"
    category_dir.mkdir(parents=True, exist_ok=True)
    playbook_dir.mkdir(parents=True, exist_ok=True)

    entity_records = _wiki_page_records(wiki_dir)
    article_records = _article_records(output_dir, raw_dir, manifest)

    _write_taxonomy(nav_dir, product, article_records, entity_records)
    _write_master_index(nav_dir, product, entity_records)
    _write_full_category_listings(nav_dir, product, article_records)
    _write_feature_cross_refs(nav_dir, product, entity_records)
    _write_category_pages(category_dir, product, article_records, entity_records)
    _write_playbooks(playbook_dir, product, article_records, entity_records)


def _write_taxonomy(
    nav_dir: Path,
    product: str,
    article_records: list[dict[str, str]],
    entity_records: list[dict[str, Any]],
) -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        f"# {_product_name(product)} Taxonomy",
        "",
        f"_Last updated: {today}_",
        "",
        "This taxonomy is product-agnostic. It keeps every Zoom product KB organized by user task and design risk, not by extraction artifact type.",
        "",
        "| Category | What It Covers | Articles | Wiki Pages | UX Use |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for category in DEFAULT_TAXONOMY:
        article_count = sum(1 for r in article_records if r["category"] == category.title)
        entity_count = sum(1 for r in entity_records if r["category"] == category.title)
        ux_use = "; ".join(category.design_scenarios[:2])
        lines.append(
            f"| {category.title} | {category.definition} | {article_count} | {entity_count} | {ux_use} |"
        )

    lines.extend([
        "",
        "## Classification Rules",
        "",
        "- Every accepted article should map to one primary category.",
        "- Every wiki page should declare `primary_category` in frontmatter.",
        "- Do not merge heterogeneous sources into a generic product page when a narrower category exists.",
        "- Use secondary links and cross references to express relationships across categories.",
        "",
    ])
    (nav_dir / "Taxonomy.md").write_text("\n".join(lines), encoding="utf-8")


def _write_master_index(
    nav_dir: Path,
    product: str,
    entity_records: list[dict[str, Any]],
) -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    task_flows = [r for r in entity_records if r["type"] == "task-flow"]
    constraints = [r for r in entity_records if r["type"] == "constraint"]
    concepts = [r for r in entity_records if r["type"] == "concept"]
    troubleshooting = [
        r for r in entity_records
        if r["category"] == "09 Monitoring, Logs & Troubleshooting"
        or re.search(r"troubleshoot|error|fail|cannot|unable|log|alert", r["title"], re.I)
    ]

    lines = [
        f"# {_product_name(product)} Master Index",
        "",
        f"_Last updated: {today}_",
        "",
        "Use this page as the human entry point into the KB. Start from product category when you need breadth; start from task flows, constraints, or troubleshooting when you already know the user problem.",
        "",
        "## Category Overview",
        "",
    ]
    for category in DEFAULT_TAXONOMY:
        filename = category_filename(category.title)
        count = sum(1 for r in entity_records if r["category"] == category.title)
        lines.append(f"- [{category.title}](Category%20Pages/{filename.replace(' ', '%20')}) - {category.definition} ({count} wiki pages)")

    lines.extend(["", "## Concept Index", ""])
    if concepts:
        for record in concepts[:50]:
            lines.append(f"- {_entity_link(record)} - {record['category']}")
    else:
        lines.append("_No concept pages yet._")

    lines.extend(["", "## Top Task Flows", ""])
    if task_flows:
        for record in task_flows[:25]:
            lines.append(f"- {_entity_link(record)} - {record['category']}")
    else:
        lines.append("_No task-flow pages yet._")

    lines.extend(["", "## High-Risk Constraints", ""])
    if constraints:
        for record in constraints[:25]:
            lines.append(f"- {_entity_link(record)} - {record['category']}")
    else:
        lines.append("_No constraint pages yet._")

    lines.extend(["", "## Troubleshooting Entry Points", ""])
    if troubleshooting:
        for record in troubleshooting[:25]:
            lines.append(f"- {_entity_link(record)} - {record['category']}")
    else:
        lines.append("- [Troubleshooting Playbooks](../30-Agent-Playbooks/Troubleshooting/Product%20Business%20Domains.md)")

    lines.extend([
        "",
        "## Core Navigation Files",
        "",
        "- [Taxonomy](Taxonomy.md)",
        "- [Full Category Listings](Full%20Category%20Listings.md)",
        "- [Feature Cross References](Feature%20Cross%20References.md)",
        "",
    ])
    (nav_dir / "Master Index.md").write_text("\n".join(lines), encoding="utf-8")


def _write_full_category_listings(
    nav_dir: Path,
    product: str,
    article_records: list[dict[str, str]],
) -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        f"# {_product_name(product)} Full Category Listings",
        "",
        f"_Last updated: {today}_",
        "",
        "Every manifest article appears here so a raw source can be found from the navigation layer without browsing `raw/` directly.",
        "",
    ]
    for category in DEFAULT_TAXONOMY:
        rows = [r for r in article_records if r["category"] == category.title]
        lines.extend([f"## {category.title}", "", category.definition, ""])
        if not rows:
            lines.append("_No articles classified here yet._")
        else:
            lines.extend(["| Article | Article ID | Status | Confidence | Raw Path |", "| --- | --- | --- | --- | --- |"])
            for record in rows:
                lines.append(
                    f"| {_article_link(record)} | {record['article_id']} | {record['status']} | {record['confidence']} | `{record['raw_path']}` |"
                )
        lines.append("")
    (nav_dir / "Full Category Listings.md").write_text("\n".join(lines), encoding="utf-8")


def _relationship_type(source: dict[str, Any], target: dict[str, Any]) -> str:
    if target["type"] == "constraint":
        return "constrained_by"
    if source["type"] == "constraint":
        return "affects"
    if target["type"] == "task-flow":
        return "unlocks_or_guides"
    if source["category"] == target["category"]:
        return "shares_surface_with"
    return "related_dependency"


def _write_feature_cross_refs(
    nav_dir: Path,
    product: str,
    entity_records: list[dict[str, Any]],
) -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    by_slug = {r["slug"]: r for r in entity_records}
    rows: list[tuple[dict[str, Any], dict[str, Any], str]] = []

    for record in entity_records:
        for link in record["links"]:
            target = by_slug.get(link)
            if target and target["slug"] != record["slug"]:
                rows.append((record, target, _relationship_type(record, target)))

    # Add same-category constraint/task-flow relationships even when the LLM did not link them.
    constraints = [r for r in entity_records if r["type"] == "constraint"]
    flows = [r for r in entity_records if r["type"] == "task-flow"]
    for constraint in constraints:
        for flow in flows:
            if constraint["category"] == flow["category"]:
                rows.append((flow, constraint, "constrained_by"))

    seen: set[tuple[str, str, str]] = set()
    unique_rows: list[tuple[dict[str, Any], dict[str, Any], str]] = []
    for source, target, relation in rows:
        key = (source["slug"], target["slug"], relation)
        if key not in seen:
            unique_rows.append((source, target, relation))
            seen.add(key)

    lines = [
        f"# {_product_name(product)} Feature Cross References",
        "",
        f"_Last updated: {today}_",
        "",
        "Use this file to answer: if this feature changes, what concepts, tasks, constraints, and surfaces might be affected?",
        "",
        "| Source | Target | Relationship | Design Impact |",
        "| --- | --- | --- | --- |",
    ]
    if unique_rows:
        for source, target, relation in unique_rows[:200]:
            impact = (
                f"Changes to {source['title']} may alter {target['title']} expectations, "
                f"especially within {source['category']}."
            )
            lines.append(f"| {_entity_link(source)} | {_entity_link(target)} | {relation} | {impact} |")
    else:
        lines.append("| _No linked features yet_ | _No linked features yet_ | _pending_ | Add related links during extraction so impact analysis can be generated. |")

    lines.extend([
        "",
        "## Relationship Types",
        "",
        "- `depends_on`: one feature cannot work without another.",
        "- `unlocks_or_guides`: a task flow teaches or enables a feature.",
        "- `constrained_by`: a requirement, license, setting, or platform rule gates behavior.",
        "- `shares_surface_with`: features compete for or coexist on the same user surface.",
        "- `affects`: a constraint or policy changes the visible behavior of another entity.",
        "",
    ])
    (nav_dir / "Feature Cross References.md").write_text("\n".join(lines), encoding="utf-8")


def _write_category_pages(
    category_dir: Path,
    product: str,
    article_records: list[dict[str, str]],
    entity_records: list[dict[str, Any]],
) -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for category in DEFAULT_TAXONOMY:
        articles = [r for r in article_records if r["category"] == category.title]
        entities = [r for r in entity_records if r["category"] == category.title]
        concepts = [r for r in entities if r["type"] == "concept"]
        constraints = [r for r in entities if r["type"] == "constraint"]
        flows = [r for r in entities if r["type"] == "task-flow"]

        lines = [
            f"# {category.title}",
            "",
            f"_Product: {_product_name(product)} - Last updated: {today}_",
            "",
            "## Category Definition",
            "",
            category.definition,
            "",
            "## Applicable Users / Roles",
            "",
            *[f"- {user}" for user in category.users],
            "",
            "## Typical Tasks",
            "",
            *[f"- {task}" for task in category.tasks],
            "",
            "## Design Scenarios",
            "",
            *[f"- {scenario}" for scenario in category.design_scenarios],
            "",
            "## Document List",
            "",
        ]
        if articles:
            for record in articles[:100]:
                lines.append(f"- {_article_link(record, prefix='../../')} (`{record['article_id']}`)")
        else:
            lines.append("_No raw articles classified here yet._")

        lines.extend(["", "## Key Concepts", ""])
        if concepts:
            for record in concepts[:40]:
                lines.append(f"- {_entity_link(record, prefix='../../')}")
        else:
            lines.append("_No concept pages yet._")

        lines.extend(["", "## Key Constraints", ""])
        if constraints:
            for record in constraints[:40]:
                lines.append(f"- {_entity_link(record, prefix='../../')}")
        else:
            for failure in category.failure_states:
                lines.append(f"- {failure}")

        lines.extend(["", "## Common Failure States", ""])
        for failure in category.failure_states:
            lines.append(f"- {failure}")

        lines.extend(["", "## Related Task Flows", ""])
        if flows:
            for record in flows[:40]:
                lines.append(f"- {_entity_link(record, prefix='../../')}")
        else:
            lines.append("_No task-flow pages yet._")

        lines.extend(["", "## Related Categories", ""])
        for other in DEFAULT_TAXONOMY:
            if other.title != category.title and set(other.users) & set(category.users):
                filename = category_filename(other.title).replace(" ", "%20")
                lines.append(f"- [{other.title}]({filename})")

        (category_dir / category_filename(category.title)).write_text("\n".join(lines), encoding="utf-8")


def _troubleshooting_articles(article_records: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        r for r in article_records
        if r["category"] == "09 Monitoring, Logs & Troubleshooting"
        or re.search(r"troubleshoot|issue|error|cannot|unable|fail|offline|logs|alert", r["title"], re.I)
    ]


def _write_playbooks(
    playbook_dir: Path,
    product: str,
    article_records: list[dict[str, str]],
    entity_records: list[dict[str, Any]],
) -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    troubleshooting_articles = _troubleshooting_articles(article_records)

    overview = [
        f"# {_product_name(product)} Troubleshooting Business Domains",
        "",
        f"_Last updated: {today}_",
        "",
        "Use these playbooks to translate user symptom language into evidence collection, likely root cause domains, and affected UX/product areas.",
        "",
        "| Domain | When to Use | Related Sources |",
        "| --- | --- | ---: |",
    ]
    for category in DEFAULT_TAXONOMY:
        count = sum(1 for r in troubleshooting_articles if r["category"] == category.title)
        overview.append(f"| {category.title} | {'; '.join(category.failure_states)} | {count} |")
    overview.append("")
    (playbook_dir / "Product Business Domains.md").write_text("\n".join(overview), encoding="utf-8")

    priority_categories = [
        "09 Monitoring, Logs & Troubleshooting",
        "01 Getting Started & Deployment",
        "04 Devices, Clients & Surfaces",
        "07 Integrations & Interop",
        "08 Requirements, Licenses & Platform Support",
        "06 Admin, Roles & Policy",
    ]

    for category_title in priority_categories:
        category = get_category(category_title)
        articles = [r for r in troubleshooting_articles if r["category"] == category.title]
        entities = [r for r in entity_records if r["category"] == category.title]
        short_title = re.sub(r"^[0-9]+\s+", "", category.title)
        filename = f"Root Cause {short_title.replace('&', 'and')}.md"
        filename = re.sub(r"[^A-Za-z0-9 .&-]+", "", filename)
        lines = [
            f"# Root Cause: {short_title}",
            "",
            f"_Product: {_product_name(product)} - Last updated: {today}_",
            "",
            "## When to Use",
            "",
            category.definition,
            "",
            "## User Symptom Language",
            "",
            "| User says | Likely domain |",
            "| --- | --- |",
        ]
        if articles:
            for record in articles[:10]:
                lines.append(f"| {record['title']} | {category.title} |")
        else:
            for failure in category.failure_states:
                lines.append(f"| {failure} | {category.title} |")

        lines.extend([
            "",
            "## Required Inputs",
            "",
            "- User role and affected account or workspace.",
            "- Surface or client where the symptom appears.",
            "- Exact error, unavailable state, or missing affordance.",
            "- Relevant license, policy, integration, or version context.",
            "",
            "## First Checks",
            "",
            *[f"- Verify {task.lower()}." for task in category.tasks[:3]],
            "",
            "## Evidence Map",
            "",
            "- Raw source articles linked below are the authority for factual claims.",
            "- Wiki pages explain design-facing implications and related constraints.",
            "",
            "## Decision Tree",
            "",
            "1. Confirm the affected actor and surface.",
            "2. Check prerequisites, license, permission, and platform support.",
            "3. Validate integration or device state when the flow depends on external systems.",
            "4. Map the symptom to a task flow, constraint, or UX pattern before proposing product changes.",
            "",
            "## Common Root Causes",
            "",
            *[f"- {failure}" for failure in category.failure_states],
            "",
            "## What to Tell Support / PM / UX",
            "",
            "- Support needs the minimum evidence needed to reproduce and escalate.",
            "- PM needs to know whether the symptom is expected policy, missing configuration, or product gap.",
            "- UX needs the blocked state, recovery path, and dependency chain.",
            "",
            "## Related KB Pages",
            "",
        ])
        if entities:
            for record in entities[:20]:
                lines.append(f"- {_entity_link(record, prefix='../../')}")
        else:
            lines.append("_No wiki pages in this domain yet._")

        lines.extend(["", "## Related Raw Articles", ""])
        if articles:
            for record in articles[:20]:
                lines.append(f"- {_article_link(record, prefix='../../')} (`{record['article_id']}`)")
        else:
            lines.append("_No troubleshooting-specific raw articles classified here yet._")

        (playbook_dir / filename).write_text("\n".join(lines), encoding="utf-8")
