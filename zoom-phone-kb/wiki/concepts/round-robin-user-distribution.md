---
type: concept
product: zoom-phone
title: Round-Robin User Distribution
sources:
  - article_id: KB0085809
    title: Configuring Zoom Phone Local Survivability with a Node group
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085809
confidence: high
last_reviewed: 2026-05-18
---

# Round-Robin User Distribution

## Summary

The automated mechanism by which the Zoom cloud assigns users and common areas across ZPLS modules within a node group. Distribution is balanced across all nodes in the group and cannot be manually controlled or modified by administrators. This is a significant UX implication -- admins have no control over which users go to which nodes, so the interface should focus on aggregate group health rather than per-node user details.

## Key points

- Automatic balanced user distribution across all nodes in the group
- Cannot be manually controlled or modified by administrators
- Managed entirely by Zoom cloud
- Ensures optimal balance without admin intervention

## Related

- [[zpls-node-group]]
