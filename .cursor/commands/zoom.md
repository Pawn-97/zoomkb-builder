# ZoomKB Router

Act as the ZoomKB workflow router for this repository.

Interpret any text the user typed after `/zoom` as the requested ZoomKB action. Route to one of these workflows:

- Build a new KB: follow the same behavior as `/zoomkb-build`.
- Refresh an existing KB: follow the same behavior as `/zoomkb-refresh`.
- Lint or audit KB quality: follow the same behavior as `/zoomkb-lint`.

If the user intent is unclear, ask one concise clarification question instead of guessing.

Supported products:

- `Zoom Phone`
- `Zoom Contact Center`
- `Zoom Clips`
- `Zoom Meetings`
- `Zoom Rooms`
- `Shared Zoom Platform`

Prefer the product and output directory explicitly provided by the user. If the user gives only a product, derive the default output directory from the project convention, for example `Zoom Rooms` -> `./zoom-rooms-kb`.

Use the repository's existing Python CLI. Prefer:

```bash
. .venv/bin/activate && zoomkb ...
```

If `.venv` is missing or `zoomkb` is unavailable, set up the local editable install before running the workflow:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev]"
```

Do not rewrite files in `raw/support-articles/` with LLM-generated content. Treat raw support articles as source of truth.

At the end, report:

- What workflow ran
- What command or commands were executed
- Where the KB output lives
- Any lint or extraction issues that still need attention
