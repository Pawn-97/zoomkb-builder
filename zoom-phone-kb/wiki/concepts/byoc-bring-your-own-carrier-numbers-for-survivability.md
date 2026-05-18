---
type: concept
product: zoom-phone
title: BYOC (Bring Your Own Carrier) Numbers for Survivability
sources:
  - article_id: KB0085766
    title: Configuring call forwarding for Zoom Phone Local Survivability
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085766
confidence: high
last_reviewed: 2026-05-18
---

# BYOC (Bring Your Own Carrier) Numbers for Survivability

## Summary

Customer-provided PSTN phone numbers that serve as the destination for forwarded calls during survivability mode. The number of BYOC extensions must match the count of unique extensions needed during failover (a 1:1 mapping requirement). One additional BYOC number must be reserved for emergency services (ELIN) and cannot be assigned to any user or entity.

## Key points

- Must be acquired from BYOC provider and assigned to users within the site
- 1:1 mapping needed: N users requiring DID equals N BYOC extensions required
- One BYOC number must be reserved exclusively for emergency services (ELIN)
- Only BYOC numbers assigned to users within the same site can be used

## Related

- [[call-forwarding-local-survivability]]
