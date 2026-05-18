---
type: constraint
product: zoom-phone
title: Approved Messaging Campaign Required for Phone Number
sources:
  - article_id: KB0085540
    title: Configuring Zoom Virtual Agent SMS tool to enable Zoom Phone SMS feature
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085540
confidence: high
last_reviewed: 2026-05-18
---

# Approved Messaging Campaign Required for Phone Number

## Summary

The phone number assigned to the auto receptionist for SMS must have an Approved Messaging Campaign. If no campaign exists, one must be created before the SMS feature can be enabled. This creates a prerequisite sub-flow that may not be obvious to admins setting up SMS for the first time.

## Key points

- Phone number must have an Approved Messaging Campaign before SMS can be enabled
- If no campaign exists, one must be created separately
- This is noted as a prerequisite rather than a step in the main flow
- Admins may be blocked if they are unaware of this requirement

## Related

- [[approved-messaging-campaign]]
