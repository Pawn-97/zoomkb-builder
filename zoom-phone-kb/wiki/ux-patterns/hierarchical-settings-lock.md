---
type: ux-pattern
product: zoom-phone
title: Hierarchical Settings Lock
sources:
  - article_id: KB0083729
    title: Enabling or disabling Peer-to-Peer media for Zoom Phone
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0083729
  - article_id: KB0084689
    title: Enabling or disabling Zoom Phone call delegation
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084689
confidence: high
last_reviewed: 2026-05-18
---

# Hierarchical Settings Lock

## Summary

A governance mechanism where settings configured at a higher hierarchy level (Account) propagate down and can be locked to prevent changes at lower levels (Group, Site, User). When locked, lower-level toggles appear grayed out with a note directing admins to change the setting at the locking level. This pattern is foundational to Zoom Phone's admin UX and must clearly communicate the lock source to avoid confusion.

## Key points

- Lock cascades from account > group > site > user
- Grayed-out toggle with descriptive note when locked at higher level
- Lock icon displayed next to toggle when lockable
- Note at user level explicitly directs admin to contact higher-level admin
- Account > Group/Site > Phone User/Common Area hierarchy
- Lock icon enforces the current setting and prevents lower-level changes
- Grayed-out toggle with note indicates the setting is locked at a higher level
- Admins must navigate to the locking level to make changes

## Related

- [[delegation-toggle]]
- [[peer-to-peer-media]]
