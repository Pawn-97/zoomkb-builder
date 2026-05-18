---
type: concept
product: zoom-phone
title: Alert Rules for Device Monitoring
sources:
  - article_id: KB0075917
    title: Managing Zoom Phone Appliance device monitoring
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0075917
confidence: high
last_reviewed: 2026-05-18
---

# Alert Rules for Device Monitoring

## Summary

Three distinct alert rules define the conditions that trigger a notification. 'Devices go offline' and 'Devices go online' monitor individual device state transitions, while 'Offline Devices Rate' triggers when a percentage of devices at a site level goes offline. Each rule type has different target options and configuration parameters, requiring context-aware form controls.

## Key points

- Devices go offline: triggers on individual device disconnection, targetable to a single device or entire account
- Devices go online: triggers on individual device reconnection, targetable to a single device or entire account
- Offline Devices Rate: triggers when a percentage threshold is crossed at the site level, with separate warning and critical percentage values
- Each rule type can only be set once per target

## Related

- [[alert-targets]]
