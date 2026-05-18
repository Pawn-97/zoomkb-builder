---
type: constraint
product: zoom-phone
title: Manual Sync Rate Limit
sources:
  - article_id: KB0085762
    title: Manually synchronizing data in Zoom Phone Local Survivability
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085762
confidence: high
last_reviewed: 2026-05-18
---

# Manual Sync Rate Limit

## Summary

Manual synchronization is capped at once every 30 minutes. This constraint should be reflected in the admin UI with a clear indication of when the next sync can be performed, preventing user confusion when the Sync button appears unresponsive.

## Key points

- Maximum one manual sync every 30 minutes
- No workaround available; automatic sync occurs every 10 hours otherwise
- UI must communicate sync availability status

## Related

- [[zpls-data-synchronization]]
