---
type: ux-pattern
product: zoom-phone
title: Hierarchical Settings with Lock Propagation
sources:
  - article_id: KB0084689
    title: Enabling or disabling Zoom Phone call delegation
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084689
confidence: high
last_reviewed: 2026-05-18
---

# Hierarchical Settings with Lock Propagation

## Summary

A governance pattern where settings cascade from Account > Group/Site > Phone User/Common Area, with lock mechanisms at each level to prevent downstream overrides. This pattern is reusable across all Zoom Phone policy settings and should use consistent visual language (toggle, lock icon, grayed-out disabled state) to build admin familiarity.

## Key points

- Top-down cascade: Account overrides Group/Site, which override Phone User/Common Area
- Lock icon at each level enforces the current setting downward
- Grayed-out state + informational note communicates upstream lock
- Consistent toggle component across all five levels

## Related

- [[delegation-toggle]]
- [[hierarchical-settings-lock]]
