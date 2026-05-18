---
type: task-flow
product: zoom-phone
title: Configure Call Forwarding Numbers
sources:
  - article_id: KB0085766
    title: Configuring call forwarding for Zoom Phone Local Survivability
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085766
confidence: high
last_reviewed: 2026-05-18
---

# Configure Call Forwarding Numbers

## Summary

A pre-outage planning workflow where admins define the source-to-destination number mappings. The interface uses an Add dialog with Source Number(s) and Destination Number selectors. With support for multiple source types (Users, Common Area Phones, Share Line Groups, Call Queues, Auto Receptionists), the source selector must handle grouped/filtered selection. The disabled-by-default state means admins should be prompted to review and enable individual entries after saving.

## Key points

- Navigate: Phone System Management > Company Info > Site > Settings > Zoom Node > Call Forwarding Local Survivability > Manage > Add
- Select Source Number(s) from multiple entity types, then Destination Number from BYOC pool
- Multiple source numbers can map to one destination
- Default forwarding status is disabled after save; must be explicitly enabled
- Main company number excluded from source selection

## Related

_None yet_
