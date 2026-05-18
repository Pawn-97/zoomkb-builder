---
type: ux-pattern
product: zoom-phone
title: Verification Status and Rejection Handling
sources:
  - article_id: KB0085008
    title: Setting up business address verification for Zoom Phone Mobile UK
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085008
confidence: high
last_reviewed: 2026-05-18
---

# Verification Status and Rejection Handling

## Summary

After submission, verification undergoes human review. If documents are rejected, admins need clear feedback on what was wrong and how to fix it. The article FAQ indicates a single verification can be reused for multiple orders, suggesting a status dashboard pattern where verification state is visible across different workflows. Designers should plan for the full lifecycle: pending, approved, rejected-with-reason, and expired.

## Key points

- Verification is not instant; there is a review and approval period
- Rejection requires specific guidance on what to fix and resubmit
- A single verification can cover multiple number orders (don't force re-verification)
- Status should be visible from any workflow that depends on verification

## Related

- [[business-address-verification]]
