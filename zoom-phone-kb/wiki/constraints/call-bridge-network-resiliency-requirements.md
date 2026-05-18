---
type: constraint
product: zoom-phone
title: Call Bridge Network Resiliency Requirements
sources:
  - article_id: KB0085763
    title: Deploying the Call Bridge service for Zoom Phone Local Survivability
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085763
confidence: high
last_reviewed: 2026-05-18
---

# Call Bridge Network Resiliency Requirements

## Summary

The Call Bridge must be deployed on a standalone Node server with connectivity to all ZPLS modules. If the Call Bridge becomes unreachable during survivability mode, cross-site calls fail because the originating node cannot determine the destination node's location. This single-point-of-failure risk should be clearly communicated in the admin UI.

## Key points

- Standalone Node server required, accessible to all ZPLS modules
- Loss of Call Bridge connectivity causes cross-site call failure
- Within same node group, nodes communicate without Call Bridge
- Network topology resiliency must be considered by admin

## Related

_None yet_
