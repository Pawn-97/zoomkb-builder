---
type: concept
product: zoom-phone
title: A2P SMS (Application-to-Person Messaging)
sources:
  - article_id: KB0084727
    title: Japan SMS registration guide for Zoom Phone and Contact Center
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084727
confidence: high
last_reviewed: 2026-05-18
---

# A2P SMS (Application-to-Person Messaging)

## Summary

Business-to-consumer SMS messaging capability on Japanese phone numbers. In Japan, A2P SMS requires mandatory registration and is outbound-only (business to consumer). A key UX consideration is that for SoftBank recipients, the sender ID shown is not the actual phone number but a unique ID assigned by SoftBank, which can confuse recipients expecting the business number to appear.

## Key points

- Outbound-only direction: from business numbers to end consumers
- SoftBank recipients see a unique aggregator sender ID instead of the actual phone number
- This sender ID masking is a carrier-imposed restriction, not configurable by Zoom or the business

## Related

- [[japan-sms-registration]]
