---
type: constraint
product: zoom-phone
title: Caller Name and ID Always Shared
sources:
  - article_id: KB0084608
    title: Configuring caller data sharing between Zoom Phone and Zoom Contact Center
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084608
confidence: high
last_reviewed: 2026-05-18
---

# Caller Name and ID Always Shared

## Summary

The caller name and caller ID are non-optional -- they are always included in all transferred calls regardless of policy configuration. This baseline ensures agents always have minimal caller identification, but designers should make this mandatory behavior clear in the configuration UI to avoid confusion about why these fields cannot be toggled off.

## Key points

- Caller name and caller ID are always passed with transferred calls
- Cannot be disabled or hidden by policy configuration

## Related

- [[transferring-call-data-policy]]
