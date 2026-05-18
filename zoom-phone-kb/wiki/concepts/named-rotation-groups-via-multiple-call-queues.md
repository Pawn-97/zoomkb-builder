---
type: concept
product: zoom-phone
title: Named Rotation Groups via Multiple Call Queues
sources:
  - article_id: KB0084041
    title: Setting up group rotating in a call queue
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084041
confidence: high
last_reviewed: 2026-05-18
---

# Named Rotation Groups via Multiple Call Queues

## Summary

An alternative to simple group rotating that chains two call queues together via overflow routing. The first queue rings designated primary members simultaneously; if unanswered, overflow routes the call to a second queue with secondary members. This enables named, tiered escalation groups rather than anonymous group-by-group rotation.

## Key points

- Primary queue uses simultaneous distribution; secondary queue also uses simultaneous
- First queue's overflow routes to second queue
- Second queue's overflow handles final escalation (e.g., voicemail)
- Provides more control over who is rung and in what order than basic group rotating

## Related

- [[call-queue]]
- [[group-rotating-call-distribution]]
- [[overflow-settings]]
