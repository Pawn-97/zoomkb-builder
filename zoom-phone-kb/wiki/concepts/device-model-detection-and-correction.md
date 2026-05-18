---
type: concept
product: zoom-phone
title: Device Model Detection and Correction
sources:
  - article_id: KB0083412
    title: Zoom Phone automatic device model detection and correction
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0083412
confidence: high
last_reviewed: 2026-05-18
---

# Device Model Detection and Correction

## Summary

An automated system that validates desk phone models against Zoom's certified device list and silently corrects incorrect model information. Designers should ensure that corrected device details propagate consistently across all web portal pages without requiring manual refresh.

## Key points

- Automatically detects and corrects incorrect model information for certified devices
- Corrections are reflected across all web portal pages without user intervention
- Non-certified devices trigger a persistent red warning message that cannot be dismissed
- Covers models from AudioCodes, Avaya, Cisco, Grandstream, Mitel, Poly, and Yealink

## Related

- [[certified-devices]]
- [[non-certified-device-warning]]
