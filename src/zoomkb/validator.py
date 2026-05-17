"""Validate extracted articles for quality, completeness, and duplicates."""

import logging
from dataclasses import dataclass
from pathlib import Path

from zoomkb.constants import MIN_BODY_LENGTH, MIN_WORD_COUNT

logger = logging.getLogger("zoomkb.validator")


@dataclass(frozen=True)
class ValidationResult:
    passed: bool
    errors: list[str]
    warnings: list[str]


def validate_article(article) -> ValidationResult:
    """Validate a single extracted article. Raises ValueError on critical issues."""
    errors: list[str] = []
    warnings: list[str] = []

    # Critical: body must exist and be substantial
    if not article.body or len(article.body) < MIN_BODY_LENGTH:
        errors.append(f"Body too short: {len(article.body or '')} chars (min {MIN_BODY_LENGTH})")

    if article.word_count < MIN_WORD_COUNT:
        errors.append(f"Word count too low: {article.word_count} (min {MIN_WORD_COUNT})")

    # Critical: must have article_id
    if article.article_id == "unknown":
        errors.append("Missing article_id (sysparm_article not found in URL)")

    # Critical: must have title
    if not article.title or article.title == article.article_id:
        warnings.append("Title missing or same as article_id")

    # Warnings
    if article.extraction_method == "trafilatura":
        warnings.append("Used trafilatura fallback (JSON-LD unavailable)")
    elif article.extraction_method == "crawl4ai":
        warnings.append("Used crawl4ai fallback (JSON-LD and trafilatura failed)")

    if errors:
        raise ValueError(f"Validation failed for {article.source_url}: {'; '.join(errors)}")

    if warnings:
        logger.warning("Warnings for %s: %s", article.article_id, warnings)

    return ValidationResult(passed=True, errors=errors, warnings=warnings)


def check_duplicates(manifest_path: Path, content_hash: str, article_id: str) -> bool:
    """Check if article already exists in manifest by hash or ID."""
    from zoomkb.manifest import load_manifest

    if not manifest_path.exists():
        return False

    manifest = load_manifest(manifest_path)
    for article in manifest.get("articles", []):
        if article.get("article_id") == article_id:
            return True
        if article.get("content_hash") == content_hash:
            return True
    return False
