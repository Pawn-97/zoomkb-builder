---
type: constraint
product: zoom-phone
title: Automated Distribution Limitation
sources:
  - article_id: KB0085809
    title: Configuring Zoom Phone Local Survivability with a Node group
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085809
confidence: high
last_reviewed: 2026-05-18
---

# Automated Distribution Limitation

## Summary

User and common area distribution across ZPLS nodes is fully automated via round-robin and cannot be manually controlled or modified. This means the admin interface should not expose per-node user assignment controls, as they would have no effect. This is a significant design constraint that simplifies the UI but removes admin flexibility.

## Key points

- User distribution is fully automated, no manual control
- Admins cannot specify which users go to which nodes
- Interface should focus on aggregate group health rather than per-node details

## Related

_None yet_
