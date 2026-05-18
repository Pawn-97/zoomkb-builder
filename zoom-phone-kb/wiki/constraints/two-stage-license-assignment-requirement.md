---
type: constraint
product: zoom-phone
title: Two-Stage License Assignment Requirement
sources:
  - article_id: KB0084068
    title: Getting started with Zoom Phone Mobile licenses
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084068
confidence: high
last_reviewed: 2026-05-18
---

# Two-Stage License Assignment Requirement

## Summary

Admins must assign licenses in a specific order: first Zoom Phone Basic in User Management, then Zoom Phone Mobile in eSIM Management. eSIM Management cannot assign a Mobile license to a user who lacks the Basic license. This split assignment flow adds operational complexity.

## Key points

- Design implication: cross-surface workflow with dependency
- eSIM Management should indicate which users are eligible (already have Basic license)
- Error prevention: block or warn if Mobile license assigned without Basic license

## Related

- [[esim-management]]
