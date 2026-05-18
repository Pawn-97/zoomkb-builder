---
type: ux-pattern
product: zoom-phone
title: Lifecycle State-Driven UI
sources:
  - article_id: KB0084727
    title: Japan SMS registration guide for Zoom Phone and Contact Center
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084727
confidence: high
last_reviewed: 2026-05-18
---

# Lifecycle State-Driven UI

## Summary

Both business and SMS registrations have lifecycle states that control what actions are available. Business registration can be edited/deleted only when no linked SMS registration is pending/active. SMS registration goes through pending, active, and rejected states. The UI should use state-based disabling with explanatory tooltips rather than hiding actions entirely.

## Key points

- Actions are conditionally available based on registration state
- Disabled states should explain why an action is unavailable
- Rejected state triggers corrective actions (update business info, resubmit)

## Related

- [[manage-business-registration-lifecycle]]
