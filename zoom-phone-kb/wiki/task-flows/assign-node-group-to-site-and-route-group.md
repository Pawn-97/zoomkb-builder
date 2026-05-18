---
type: task-flow
product: zoom-phone
title: Assign Node Group to Site and Route Group
sources:
  - article_id: KB0085809
    title: Configuring Zoom Phone Local Survivability with a Node group
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085809
confidence: high
last_reviewed: 2026-05-18
---

# Assign Node Group to Site and Route Group

## Summary

An assignment workflow that links a node group to a specific Site and a pre-configured Survivability Route Group. The edit interface uses a modal window, and the assignment triggers automatic round-robin user distribution. The admin cannot control which users land on which nodes after assignment.

## Key points

- Navigate: Phone System Management > Company Info > Account Settings > Zoom Node > Local Survivability > Manage > Node groups tab
- Click '...' (More), Edit, select Site and Route Group
- Assignment triggers automatic round-robin user distribution
- Route Group must be pre-created (dependency on KB0085804)

## Related

- [[zpls-node-group]]
