---
type: task-flow
product: zoom-phone
title: Validate ZPLS Configuration on Zoom Client
sources:
  - article_id: KB0085809
    title: Configuring Zoom Phone Local Survivability with a Node group
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085809
confidence: high
last_reviewed: 2026-05-18
---

# Validate ZPLS Configuration on Zoom Client

## Summary

An end-user validation workflow where users check the Zoom client to confirm ZPLS is configured correctly. The status starts as Configured and changes to Registered upon successful connection. This flow is located in the Statistics > Phone tab, which is a technical/debug location rather than a user-facing status area. Designers should consider surfacing ZPLS status in a more visible location.

## Key points

- User logs into Zoom client, opens profile picture menu > Settings > Statistics > Phone tab
- Verifies Local Survivability status shows Configured (initial) or Registered (connected)
- Confirms displayed IP address is correct
- Recommended follow-up: simulated failover testing

## Related

- [[zoom-client-zpls-validation]]
- [[zpls-node-group]]
