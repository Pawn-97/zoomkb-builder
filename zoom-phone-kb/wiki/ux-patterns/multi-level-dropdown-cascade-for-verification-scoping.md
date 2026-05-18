---
type: ux-pattern
product: zoom-phone
title: Multi-Level Dropdown Cascade for Verification Scoping
sources:
  - article_id: KB0085008
    title: Setting up business address verification for Zoom Phone Mobile UK
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085008
confidence: high
last_reviewed: 2026-05-18
---

# Multi-Level Dropdown Cascade for Verification Scoping

## Summary

The verification setup uses a three-level dropdown cascade (Product > Country > Number Type) that progressively narrows options. Each selection determines what appears in the next dropdown, and the combination scopes the verification context. This pattern requires clear dependency indicators and may benefit from wizard-style progression rather than a flat form.

## Key points

- Three-level cascade: Product > Country/Region > Number Type & Capability
- Each dropdown choice filters the next dropdown's options
- The combination (Phone + United Kingdom + Mobile - eSIM) determines verification requirements
- Could benefit from visual progression indicators to show where the user is in the scoping process

## Related

- [[business-address-verification]]
