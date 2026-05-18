---
type: concept
product: zoom-phone
title: Japan SMS Registration
sources:
  - article_id: KB0084727
    title: Japan SMS registration guide for Zoom Phone and Contact Center
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084727
confidence: high
last_reviewed: 2026-05-18
---

# Japan SMS Registration

## Summary

A two-step registration process required by Japanese mobile carriers to enable business-to-consumer (A2P) SMS messaging on Japan-based phone numbers. The process involves a business registration (company info) followed by an SMS registration (number assignment and carrier approval), with external carrier review taking a minimum of 2 weeks. The multi-step dependency and external approval timeline have significant UX implications for progress tracking and expectation management.

## Key points

- Two-phase process: business registration (no approval needed) then SMS registration (carrier approval required)
- External carrier approval takes a minimum of 2 weeks
- Business registration must exist before SMS registration can be created
- Numbers are assigned to the SMS registration before it is sent for approval
- Inconsistencies flagged during SMS registration approval may require updating the business registration
- Created after business registration is complete
- Includes a checklist requirement that users must open and review before proceeding
- Phone numbers are assigned before submission for approval
- Lifecycle states: pending, active, rejected -- each with different available actions

## Related

- [[japan-sms-registration]]
