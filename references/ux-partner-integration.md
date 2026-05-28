# UX-partner Integration

After building a KB with `/zoomkb:build`, the output is directly consumable by UX-partner via its `setup-kb` command:

```bash
# 1. Build the KB
/zoomkb:build --product "Zoom Phone" --output ./zoom-phone-kb

# 2. In UX-partner, index it for design sessions
/ux-project:setup-kb ./zoom-phone-kb
```

## Detection

UX-partner's `setup-kb` detects zoomkb-builder output by checking `manifest.json` for `"kb_type": "zoomkb"` (fallback: verifies `wiki/index.md` and the five standard wiki subdirectories exist).

## Classification tags

Each wiki page is tagged by its source directory when indexed into context-mode FTS5:

| Wiki path | UX-partner tag | Usage |
|---|---|---|
| `wiki/concepts/` | CONCEPT | Product concepts and features |
| `wiki/task-flows/` | TASK-FLOW | User task steps and dependencies |
| `wiki/user-roles/` | USER-ROLE | Role definitions and permissions |
| `wiki/constraints/` | CONSTRAINT | Design limitations and rules |
| `wiki/ux-patterns/` | UX-PATTERN | Reusable interaction patterns |
| `raw/support-articles/` | RAW-SOURCE | Ground truth — always cite |
| `wiki/index.md` | META | Navigation index |
| `10-LLM-Wiki/` | META | Taxonomy, category navigation, full listings, and cross references |
| `30-Agent-Playbooks/` | PLAYBOOK | Troubleshooting and root-cause workflows |

## Citation policy

UX-partner applies a cite-or-die policy: every UX claim must reference a KB page. Citation priority order:

1. PRD / PM requirement document
2. KB wiki pages (concepts, task-flows, constraints, user-roles, ux-patterns)
3. KB raw articles (support articles — ultimate authority)
4. Project memory files
5. Assumptions (explicitly marked)

Raw articles are never LLM-rewritten, making them the most authoritative source for fact-checking wiki claims.
