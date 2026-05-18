---
type: concept
product: zoom-phone
title: Survivability Routing Rules
sources:
  - article_id: KB0085804
    title: Configuring Zoom Phone Local Survivability with a Session Border Controller (SBC)
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085804
confidence: high
last_reviewed: 2026-05-18
---

# Survivability Routing Rules

## Summary

Rules governing how calls are routed during survivability mode. While the Routing Path (SIP Group or PSTN) is ignored during survivability, number translations are preserved. The 'Other sites' routing path is restricted to same-site extension calls only. This is important for designers because it means the full routing configuration does not apply in survivability mode -- only a subset of features work.

## Key points

- Routing Path ignored during survivability mode; number translations preserved
- Other sites routing path limited to same-site extension calls only
- Preserves legacy dialing habits and custom call routing where translations apply

## Related

- [[survivability-route-group]]
