---
type: concept
product: zoom-phone
title: Automatic Failover via SBC
sources:
  - article_id: KB0085804
    title: Configuring Zoom Phone Local Survivability with a Session Border Controller (SBC)
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085804
confidence: high
last_reviewed: 2026-05-18
---

# Automatic Failover via SBC

## Summary

The SBC monitors Zoom cloud connectivity via OPTIONS ping requests and automatically redirects calls to ZPLS when the cloud returns SIP 503 or ping failures. This failover is transparent to end users. Designers should note that the failover trigger conditions (OPTIONS ping failure, SIP 503) are technical indicators that may need to be abstracted into user-friendly status displays.

## Key points

- OPTIONS ping failure to Zoom primary and secondary triggers failover
- SIP 503 Service Unavailable response also triggers failover
- Automatic -- no admin intervention required for failover itself
- SBC must be configured with ZPLS node IP for local network routing

## Related

_None yet_
