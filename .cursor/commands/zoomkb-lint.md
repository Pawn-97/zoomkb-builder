# Lint A ZoomKB

Audit a ZoomKB for traceability, coverage, consistency, freshness, navigation, and wiki quality.

Interpret any text the user typed after `/zoomkb-lint` as lint parameters: output directory, strict mode, stale-day threshold, or request to fix issues.

If the output directory is missing:

- Use the directory named by the user if one is mentioned.
- If exactly one `*-kb` directory exists, use it.
- If multiple KB directories exist, ask which one to lint.

Use the project CLI from the repository root. Prefer:

```bash
. .venv/bin/activate && zoomkb lint --output ./zoom-rooms-kb
```

Add optional flags only when requested:

```bash
--strict
--stale-days 60
```

If `.venv` or the `zoomkb` command is missing, install locally first:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev]"
```

After lint:

1. Read `lint-report.md`.
2. Prioritize critical issues first.
3. Fix deterministic wiki metadata, navigation, broken links, or traceability problems when the user asked for fixes.
4. Do not fabricate missing source support.
5. Do not LLM-rewrite `raw/support-articles/`.
6. Re-run lint after fixes.

For UX-design usefulness, call out whether the KB is actually usable for design work, not just whether the command exited successfully. Pay attention to:

- Missing task flows
- Weak source traceability
- Overly fragmented concept pages
- UX patterns without concrete evidence
- Constraints that lack product or role context

Final response format:

- KB directory linted
- Pass/fail result
- Critical issues first
- Fixes made, if any
- Remaining design-facing risks
