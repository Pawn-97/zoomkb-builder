---
type: ux-pattern
product: zoom-phone
title: Multi-Document Upload with Individual Constraints
sources:
  - article_id: KB0085008
    title: Setting up business address verification for Zoom Phone Mobile UK
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085008
confidence: high
last_reviewed: 2026-05-18
---

# Multi-Document Upload with Individual Constraints

## Summary

The verification form requires three distinct document uploads (Proof of Business, Proof of Identity, Proof of Address), each with its own accepted document types. The UX must handle per-field validation, partial upload progress, and clear distinction between the three document categories to prevent users from uploading the wrong document type in each slot.

## Key points

- Three separate upload slots, each for a different document category
- Each slot has specific accepted document types (e.g., passport only for identity)
- Inline validation for format, size, clarity, and date freshness per slot
- Users should be able to save partial progress and return to complete

## Related

- [[business-address-verification]]
