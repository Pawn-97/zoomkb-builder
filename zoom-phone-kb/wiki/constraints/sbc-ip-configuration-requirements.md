---
type: constraint
product: zoom-phone
title: SBC IP Configuration Requirements
sources:
  - article_id: KB0085804
    title: Configuring Zoom Phone Local Survivability with a Session Border Controller (SBC)
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085804
confidence: high
last_reviewed: 2026-05-18
---

# SBC IP Configuration Requirements

## Summary

For single ZPLS node deployments, the SBC must be configured with the node's IP address. For node group deployments, the SBC must route to at least 2 ZPLS node IP addresses to eliminate single point of failure. This distinction must be clear in the admin interface to prevent misconfiguration.

## Key points

- Single node: enter one ZPLS node IP in SBC config
- Node group: must configure at least 2 ZPLS node IP addresses
- SBC generally uses internal/RFC1918 IP for local communication

## Related

_None yet_
