# Build A ZoomKB

Create or update a design-facing Zoom knowledge base from official Zoom Support articles.

Interpret any text the user typed after `/zoomkb-build` as build parameters: product, output directory, URL list, max candidates, dry run, force rebuild, or skip flags.

Supported products:

- `Zoom Phone`
- `Zoom Contact Center`
- `Zoom Clips`
- `Zoom Meetings`
- `Zoom Rooms`
- `Shared Zoom Platform`

If the product is missing, ask the user which product to build. Do not silently default to `Zoom Phone` unless the user explicitly asks for the default.

Use the project CLI from the repository root. Prefer:

```bash
. .venv/bin/activate && zoomkb build --product "Zoom Rooms"
```

Add `--output`, `--max-candidates`, `--urls`, `--url-file`, `--dry-run`, `--force`, `--skip-discover`, `--skip-crawl`, `--min-sources`, or `--min-quality` only when the user requests them or the existing KB state clearly requires them.

If `.venv` or the `zoomkb` command is missing, install locally first:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev]"
```

During the extraction phase:

1. Look for prompt files in the target KB's `extraction-queue/*.prompt.md`.
2. For each prompt that lacks a matching `.result.json`, read the source article content and extract only grounded entities.
3. Write a result JSON with this shape:

```json
{
  "entities": [
    {
      "type": "concept|task-flow|user-role|constraint|ux-pattern",
      "title": "Entity title",
      "description": "Concise description grounded in source articles",
      "source_article_ids": ["KB0060257"],
      "quality_score": 85
    }
  ]
}
```

4. Do not invent entities that are not supported by the source article.
5. Do not rewrite `raw/support-articles/`.
6. After results are written, run `zoomkb ingest --output <kb-dir> --commit`, then run `zoomkb lint --output <kb-dir>`.

Quality checks:

- Every wiki page needs frontmatter with `type`, `source_article_ids`, and `quality_score`.
- Every entity must trace back to at least one raw article.
- `wiki/index.md` should cover `concepts`, `task-flows`, `user-roles`, `constraints`, and `ux-patterns`.
- Prefer fixing deterministic wiki/report issues. Ask before making broad editorial rewrites.

Final response format:

- Product and output directory
- Commands run
- Number of prompts processed, if any
- Lint result and remaining issues
