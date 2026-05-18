---
type: ux-pattern
product: zoom-phone
title: Overflow Routing as Queue-to-Queue Chaining
sources:
  - article_id: KB0084041
    title: Setting up group rotating in a call queue
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084041
confidence: high
last_reviewed: 2026-05-18
---

# Overflow Routing as Queue-to-Queue Chaining

## Summary

Overflow configuration acts as an explicit routing link between call queues, enabling a chain-of-responsibility pattern. Designers can treat this as a visual call-routing builder where queues are connected nodes in a flow graph.

## Key points

- Overflow settings allow selecting another call queue as the destination
- Enables multi-tier escalation chains: queue 1 -> queue 2 -> voicemail
- Low-code routing: admins compose complex call flows without scripting

## Related

- [[call-queue]]
- [[named-rotation-groups-via-multiple-call-queues]]
- [[overflow-settings]]
