---
type: ux-pattern
product: zoom-phone
title: Toggle with Dependent Configuration
sources:
  - article_id: KB0085540
    title: Configuring Zoom Virtual Agent SMS tool to enable Zoom Phone SMS feature
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085540
confidence: high
last_reviewed: 2026-05-18
---

# Toggle with Dependent Configuration

## Summary

The SMS toggle in the Auto Receptionist Policy tab cannot function independently—it requires a phone number with an approved messaging campaign and at least one user on the Allow List. This pattern of a master toggle with prerequisite sub-configurations should provide inline validation and guided setup rather than allowing the toggle to be enabled in a non-functional state.

## Key points

- SMS toggle under Policy > General is the master enable/disable
- Depends on: assigned 10-digit number with campaign, Allow List with at least one user
- Enabling without prerequisites met should surface validation errors or guided setup
- Relationship between toggle and its dependencies should be visually clear

## Related

- [[approved-messaging-campaign]]
