# Refresh A ZoomKB

Refresh an existing ZoomKB by re-crawling accepted Zoom Support articles, detecting changed or stale sources, and reporting what needs review.

Interpret any text the user typed after `/zoomkb-refresh` as refresh parameters: output directory, article IDs, force refresh, or stale-day threshold.

If the output directory is missing:

- Use the directory named by the user if one is mentioned.
- If exactly one `*-kb` directory exists, use it.
- If multiple KB directories exist, ask which one to refresh.

Use the project CLI from the repository root. Prefer:

```bash
. .venv/bin/activate && zoomkb refresh --output ./zoom-rooms-kb
```

Add optional flags only when requested:

```bash
--force
--article-ids KB0060257 KB0069655
--stale-days 14
```

If `.venv` or the `zoomkb` command is missing, install locally first:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev]"
```

After refresh:

1. Read the generated `refresh-report.md` if it exists.
2. Check whether articles moved to review or were marked stale.
3. Run `zoomkb freshness --output <kb-dir>` when source freshness needs explanation.
4. Run `zoomkb lint --output <kb-dir>` to show the current KB quality state.

Do not rewrite `raw/support-articles/` manually. The crawler owns raw article files.

If refreshed articles require new extraction, explain the next step clearly. Only run ingest prepare/extract/commit when the user asked for a full update, not merely a freshness check.

Final response format:

- KB directory refreshed
- Commands run
- Changed, stale, failed, or review articles
- Whether lint passed
- Recommended next action
