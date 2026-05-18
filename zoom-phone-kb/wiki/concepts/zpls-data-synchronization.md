---
type: concept
product: zoom-phone
title: ZPLS Data Synchronization
sources:
  - article_id: KB0085762
    title: Manually synchronizing data in Zoom Phone Local Survivability
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085762
confidence: high
last_reviewed: 2026-05-18
---

# ZPLS Data Synchronization

## Summary

A two-path workflow allowing admins to sync either a single ZPLS node or an entire node group. The UI differentiates these paths by placing the Sync button in different sections (Status section for individual nodes, Site section for node groups), which could be confusing if not clearly labeled. The 30-minute rate limit means the interface should display a cooldown timer or disable the button after use.

## Key points

- Automatic sync on node boot and every 10 hours
- Manual sync available from admin portal but limited to once per 30 minutes
- Required after adding users, common areas, phone numbers, or Survivable Distribution Groups
- Navigate: Phone System Management > Company Info > Site > Settings > Zoom Node > Local Survivability > Manage
- For individual node: scroll to Status section, click Sync
- For node group: scroll to Site section, click Sync
- Manual sync limited to once every 30 minutes
- Sync status should be communicated to admin after initiation

## Related

- [[zpls-data-synchronization]]
- [[zpls-node-group]]
