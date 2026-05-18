---
type: ux-pattern
product: zoom-phone
title: Dual-Channel Credential Delivery
sources:
  - article_id: KB0084361
    title: Using Zoom Phone eSIM numbers
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084361
confidence: high
last_reviewed: 2026-05-18
---

# Dual-Channel Credential Delivery

## Summary

Activation credentials (QR code, manual codes) are delivered through both email and the Zoom web portal, providing an automatic fallback if one channel fails. This pattern is reusable for any provisioning flow where users need to receive credentials on a separate device.

## Key points

- Email delivery is automatic and pushes to the user
- Web portal access (Phone > Settings > eSIM > View QR Code) allows self-service retrieval
- Both channels show identical content, ensuring consistency

## Related

- [[esim-activation-message]]
