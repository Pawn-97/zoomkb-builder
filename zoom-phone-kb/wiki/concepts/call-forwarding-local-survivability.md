---
type: concept
product: zoom-phone
title: Call Forwarding Local Survivability
sources:
  - article_id: KB0085766
    title: Configuring call forwarding for Zoom Phone Local Survivability
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085766
confidence: high
last_reviewed: 2026-05-18
---

# Call Forwarding Local Survivability

## Summary

A survivability feature that redirects inbound calls to Zoom native numbers (or Provider Exchange numbers) through BYOC PSTN numbers when internet connectivity is lost. This ensures users receive calls even during outages by routing through the local PSTN network. Designers should understand this as a pre-configured failover mechanism that admins must plan and activate.

## Key points

- Automatically forwards Zoom native numbers to BYOC numbers during survivability mode
- Inbound calls rerouted through PSTN to local site when Zoom cloud is unreachable
- Forwarding rules must be configured before an outage; enabling is a manual step during outage

## Related

_None yet_
