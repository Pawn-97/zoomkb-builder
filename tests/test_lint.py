"""Tests for zoomkb.lint module — regression test for issue counting."""

import json
from pathlib import Path
from zoomkb.lint import lint


def _setup_kb(output_dir: Path, articles: list[dict]):
    """Create a minimal KB structure for lint testing."""
    wiki_dir = output_dir / "wiki"
    wiki_dir.mkdir(parents=True)
    for d in ["concepts", "user-roles", "task-flows", "constraints", "ux-patterns"]:
        (wiki_dir / d).mkdir(exist_ok=True)

    # Minimal index.md to avoid "index.md missing" navigation issue
    (wiki_dir / "index.md").write_text("# Test KB Index\n\nThis is a minimal index for lint testing.\n")

    raw_dir = output_dir / "raw" / "support-articles"
    raw_dir.mkdir(parents=True)

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps({"articles": articles}))


class TestIssueCounting:
    """Informational messages must not count as issues."""

    def test_positive_coverage_message_not_counted_as_issue(self, tmp_path):
        """'All high-confidence articles have been ingested.' must not make lint FAIL."""
        _setup_kb(tmp_path, [
            {
                "article_id": "KB0012345",
                "title": "Test Article",
                "confidence": "high",
                "status": "accepted",
                "ingested_at": "2026-05-17T00:00:00Z",
            }
        ])

        report = lint(tmp_path, strict=False)
        assert report["total_issues"] == 0
        assert report["passed"] is True

    def test_actual_issue_still_counted(self, tmp_path):
        """Real issues must still be counted."""
        _setup_kb(tmp_path, [
            {
                "article_id": "KB0012345",
                "title": "Test Article",
                "confidence": "high",
                "status": "accepted",
            }
        ])

        report = lint(tmp_path, strict=False)
        assert report["total_issues"] == 1
        assert report["passed"] is False
        assert "not yet ingested" in report["coverage"][0]

    def test_no_articles_in_manifest_not_counted(self, tmp_path):
        """'No articles in manifest' is informational, not an issue."""
        _setup_kb(tmp_path, [])

        report = lint(tmp_path, strict=False)
        assert report["total_issues"] == 0
        assert report["passed"] is True

    def test_strict_mode_sets_exit_code(self, tmp_path):
        """When strict and an issue exists, exit_code = 1."""
        _setup_kb(tmp_path, [
            {
                "article_id": "KB0012345",
                "title": "Test Article",
                "confidence": "high",
                "status": "accepted",
            }
        ])

        report = lint(tmp_path, strict=True)
        assert report["exit_code"] == 1

    def test_raw_orphan_files_count_as_coverage_issue(self, tmp_path):
        """Raw article files outside the manifest indicate contaminated source data."""
        _setup_kb(tmp_path, [
            {
                "article_id": "KB0012345",
                "title": "Test Article",
                "confidence": "high",
                "status": "accepted",
                "ingested_at": "2026-05-17T00:00:00Z",
                "local_path": "raw/support-articles/KB0012345-test.md",
            }
        ])

        raw_dir = tmp_path / "raw" / "support-articles"
        (raw_dir / "KB0012345-test.md").write_text(
            "---\narticle_id: KB0012345\n---\nExpected article.\n",
            encoding="utf-8",
        )
        (raw_dir / "KB0099999-zoom-phone-leftover.md").write_text(
            "---\narticle_id: KB0099999\n---\nWrong product leftover.\n",
            encoding="utf-8",
        )

        report = lint(tmp_path, strict=False)

        assert report["passed"] is False
        assert any("not referenced by manifest" in issue for issue in report["coverage"])
