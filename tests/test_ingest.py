"""Tests for zoomkb.ingest module."""

import json
from pathlib import Path
from zoomkb.ingest import (
    _slugify,
    _normalize_slug,
    _dedup_entities,
    _score_entity,
    _merge_entities,
    WikiEntity,
    parse_extraction_result,
    commit_extraction,
)


def make_entity(
    entity_type="concept",
    title="Test Entity",
    slug=None,
    summary="A test entity.",
    key_points=None,
    related=None,
    sources=None,
):
    if sources is None:
        sources = [{"article_id": "KB0012345", "title": "Source Article"}]
    return WikiEntity(
        type=entity_type,
        title=title,
        slug=slug or _slugify(title),
        summary=summary,
        key_points=key_points or [],
        related=related or [],
        sources=sources,
    )


class TestSlugify:
    def test_simple_title(self):
        assert _slugify("Getting Started with Zoom Phone") == "getting-started-with-zoom-phone"

    def test_special_characters_removed(self):
        assert _slugify("How to: Set up & configure") == "how-to-set-up-configure"

    def test_multiple_spaces_and_dashes(self):
        slug = _slugify("Call  queues --  overview")
        assert "--" not in slug

    def test_unicode_latin_only(self):
        slug = _slugify("Déploiement des téléphones")
        assert all(c.isascii() or c == "-" for c in slug)


class TestNormalizeSlug:
    def test_plural_stripped(self):
        assert _normalize_slug("call-queues") == "call-queue"

    def test_non_plural_unchanged(self):
        assert _normalize_slug("call-queue") == "call-queue"

    def test_double_s_preserved(self):
        result = _normalize_slug("wireless")
        assert result == "wireless"

    def test_empty_after_strip_returns_original(self):
        assert _normalize_slug("s") == "s"


class TestScoreEntity:
    def test_high_quality_score(self):
        entity = make_entity(
            summary="A comprehensive guide to setting up and configuring Zoom Phone for enterprise.",
            key_points=["Point 1", "Point 2", "Point 3", "Point 4", "Point 5"],
            sources=[{"article_id": "KB001"}, {"article_id": "KB002"}, {"article_id": "KB003"}],
        )
        score = _score_entity(entity)
        assert score >= 60

    def test_low_quality_score(self):
        entity = make_entity(
            summary="Short summary.",
            key_points=[],
            sources=[{"article_id": "KB001"}],
        )
        score = _score_entity(entity)
        assert score < 60

    def test_empty_summary_handled(self):
        entity = make_entity(summary="")
        score = _score_entity(entity)
        assert score >= 0


class TestDedupEntities:
    def test_exact_slug_match_merged(self):
        entities = [
            make_entity(slug="call-queue", title="Call Queue", summary="A call queue."),
            make_entity(slug="call-queue", title="Call Queue Overview", summary="Overview of call queues."),
        ]
        result = _dedup_entities(entities)
        assert len(result) == 1
        assert result[0].summary == "Overview of call queues."

    def test_normalized_slug_match_merged(self):
        entities = [
            make_entity(slug="call-queues", title="Call Queues"),
            make_entity(slug="call-queue", title="Call Queue"),
        ]
        result = _dedup_entities(entities)
        assert len(result) == 1

    def test_unique_entities_preserved(self):
        entities = [
            make_entity(slug="call-queue", title="Call Queue"),
            make_entity(slug="auto-receptionist", title="Auto Receptionist"),
            make_entity(slug="phone-number", title="Phone Number"),
        ]
        result = _dedup_entities(entities)
        assert len(result) == 3

    def test_empty_list(self):
        assert _dedup_entities([]) == []

    def test_single_entity(self):
        entities = [make_entity()]
        result = _dedup_entities(entities)
        assert len(result) == 1

    def test_sources_merged_correctly(self):
        entities = [
            make_entity(
                slug="call-queue", title="Call Queue",
                sources=[{"article_id": "KB001", "title": "Article 1"}],
            ),
            make_entity(
                slug="call-queue", title="Call Queue",
                sources=[{"article_id": "KB002", "title": "Article 2"}],
            ),
        ]
        result = _dedup_entities(entities)
        assert len(result) == 1
        source_ids = [s["article_id"] for s in result[0].sources]
        assert "KB001" in source_ids
        assert "KB002" in source_ids


class TestMergeEntities:
    def test_sources_combined(self):
        a = make_entity(sources=[{"article_id": "KB001", "title": "A"}])
        b = make_entity(sources=[{"article_id": "KB002", "title": "B"}])
        _merge_entities(a, b)
        assert len(a.sources) == 2

    def test_duplicate_source_not_added(self):
        a = make_entity(sources=[{"article_id": "KB001", "title": "A"}])
        b = make_entity(sources=[{"article_id": "KB001", "title": "A"}])
        _merge_entities(a, b)
        assert len(a.sources) == 1

    def test_longer_summary_kept(self):
        a = make_entity(summary="Short")
        b = make_entity(summary="A much longer summary with more detail.")
        _merge_entities(a, b)
        assert a.summary == "A much longer summary with more detail."

    def test_key_points_combined(self):
        a = make_entity(key_points=["Point A"])
        b = make_entity(key_points=["Point B", "Point A"])
        _merge_entities(a, b)
        assert len(a.key_points) == 2


class TestParseExtractionResult:
    def test_valid_json_parsed(self, tmp_path):
        result_path = tmp_path / "KB001.result.json"
        data = {
            "article_id": "KB001",
            "concepts": [
                {"title": "Call Queue", "summary": "A call queue.", "key_points": ["P1"], "related": []}
            ],
        }
        result_path.write_text(json.dumps(data))
        result = parse_extraction_result(result_path, article_id="KB001")
        assert len(result.entities) == 1
        assert result.entities[0].title == "Call Queue"

    def test_non_json_raises(self, tmp_path):
        result_path = tmp_path / "KB001.result.json"
        result_path.write_text("not valid json")
        import json as _json
        import pytest
        with pytest.raises(_json.JSONDecodeError):
            parse_extraction_result(result_path, article_id="KB001")

    def test_missing_file_raises(self, tmp_path):
        import pytest
        with pytest.raises(FileNotFoundError):
            parse_extraction_result(tmp_path / "nonexistent.json", article_id="KB001")


class TestCommitExtraction:
    def test_min_sources_filter(self, tmp_path):
        """Entities with < min_sources should be filtered out."""
        import os
        output_dir = tmp_path / "test-kb"
        output_dir.mkdir()

        wiki_dir = output_dir / "wiki"
        wiki_dir.mkdir()
        for d in ["concepts", "user-roles", "task-flows", "constraints", "ux-patterns"]:
            (wiki_dir / d).mkdir()

        raw_dir = output_dir / "raw" / "support-articles"
        raw_dir.mkdir(parents=True)

        # Manifest with 3 accepted articles
        manifest = {
            "articles": [
                {"article_id": "KB001", "title": "Article 1", "confidence": "high", "status": "accepted"},
                {"article_id": "KB002", "title": "Article 2", "confidence": "high", "status": "accepted"},
                {"article_id": "KB003", "title": "Article 3", "confidence": "high", "status": "accepted"},
            ]
        }
        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest))

        # Extraction results — same entity from 2 articles, third article creates different entity
        extraction_dir = output_dir / "extraction-queue"
        extraction_dir.mkdir()

        for i, aid in enumerate(["KB001", "KB002"]):
            data = {
                "article_id": aid,
                "concepts": [
                    {"title": "Call Queue", "summary": "A call queue for routing calls to agents.",
                     "key_points": ["Routes calls", "Configurable"], "related": []}
                ],
            }
            (extraction_dir / f"{aid}.result.json").write_text(json.dumps(data))

        # KB003: different entity
        data3 = {
            "article_id": "KB003",
            "concepts": [
                {"title": "Obscure Setting", "summary": "x",
                 "key_points": [], "related": []}
            ],
        }
        (extraction_dir / "KB003.result.json").write_text(json.dumps(data3))

        # Also create raw files (commit_extraction checks for source titles)
        for aid in ["KB001", "KB002", "KB003"]:
            raw_file = raw_dir / f"{aid}-test.md"
            raw_file.write_text("---\ntitle: Test\n---\nTest content.")

        # Commit with min_sources=2: "Call Queue" (2 sources) survives, "Obscure Setting" (1 source) filtered
        stats = commit_extraction(
            manifest_path=manifest_path,
            raw_dir=raw_dir,
            wiki_dir=wiki_dir,
            min_sources=2,
            min_quality=0,
        )

        # Call Queue should be created (has 2 sources)
        # Obscure Setting should be filtered (has 1 source)
        assert stats["entities_created"] == 1
        assert stats["entities_filtered"] >= 1

        concept_page = wiki_dir / "concepts" / "call-queue.md"
        content = concept_page.read_text(encoding="utf-8")
        assert "primary_category:" in content
        assert "source_article_ids:" in content
        assert "## Product context" in content
        assert "## UX implications" in content

        assert (output_dir / "10-LLM-Wiki" / "Master Index.md").exists()
        assert (output_dir / "10-LLM-Wiki" / "Taxonomy.md").exists()
        assert (output_dir / "10-LLM-Wiki" / "Full Category Listings.md").exists()
        assert (output_dir / "10-LLM-Wiki" / "Feature Cross References.md").exists()
        assert list((output_dir / "10-LLM-Wiki" / "Category Pages").glob("*.md"))
        assert (output_dir / "30-Agent-Playbooks" / "Troubleshooting" / "Product Business Domains.md").exists()
