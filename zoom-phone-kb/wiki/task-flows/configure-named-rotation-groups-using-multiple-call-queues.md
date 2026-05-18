---
type: task-flow
product: zoom-phone
title: Configure Named Rotation Groups Using Multiple Call Queues
sources:
  - article_id: KB0084041
    title: Setting up group rotating in a call queue
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084041
confidence: high
last_reviewed: 2026-05-18
---

# Configure Named Rotation Groups Using Multiple Call Queues

## Summary

A two-phase setup where admins create two separate call queues linked by overflow routing. The primary queue rings a named set of members simultaneously; if unanswered, calls overflow to a secondary queue with a different set of members, which itself has its own overflow escalation.

## Key points

- Phase 1: Create primary queue, add members, set distribution to Simultaneous, configure overflow to second queue
- Phase 2: Create secondary queue, add different members, configure its overflow to voicemail or forwarding
- End result: named tier-1 group rings first, named tier-2 group rings second, final overflow handles the rest
- Provides deliberate, predictable call routing across known member groups

## Related

- [[call-queue]]
- [[named-rotation-groups-via-multiple-call-queues]]
- [[overflow-settings]]
