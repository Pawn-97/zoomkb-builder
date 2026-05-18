---
type: constraint
product: zoom-phone
title: Rule-Target Compatibility Matrix
sources:
  - article_id: KB0075917
    title: Managing Zoom Phone Appliance device monitoring
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0075917
confidence: high
last_reviewed: 2026-05-18
---

# Rule-Target Compatibility Matrix

## Summary

Not all target types work with all rule types. The 'Account' and 'Specify Device' targets are only available for the 'Devices go offline' and 'Devices go online' rules, while 'Site' is only available for 'Offline Devices Rate'. This conditional relationship must be reflected in the UI with dynamic form controls.

## Key points

- Account target: only for Devices go offline and Devices go online rules
- Specify Device target: only for Devices go offline and Devices go online rules
- Site target: only for Offline Devices Rate rule

## Related

- [[alert-targets]]
