---
type: constraint
product: zoom-phone
title: Node Group Module Assignment Restrictions
sources:
  - article_id: KB0085809
    title: Configuring Zoom Phone Local Survivability with a Node group
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085809
confidence: high
last_reviewed: 2026-05-18
---

# Node Group Module Assignment Restrictions

## Summary

Only ZPLS modules that are currently unassigned (not tied to a site or other node group) can be added to a node group. This prevents configuration conflicts but means admins must first unassign a module if it was previously assigned elsewhere. The interface should clearly indicate why certain modules are unavailable for selection.

## Key points

- Only unassigned ZPLS modules can be added to a node group
- Modules already assigned to a Site or another node group are excluded
- Maximum 20 modules per node group

## Related

- [[zpls-node-group]]
