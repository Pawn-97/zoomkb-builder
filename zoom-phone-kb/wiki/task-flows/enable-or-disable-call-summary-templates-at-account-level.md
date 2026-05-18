---
type: task-flow
product: zoom-phone
title: Enable or Disable Call Summary Templates at Account Level
sources:
  - article_id: KB0084831
    title: Enabling or disabling Zoom Phone call summary templates
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084831
confidence: high
last_reviewed: 2026-05-18
---

# Enable or Disable Call Summary Templates at Account Level

## Summary

Admins navigate through Account Management > Account Settings > Zoom Phone > AI Companion to toggle call summary templates for all users. The flow includes an optional lock step to prevent lower-level changes, and an optional default template selection step. Designers should structure this as a single coherent settings section with clear hierarchy indicators.

## Key points

- Path: Account Management > Account Settings > Zoom Phone > AI Companion
- Toggle with verification dialog for enable/disable confirmation
- Optional lock icon to prevent lower-level overrides
- Optional default template selection step
- Path: User Management > Groups > [group name] > Zoom Phone > AI Companion
- Grayed out if locked at account level, with note directing to account-level change
- Optional lock and default template selection
- Changes apply only to users in the selected group
- Path: Phone System Management > Company Info > [site name] > Policy > AI Companion
- Uses Policy tab rather than a dedicated Zoom Phone tab, which differs from account/group flows
- Grayed out if locked at account level

## Related

- [[hierarchical-setting-locking]]
