---
type: concept
product: zoom-phone
title: Zoom Phone Local Survivability (ZPLS)
sources:
  - article_id: KB0085762
    title: Manually synchronizing data in Zoom Phone Local Survivability
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085762
confidence: high
last_reviewed: 2026-05-18
---

# Zoom Phone Local Survivability (ZPLS)

## Summary

A cloud-managed telephony survivability system that keeps phone services running when internet connectivity to Zoom's cloud is lost. ZPLS nodes and node groups are deployed on-premises and must receive up-to-date configuration data to function correctly during outages. Designers should note that ZPLS is fully managed from the cloud with no local admin interface.

## Key points

- Fully cloud-managed; no local admin interface on ZPLS modules
- Supports individual nodes and node groups for different deployment scales
- Requires data synchronization after any configuration change (users, phones, groups)

## Related

- [[zpls-data-synchronization]]
- [[zpls-node-group]]
