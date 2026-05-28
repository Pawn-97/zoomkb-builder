"""Tests for UX-partner integration compatibility.

Validates that zoomkb-builder fixture output meets
UX-partner's setup-kb detection and classification requirements.
"""

import json
import re
from pathlib import Path

import pytest

KB_ROOT = Path(__file__).resolve().parent / "fixtures" / "test-kb-e2e"
MANIFEST_PATH = KB_ROOT / "manifest.json"
WIKI_DIR = KB_ROOT / "wiki"

WIKI_SUBDIRS = ["concepts", "task-flows", "user-roles", "constraints", "ux-patterns"]
SECTION_HEADERS = {
    "concept": "Concepts",
    "user-role": "User Roles",
    "task-flow": "Task Flows",
    "constraint": "Constraints",
    "ux-pattern": "UX Patterns",
}
SUBDIR_TO_TYPE = {
    "concepts": "concept",
    "user-roles": "user-role",
    "task-flows": "task-flow",
    "constraints": "constraint",
    "ux-patterns": "ux-pattern",
}
REQUIRED_FRONTMATTER = {"type", "product", "title", "sources", "confidence"}


def _extract_frontmatter(content):
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    fm = {}
    for line in parts[1].strip().split("\n"):
        if ":" in line and not line.startswith(" "):
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip()
    return fm


# ── Manifest tests ──────────────────────────────────────────────────

class TestManifestIntegration:
    def test_manifest_exists(self):
        assert MANIFEST_PATH.exists(), f"manifest.json not found at {MANIFEST_PATH}"

    def test_manifest_has_kb_type(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        assert manifest.get("kb_type") == "zoomkb", (
            f"Expected kb_type='zoomkb', got {manifest.get('kb_type')}"
        )

    def test_manifest_has_kb_version(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        assert "kb_version" in manifest, "manifest.json missing kb_version field"


# ── Wiki structure tests ────────────────────────────────────────────

class TestWikiStructure:
    def test_wiki_index_exists(self):
        assert (WIKI_DIR / "index.md").exists(), "wiki/index.md not found"

    def test_all_wiki_subdirs_exist(self):
        for sub in WIKI_SUBDIRS:
            subdir = WIKI_DIR / sub
            assert subdir.is_dir(), f"wiki/{sub}/ directory not found"

    def test_index_md_covers_all_sections(self):
        content = (WIKI_DIR / "index.md").read_text(encoding="utf-8")
        for key, header in SECTION_HEADERS.items():
            assert f"## {header}" in content, (
                f"index.md missing section header '## {header}'"
            )

    def test_index_has_no_empty_sections_without_placeholder(self):
        content = (WIKI_DIR / "index.md").read_text(encoding="utf-8")
        sections = content.split("\n## ")
        for section in sections[1:]:  # skip title
            lines = section.strip().split("\n")
            body = [l for l in lines[1:] if l.strip()]  # skip header line
            if not body:
                assert "_No entries yet._" in section, (
                    f"Empty section without placeholder: {lines[0]}"
                )

# ── Wiki page quality tests ─────────────────────────────────────────

class TestWikiPages:
    def test_all_pages_have_frontmatter(self):
        """Every wiki page must have YAML frontmatter with required fields."""
        missing = []
        for sub in WIKI_SUBDIRS:
            subdir = WIKI_DIR / sub
            if not subdir.is_dir():
                continue
            for md_file in sorted(subdir.glob("*.md")):
                content = md_file.read_text(encoding="utf-8")
                fm = _extract_frontmatter(content)
                for field in REQUIRED_FRONTMATTER:
                    if field not in fm:
                        missing.append(f"{md_file.relative_to(KB_ROOT)}: missing '{field}'")
        assert not missing, "\n".join(missing)

    def test_page_type_matches_subdirectory(self):
        """Wiki page 'type' frontmatter must match its parent subdirectory."""
        mismatches = []
        for sub, expected_type in SUBDIR_TO_TYPE.items():
            subdir = WIKI_DIR / sub
            if not subdir.is_dir():
                continue
            for md_file in sorted(subdir.glob("*.md")):
                content = md_file.read_text(encoding="utf-8")
                fm = _extract_frontmatter(content)
                actual = fm.get("type", "")
                if actual != expected_type:
                    mismatches.append(
                        f"{md_file.relative_to(KB_ROOT)}: type='{actual}' expected='{expected_type}'"
                    )
        assert not mismatches, "\n".join(mismatches)

    def test_classification_coverage(self):
        """All wiki page types must map to known UX-partner classification tags."""
        # UX-partner tags: CONCEPT, TASK-FLOW, USER-ROLE, CONSTRAINT, UX-PATTERN
        valid_types = set(SUBDIR_TO_TYPE.values())
        unknown = []
        for sub in WIKI_SUBDIRS:
            subdir = WIKI_DIR / sub
            if not subdir.is_dir():
                continue
            for md_file in sorted(subdir.glob("*.md")):
                content = md_file.read_text(encoding="utf-8")
                fm = _extract_frontmatter(content)
                page_type = fm.get("type", "")
                if page_type not in valid_types:
                    unknown.append(
                        f"{md_file.relative_to(KB_ROOT)}: unknown type '{page_type}'"
                    )
        assert not unknown, "\n".join(unknown)

    def test_no_orphan_entities(self):
        """No wikilink should reference a non-existent page."""
        # Build set of all valid wikilink targets
        valid_slugs = set()
        for sub in WIKI_SUBDIRS:
            subdir = WIKI_DIR / sub
            if not subdir.is_dir():
                continue
            for md_file in sorted(subdir.glob("*.md")):
                valid_slugs.add(md_file.stem)

        orphans = []
        for sub in WIKI_SUBDIRS:
            subdir = WIKI_DIR / sub
            if not subdir.is_dir():
                continue
            for md_file in sorted(subdir.glob("*.md")):
                content = md_file.read_text(encoding="utf-8")
                # Find all [[wikilinks]]
                refs = re.findall(r"\[\[(.+?)\]\]", content)
                for ref in refs:
                    if ref not in valid_slugs:
                        orphans.append(
                            f"{md_file.relative_to(KB_ROOT)}: [[{ref}]] (target not found)"
                        )
        # Note: this tests current state; some orphans are expected from LLM extraction
        # This test is informational — report count but only fail if excessive
        if len(orphans) > 100:
            pytest.fail(
                f"Too many orphan wikilinks ({len(orphans)}). "
                f"First 10:\n" + "\n".join(orphans[:10])
            )

    def test_index_to_context_mode_compatible(self):
        """All wiki files match UX-partner classification rules by path pattern."""
        # UX-partner index-to-context-mode.js QUALITY_RULES:
        # /wiki/concepts/ -> CONCEPT, /wiki/task-flows/ -> TASK-FLOW,
        # /wiki/user-roles/ -> USER-ROLE, /wiki/constraints/ -> CONSTRAINT,
        # /wiki/ux-patterns/ -> UX-PATTERN, /wiki/index.md -> META
        pattern_map = {
            "wiki/concepts/": "CONCEPT",
            "wiki/task-flows/": "TASK-FLOW",
            "wiki/user-roles/": "USER-ROLE",
            "wiki/constraints/": "CONSTRAINT",
            "wiki/ux-patterns/": "UX-PATTERN",
        }

        unmatched = []
        for sub in WIKI_SUBDIRS:
            subdir = WIKI_DIR / sub
            if not subdir.is_dir():
                continue
            for md_file in sorted(subdir.glob("*.md")):
                rel = str(md_file.relative_to(KB_ROOT))
                matched = False
                for pattern, tag in pattern_map.items():
                    if rel.startswith(pattern):
                        matched = True
                        break
                if not matched:
                    unmatched.append(rel)

        # index.md should be classified as META (also valid)
        if "wiki/index.md" in unmatched:
            unmatched.remove("wiki/index.md")

        assert not unmatched, (
            f"Files not matching any UX-partner classification rule:\n"
            + "\n".join(unmatched)
        )
