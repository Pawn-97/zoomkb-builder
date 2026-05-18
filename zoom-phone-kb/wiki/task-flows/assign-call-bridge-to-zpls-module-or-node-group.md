---
type: task-flow
product: zoom-phone
title: Assign Call Bridge to ZPLS Module or Node Group
sources:
  - article_id: KB0085763
    title: Deploying the Call Bridge service for Zoom Phone Local Survivability
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085763
confidence: high
last_reviewed: 2026-05-18
---

# Assign Call Bridge to ZPLS Module or Node Group

## Summary

After deployment, the Call Bridge must be explicitly linked to ZPLS nodes or groups through the Phone System Management interface. The assignment flow ends with a recommendation to manually synchronize ZPLS data, creating a dependency on the sync workflow from KB0085762. The tab-based selection (Node or Node Group) provides clear scope differentiation.

## Key points

- Navigate: Phone System Management > Company Info > Account Settings > Zoom Node > Local Survivability > Shared database nodes
- Click More icon, Edit, then select ZPLS Node or Node Group from corresponding tab
- Final step requires manual ZPLS data synchronization (KB0085762 dependency)
- Tab-based UI for selecting between Node and Node Group assignment

## Related

- [[zpls-data-synchronization]]
