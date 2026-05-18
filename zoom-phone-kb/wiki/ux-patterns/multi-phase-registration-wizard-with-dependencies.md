---
type: ux-pattern
product: zoom-phone
title: Multi-Phase Registration Wizard with Dependencies
sources:
  - article_id: KB0084727
    title: Japan SMS registration guide for Zoom Phone and Contact Center
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084727
confidence: high
last_reviewed: 2026-05-18
---

# Multi-Phase Registration Wizard with Dependencies

## Summary

The Japan SMS setup is a two-phase wizard (business registration then SMS registration) where phase two cannot start until phase one is complete. Each phase has its own lifecycle states. This pattern requires clear phase indicators, dependency visualization, and the ability to return to completed phases when corrections are needed.

## Key points

- Sequential phases with hard dependency: business registration must exist before SMS registration
- Each phase has independent lifecycle states (business: editable/locked; SMS: pending/active/rejected)
- Rejected SMS registration can force users back to the business registration phase for corrections

## Related

- [[japan-sms-registration]]
