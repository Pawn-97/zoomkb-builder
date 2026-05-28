# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Zoom Support KB Builder — Python CLI + Claude Code skill that crawls Zoom Support Center articles and transforms them into a design-facing wiki (concepts, user-roles, task-flows, constraints, ux-patterns).

## Dev environment

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

After editable install, the `zoomkb` console script is on PATH (see `[project.scripts]` in `pyproject.toml`). The `PYTHONPATH=src .venv/bin/python3 src/zoomkb/cli.py …` form is the fallback when running without install.

Python 3.9+ required at runtime; `mypy` config targets 3.11.

## Run tests

```bash
.venv/bin/python3 -m pytest tests/ -v
```

Single test: `.venv/bin/python3 -m pytest tests/test_ingest.py::test_dedup_by_normalized_slug -v`
Suite is 54 tests across `test_ingest.py`, `test_lint.py`, `test_validator.py`, `test_ux_partner_integration.py`.

## Architecture

**Two-layer KB design.** Every KB output dir has:
- `raw/support-articles/*.md` — verbatim crawl output, never LLM-rewritten. Source of truth.
- `wiki/{concepts,user-roles,task-flows,constraints,ux-patterns}/*.md` — extracted, deduped, quality-filtered pages with `source_article_ids` traceability.
- `manifest.json` — per-article status (discovered → crawled → accepted → ingested), hashes, classification scores.
- `extraction-queue/*.prompt.md` + `*.result.json` — handoff files between Python and Claude (see below).

**Pipeline.** `discover → crawl → classify → validate → ingest-prepare → extract → ingest-commit → lint`. The `cmd_build` function in `src/zoomkb/cli.py` runs all stages end-to-end.

**The extraction handshake (critical).** The `ingest` step is split into three parts because Claude Code does the LLM work — there is no external API:
1. `zoomkb ingest --prepare` — Python groups accepted articles by entity and writes `extraction-queue/*.prompt.md`.
2. **Claude Code** reads each prompt and writes a sibling `*.result.json` containing extracted entities.
3. `zoomkb ingest --commit` — Python reads results, runs three-stage dedup (exact slug → normalized slug → title Jaccard similarity), filters by `--min-sources` and `--min-quality`, writes markdown to `wiki/`.

`cmd_build` orchestrates this: it pauses after `--prepare`, expects results to exist before `--commit`. When running the full pipeline as a slash command, Claude is the one filling in step 2.

**Module map** (`src/zoomkb/`):
- `cli.py` — argparse entry, `cmd_*` functions per subcommand, plus `cmd_build` / `cmd_build_all` orchestrators.
- `discover.py` — sitemap-based candidate URL discovery.
- `crawler.py` — JSON-LD primary, Trafilatura fallback, optional `crawl4ai` headless browser behind `ZOOMKB_CRAWL4AI=1`.
- `classifier.py` — rule-based relevance scoring against `constants.PRODUCT_ALIASES`; optional LLM refinement behind `ZOOMKB_LLM_CLASSIFIER=1` (needs `pip install openai` + `OPENAI_API_KEY`).
- `validator.py` — frontmatter / content-quality checks, duplicate detection.
- `ingest.py` — prompt generation, result parsing, three-stage dedup, wiki page writing.
- `lint.py` — six checks: traceability, coverage, consistency, freshness, navigation, quality.
- `refresh.py` — re-crawl accepted articles, detect drift via hash compare, generate freshness reports.
- `manifest.py` — JSON read/write helpers for the per-KB manifest.
- `constants.py` — `PRODUCT_ALIASES` table driving classification.

**Claude Code skill (`SKILL.md`).** Exposes three user-facing actions: create KB (`/zoomkb:build`), update KB (`/zoomkb:refresh`), and validate quality (`/zoomkb:lint`). Other CLI subcommands exist for internal orchestration and debugging; do not promote them as primary skill commands. Detailed reference docs live in `references/cli-reference.md`, `references/architecture.md`, `references/ux-partner-integration.md`.

**Cursor compatibility.** `.cursor/rules/zoomkb.mdc` mirrors the project-critical guidance for Cursor agents. `.cursor/rules/neat-freak.mdc` loads the cleanup workflow when a user asks to sync, tidy, or hand off the project. Keep those rules concise and update them when project invariants change.

## Key conventions

- Product keys are kebab-cased slugs. Six supported: `zoom-phone`, `zoom-contact-center`, `zoom-clips`, `zoom-meetings`, `zoom-rooms`, `shared-zoom-platform`. `PRODUCT_ALIASES` in `constants.py` is the authoritative list — add new products there.
- Default KB output directory is `./{product-slug}-kb/` (e.g. `./zoom-phone-kb/`). The `--output` flag overrides.
- Discovery writes review artifacts to `review/candidate-articles.json` and `review/rejected-articles.json`; do not look for them at the KB root.
- `raw/` is append-only and never edited by LLM. Quality issues are filtered at validate / ingest time, not by rewriting source.
- Wiki entities must carry `source_article_ids` frontmatter — `_check_traceability` in `lint.py` will fail otherwise.
- Slugs are produced by `_slugify` + `_normalize_slug` in `ingest.py`; dedup relies on this canonical form, so don't bypass it when adding new entity writers.
- `docs/ideas/` and `docs/reports/` contain historical planning and validation notes, not implementation truth. Prefer `README.md`, this file, and `references/*.md` for current behavior.

## Environment variables

All optional:
- `ZOOMKB_CRAWL4AI=1` — enable headless-browser fallback for JS-rendered pages.
- `ZOOMKB_LLM_CLASSIFIER=1` — turn on LLM classification refinement (rule-based is default).
- `ZOOMKB_LLM_MODEL` — model override for LLM classifier (default `gpt-4o-mini`).
- `OPENAI_API_KEY` — required only when `ZOOMKB_LLM_CLASSIFIER=1`.

The extraction step does **not** need an API key — it runs inside Claude Code.
