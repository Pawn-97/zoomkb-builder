# CLAUDE.md

## Project

Zoom Support KB Builder — CLI tool + Claude Code skill that crawls Zoom Support Center articles and transforms them into structured, design-facing knowledge bases (wiki layer).

## Dev environment

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Run tests

```bash
.venv/bin/python3 -m pytest tests/ -v
```

## Run CLI directly (dev)

```bash
PYTHONPATH=src .venv/bin/python3 src/zoomkb/cli.py <command> [args]
```

## Architecture

- `src/zoomkb/` — Python package (cli, discover, crawler, classifier, ingest, lint, validator, manifest, refresh)
- `SKILL.md` — Claude Code skill definition, maps slash commands to CLI
- `tests/` — pytest suite (54 tests: ingest, lint, validator, UX-partner integration)
- Two-layer design: `raw/` (never LLM-rewritten) → `wiki/` (Claude Code extracted, deduped, quality filtered)

## Key conventions

- Python 3.9+ required. Use `.venv` at project root.
- All CLI commands run via `PYTHONPATH=src .venv/bin/python3 src/zoomkb/cli.py`
- Extraction step (ingest) uses Claude Code directly — no external API required
- Rule-based classifier is default; optional LLM classifier behind `ZOOMKB_LLM_CLASSIFIER=1`
- Product keys are kebab-cased slugs: `zoom-phone`, `zoom-contact-center`, etc.
