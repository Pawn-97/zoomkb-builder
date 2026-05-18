"""Manifest management: read, write, update article registry."""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger("zoomkb.manifest")


def init_manifest(product: str, output_dir: Path) -> Path:
    """Create or update manifest.json. Preserves existing articles if manifest already exists."""
    path = output_dir / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        manifest = load_manifest(path)
        manifest["product"] = manifest.get("product", product)
        manifest["generated_at"] = datetime.now(timezone.utc).isoformat()
        if "stats" not in manifest:
            manifest["stats"] = {"total": 0, "accepted": 0, "review": 0, "rejected": 0}
        save_manifest(path, manifest)
        logger.info("Updated existing manifest at %s", path)
    else:
        manifest = {
            "product": product,
            "source_root": "https://support.zoom.com/hc/en",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "articles": [],
            "stats": {
                "total": 0,
                "accepted": 0,
                "review": 0,
                "rejected": 0,
            },
        }
        path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        logger.info("Created manifest at %s", path)
    return path


def load_manifest(path: Path) -> dict:
    """Load manifest from disk."""
    return json.loads(path.read_text(encoding="utf-8"))


def save_manifest(path: Path, manifest: dict) -> None:
    """Save manifest to disk."""
    manifest["generated_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def add_article(manifest_path: Path, article_meta: dict) -> None:
    """Add or update an article in manifest."""
    manifest = load_manifest(manifest_path)
    articles = manifest["articles"]

    # Update existing or append
    existing = next(
        (a for a in articles if a["article_id"] == article_meta["article_id"]),
        None,
    )
    if existing:
        existing.update(article_meta)
        existing["last_checked_at"] = datetime.now(timezone.utc).isoformat()
    else:
        article_meta["captured_at"] = datetime.now(timezone.utc).isoformat()
        article_meta["last_checked_at"] = article_meta["captured_at"]
        articles.append(article_meta)

    # Recompute stats
    stats = {"total": 0, "accepted": 0, "review": 0, "rejected": 0}
    for a in articles:
        stats["total"] += 1
        status = a.get("status", "review")
        if status in stats:
            stats[status] += 1
    manifest["stats"] = stats

    save_manifest(manifest_path, manifest)
    logger.info(
        "Manifest updated: %d total, %d accepted, %d review, %d rejected",
        stats["total"], stats["accepted"], stats["review"], stats["rejected"],
    )
