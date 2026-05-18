---
type: constraint
product: zoom-phone
title: One Alert Per Target Per Rule Type
sources:
  - article_id: KB0075917
    title: Managing Zoom Phone Appliance device monitoring
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0075917
confidence: high
last_reviewed: 2026-05-18
---

# One Alert Per Target Per Rule Type

## Summary

For each rule type (Devices go offline, Devices go online, Offline Devices Rate), only one alert can be created per target. This prevents duplicate alerts but means the UI must enforce this constraint during alert creation, either by hiding ineligible options or showing an inline error.

## Key points

- Single alert per rule type per target (e.g., cannot create two 'Devices go offline' alerts for the same device)
- Attempting to create a duplicate should be prevented or clearly flagged in the UI

## Related

- [[alert-targets]]
