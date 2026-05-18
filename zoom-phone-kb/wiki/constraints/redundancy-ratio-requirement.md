---
type: constraint
product: zoom-phone
title: Redundancy Ratio Requirement
sources:
  - article_id: KB0085809
    title: Configuring Zoom Phone Local Survivability with a Node group
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085809
confidence: high
last_reviewed: 2026-05-18
---

# Redundancy Ratio Requirement

## Summary

When redundancy is enabled, backup nodes must be configured at a 2:1 ratio with primary nodes (2 primary nodes per 1 backup node). This hard ratio constraint means the admin interface must validate selections and prevent saving if the ratio is incorrect. Additionally, enabling redundancy halves the total user capacity.

## Key points

- 2 primary nodes : 1 backup node ratio required
- Enabling redundancy halves total user capacity
- Interface must validate ratio before allowing save

## Related

- [[node-group-redundancy]]
