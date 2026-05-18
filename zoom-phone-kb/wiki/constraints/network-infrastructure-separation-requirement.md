---
type: constraint
product: zoom-phone
title: Network Infrastructure Separation Requirement
sources:
  - article_id: KB0085766
    title: Configuring call forwarding for Zoom Phone Local Survivability
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085766
confidence: high
last_reviewed: 2026-05-18
---

# Network Infrastructure Separation Requirement

## Summary

PSTN services and the local site internet connection must use separate network infrastructure. If both share the same local loop, an outage will affect both simultaneously, defeating the purpose of survivability. This is a critical infrastructure constraint that should be communicated during setup.

## Key points

- PSTN and internet must use separate physical network infrastructure
- Shared local loop causes simultaneous failure during outages
- Administrator must verify this separation during deployment planning

## Related

- [[call-forwarding-local-survivability]]
