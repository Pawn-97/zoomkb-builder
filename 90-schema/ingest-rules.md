# Ingest Rules

Rules governing how raw support articles are compiled into design-facing wiki pages.

## Core principles

1. **Raw source is immutable.** The LLM reads raw articles but never rewrites them. Raw markdown is the source of truth.
2. **Every claim must trace to a source.** Wiki pages list `sources` in frontmatter with article_id, title, and source_url.
3. **No hallucination.** The LLM must only extract entities actually present in the article. If an entity type has no matches, return an empty array.
4. **Design-facing, not implementation-facing.** Summaries focus on UX implications, not technical configuration details.

## Entity extraction rules

### Concept
Extract when the article defines or explains a product concept, feature, or object.
- Focus on: what it is, why it exists, what designers need to know about it
- Skip: step-by-step configuration instructions (those go to task-flows)

### User-Role
Extract when the article describes a role with distinct permissions or visibility.
- Include: role name, scope (account/site/group), what they can/cannot do
- Focus on: permission boundaries that affect UI visibility

### Task-Flow
Extract when the article describes a multi-step user task.
- Include: goal, prerequisites, steps, dependencies, failure modes
- Focus on: entry points, decision points, error states

### Constraint
Extract when the article mentions a limitation, rule, or restriction.
- Include: what is constrained, why, workarounds if any
- Types: role-based, license-based, hierarchy-based (account/site/extension)

### UX-Pattern
Extract when a recurring interaction pattern is described.
- Examples: inherited settings, locked settings, bulk-apply, disabled-state explanation
- Focus on: pattern name, when to use it, what problem it solves

## Merging rules

When a wiki page already exists (same slug), the ingest merges:
- **Sources**: new article_id appended (no duplicates)
- **Summary**: longer summary kept
- **Key points**: new unique points appended
- **Related**: union of related slugs, sorted

## Quality gates

- Summary must be ≥ 2 sentences
- At least one key point per entity
- source_url must be a valid Zoom Support URL
- Entity title must be human-readable (not an article_id)
