---
type: concept
product: zoom-phone
title: Call Bridge (Shared Database Nodes)
sources:
  - article_id: KB0085763
    title: Deploying the Call Bridge service for Zoom Phone Local Survivability
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085763
confidence: high
last_reviewed: 2026-05-18
---

# Call Bridge (Shared Database Nodes)

## Summary

A standalone Node server service that synchronizes state information across ZPLS modules and enables call routing between different ZPLS nodes or node groups during internet outages. Without a Call Bridge, users at different sites cannot call each other when survivability mode is active. Designers should understand this as critical inter-site communication infrastructure that must remain accessible to all ZPLS modules.

## Key points

- Enables cross-site calls during outages when Zoom cloud is unreachable
- Must be deployed on a standalone Node server accessible to all ZPLS modules
- Also known as Shared Database Nodes in the UI
- Not required for communication between nodes within the same node group

## Related

- [[zpls-node-group]]
