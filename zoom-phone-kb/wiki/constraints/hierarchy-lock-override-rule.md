---
type: constraint
product: zoom-phone
title: Hierarchy Lock Override Rule
sources:
  - article_id: KB0084689
    title: Enabling or disabling Zoom Phone call delegation
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084689
confidence: high
last_reviewed: 2026-05-18
---

# Hierarchy Lock Override Rule

## Summary

When a setting is locked at a higher hierarchy level (e.g., Account), lower-level toggles are grayed out and cannot be changed. Admins must navigate to the locking level to modify the setting. This constraint is communicated through UI state (grayed out toggle + informational note) rather than blocking navigation, which preserves exploration while preventing changes.

## Key points

- Account-level lock overrides all lower levels
- Grayed-out toggle indicates the setting is locked upstream
- Informational note directs admin to the locking level

## Related

- [[delegation-toggle]]
- [[hierarchical-settings-lock]]
