---
type: task-flow
product: zoom-phone
title: Enable or Disable Peer-to-Peer Media at Account Level
sources:
  - article_id: KB0083729
    title: Enabling or disabling Peer-to-Peer media for Zoom Phone
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0083729
confidence: high
last_reviewed: 2026-05-18
---

# Enable or Disable Peer-to-Peer Media at Account Level

## Summary

Admins navigate to Account Settings > Zoom Phone > General and toggle the Peer to Peer Media setting. A verification dialog confirms the change, and an optional lock prevents lower-level overrides. Designers should ensure the toggle, dialog, and lock icon are clearly associated and the grayed-out state at lower levels communicates the lock relationship.

## Key points

- Navigate: Account Management > Account Settings > Zoom Phone tab
- Toggle Peer to Peer Media under General section
- Confirm via verification dialog (Enable/Disable)
- Optional: click lock icon to prevent user-level changes
- Navigate: User Management > Groups > select group > Zoom Phone tab
- Option grayed out if locked at account level, with explanatory note
- Optional: click lock icon to prevent user-level changes within group
- Navigate: Phone System Management > Company Info > select site > Policy tab
- Confirm via verification dialog
- Optional: lock to prevent user-level changes within site

## Related

- [[hierarchical-settings-lock]]
- [[peer-to-peer-media]]
