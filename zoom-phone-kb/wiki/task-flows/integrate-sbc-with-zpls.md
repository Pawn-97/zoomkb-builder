---
type: task-flow
product: zoom-phone
title: Integrate SBC with ZPLS
sources:
  - article_id: KB0085804
    title: Configuring Zoom Phone Local Survivability with a Session Border Controller (SBC)
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085804
confidence: high
last_reviewed: 2026-05-18
---

# Integrate SBC with ZPLS

## Summary

The administrator locates the SBC in the BYOC Configuration area and enters the SBC's Survivability IP Address. The interface must make clear that in most deployments the internal IP (RFC1918) should be used, as the SBC communicates directly with ZPLS on the local network. This is a critical detail that, if misunderstood, could cause integration failure.

## Key points

- Navigate: Number Management > BYOC Configuration > Session Border Controllers > Manage
- Select SBC, scroll to Survivability IP Address section, enter SBC's internal IP
- In most deployments, use internal/RFC1918 IP for local network communication
- Ports and protocols must be allowed per network requirements

## Related

_None yet_
