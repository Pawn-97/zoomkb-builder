---
type: concept
product: zoom-phone
title: Transfer Initiator Information
sources:
  - article_id: KB0084608
    title: Configuring caller data sharing between Zoom Phone and Zoom Contact Center
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084608
confidence: high
last_reviewed: 2026-05-18
---

# Transfer Initiator Information

## Summary

Metadata about the source of a transferred call, varying by whether the transfer came from a Zoom Phone user, queue, auto receptionist, or shared line group. Each source type provides different identifying fields, so the UI displaying this info must be flexible enough to show the right context for each scenario.

## Key points

- From Zoom Phone user: user name, extension, and DID (if available)
- From Zoom Phone queue: queue name, extension, and DID (if available)
- From auto receptionist: auto receptionist name, extension, and DID (if available)
- From shared line group: shared line group name, extension, and DID (if available)

## Related

- [[caller-data-enrichment]]
- [[transferring-call-data-policy]]
