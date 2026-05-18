---
type: constraint
product: zoom-phone
title: Group Rotating Member Order
sources:
  - article_id: KB0084041
    title: Setting up group rotating in a call queue
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084041
confidence: high
last_reviewed: 2026-05-18
---

# Group Rotating Member Order

## Summary

In the basic group rotating method, there is no guarantee of which specific members are in each group. The system divides members into groups automatically. For precise control over who is rung first, admins must use the named rotation groups pattern with multiple call queues.

## Key points

- Basic group rotating assigns members to groups arbitrarily—no manual ordering
- Named rotation groups solve this by chaining queues with explicit member lists
- Design implication: clearly communicate this limitation in the UI to prevent confusion

## Related

- [[group-rotating-call-distribution]]
- [[named-rotation-groups-via-multiple-call-queues]]
