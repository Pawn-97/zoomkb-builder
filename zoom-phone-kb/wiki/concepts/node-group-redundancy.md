---
type: concept
product: zoom-phone
title: Node Group Redundancy
sources:
  - article_id: KB0085809
    title: Configuring Zoom Phone Local Survivability with a Node group
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085809
confidence: high
last_reviewed: 2026-05-18
---

# Node Group Redundancy

## Summary

An optional high-availability configuration within node groups where backup nodes automatically take over if primary nodes fail. Redundancy requires a strict 2:1 primary-to-backup ratio. When enabled, total user capacity is halved (from 100K to 50K with 20 modules). This trade-off between capacity and resilience must be clearly communicated in the admin interface.

## Key points

- 2:1 primary-to-backup node ratio required for proper redundancy
- Halves total user capacity when enabled (100K to 50K with 20 modules)
- Backup nodes are selected from the node list after adding primary nodes

## Related

- [[zpls-node-group]]
