---
type: constraint
product: zoom-phone
title: Hierarchical Setting Locking
sources:
  - article_id: KB0084831
    title: Enabling or disabling Zoom Phone call summary templates
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084831
confidence: high
last_reviewed: 2026-05-18
---

# Hierarchical Setting Locking

## Summary

A cascading permissions pattern where admins can lock a setting at any level (account, group, site), preventing lower-level roles from modifying it. The UI uses a lock icon button paired with a lock confirmation dialog. This pattern appears across Zoom Phone admin settings and needs visual consistency in how locks are represented, confirmed, and unlocked.

## Key points

- Account-level lock cascades down to all lower levels
- Grayed-out controls must include explanatory text about where to change the setting
- Individual users are told to contact their admin when locked
- Lock icon is a visual indicator used across all admin configuration pages
- Lock icon toggle with confirmation dialog
- Grayed-out state for locked settings at lower levels
- Informational text explaining where the lock was applied
- Pattern repeats identically across account, group, site, and user configuration pages

## Related

_None yet_
