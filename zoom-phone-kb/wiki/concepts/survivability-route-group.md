---
type: concept
product: zoom-phone
title: Survivability Route Group
sources:
  - article_id: KB0085804
    title: Configuring Zoom Phone Local Survivability with a Session Border Controller (SBC)
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085804
confidence: high
last_reviewed: 2026-05-18
---

# Survivability Route Group

## Summary

A form-based workflow where admins create a new route group with type 'Survivability' and assign SBCs to it. The display name and type selection are the primary UX elements. The distinction between Common and Zoom Phone tabs addresses different customer needs, with most using Common. Options Ping should be enabled for health monitoring.

## Key points

- Groups SBCs for survivability routing with type 'Survivability'
- Must be assigned to a ZPLS module and associated with a site
- Options Ping should be enabled for continuous connectivity monitoring
- Navigate: Number Management > BYOC Configuration > Route Groups > Manage
- Select Common or Zoom Phone tab, click Add
- Enter Display Name, select Survivability as Type, assign SBCs
- Enable Options Ping for continuous connectivity monitoring

## Related

- [[survivability-route-group]]
- [[survivability-routing-rules]]
