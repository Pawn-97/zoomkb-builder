"""Tests for zoomkb.validator module."""

from dataclasses import dataclass
from pathlib import Path
import pytest
from zoomkb.validator import validate_article, check_duplicates, ValidationResult


@dataclass
class MockArticle:
    body: str
    word_count: int
    article_id: str
    title: str
    source_url: str = "https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0000001"
    extraction_method: str = "jsonld"


def make_article(body="x", word_count=0, article_id="unknown", title="Title", **kwargs):
    """Factory for MockArticle with reasonable defaults."""
    return MockArticle(body=body, word_count=word_count, article_id=article_id, title=title, **kwargs)


class TestValidateArticle:
    def test_valid_article_passes(self):
        article = make_article(
            body="A" * 500,
            word_count=200,
            article_id="KB0012345",
            title="Getting Started with Zoom Phone",
        )
        result = validate_article(article)
        assert result.passed is True

    def test_short_body_raises_value_error(self):
        article = make_article(body="short", word_count=200, article_id="KB0012345", title="T")
        with pytest.raises(ValueError, match="Body too short"):
            validate_article(article)

    def test_low_word_count_raises_value_error(self):
        article = make_article(body="A" * 500, word_count=10, article_id="KB0012345", title="T")
        with pytest.raises(ValueError, match="Word count too low"):
            validate_article(article)

    def test_missing_article_id_raises_value_error(self):
        article = make_article(body="A" * 500, word_count=200, title="Good Title")
        with pytest.raises(ValueError, match="Missing article_id"):
            validate_article(article)

    def test_missing_title_warns(self):
        article = make_article(
            body="A" * 500,
            word_count=200,
            article_id="KB0012345",
            title="KB0012345",  # same as article_id triggers warning
        )
        result = validate_article(article)
        assert result.passed is True
        assert any("Title missing" in w for w in result.warnings)

    def test_trafilatura_fallback_warns(self):
        article = make_article(
            body="A" * 500,
            word_count=200,
            article_id="KB0012345",
            title="Good Title",
            extraction_method="trafilatura",
        )
        result = validate_article(article)
        assert any("trafilatura fallback" in w for w in result.warnings)

    def test_multiple_errors_reported(self):
        article = make_article(body="", word_count=0, article_id="unknown", title="Title")
        with pytest.raises(ValueError) as exc:
            validate_article(article)
        assert "Body too short" in str(exc.value)
        assert "Word count too low" in str(exc.value)
        assert "Missing article_id" in str(exc.value)

    def test_empty_body_counted_as_zero(self):
        article = make_article(body="", word_count=200, article_id="KB0012345", title="T")
        with pytest.raises(ValueError, match="Body too short: 0 chars"):
            validate_article(article)

    def test_none_body_handled(self):
        article = make_article(body=None, word_count=200, article_id="KB0012345", title="T")
        with pytest.raises(ValueError, match="Body too short"):
            validate_article(article)


class TestCheckDuplicates:
    def test_no_manifest_returns_false(self, tmp_path):
        result = check_duplicates(
            manifest_path=tmp_path / "nonexistent.json",
            content_hash="abc123",
            article_id="KB0012345",
        )
        assert result is False

    def test_duplicate_by_id_detected(self, tmp_path):
        import json
        manifest_path = tmp_path / "manifest.json"
        manifest = {
            "articles": [
                {"article_id": "KB0012345", "content_hash": "hash1"},
            ]
        }
        manifest_path.write_text(json.dumps(manifest))
        result = check_duplicates(manifest_path, "hash2", "KB0012345")
        assert result is True

    def test_duplicate_by_hash_detected(self, tmp_path):
        import json
        manifest_path = tmp_path / "manifest.json"
        manifest = {
            "articles": [
                {"article_id": "KB0012345", "content_hash": "hash1"},
            ]
        }
        manifest_path.write_text(json.dumps(manifest))
        result = check_duplicates(manifest_path, "hash1", "KB0099999")
        assert result is True

    def test_unique_article_returns_false(self, tmp_path):
        import json
        manifest_path = tmp_path / "manifest.json"
        manifest = {"articles": [{"article_id": "KB0012345", "content_hash": "hash1"}]}
        manifest_path.write_text(json.dumps(manifest))
        result = check_duplicates(manifest_path, "hash2", "KB0099999")
        assert result is False
