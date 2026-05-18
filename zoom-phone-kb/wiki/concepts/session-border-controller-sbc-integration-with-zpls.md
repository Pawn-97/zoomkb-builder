---
type: concept
product: zoom-phone
title: Session Border Controller (SBC) Integration with ZPLS
sources:
  - article_id: KB0085804
    title: Configuring Zoom Phone Local Survivability with a Session Border Controller (SBC)
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085804
confidence: high
last_reviewed: 2026-05-18
---

# Session Border Controller (SBC) Integration with ZPLS

## Summary

A customer-provided Session Border Controller connects ZPLS to PSTN SIP trunks and third-party PBX systems, maintaining external call capabilities during Zoom cloud outages. The SBC acts as the bridge between the on-premises survivability network and the outside world. Designers should understand the SBC as a required hardware component that must be configured both on the device itself and within the Zoom admin portal.

## Key points

- Maintains PSTN and third-party PBX connectivity during outages
- Supports both inbound and outbound call routing through SIP trunks
- Requires dual configuration: physical SBC device + Zoom admin portal
- Third-party PBX systems can integrate through SBC for inter-system dialing

## Related

- [[survivability-route-group]]
- [[survivability-routing-rules]]
