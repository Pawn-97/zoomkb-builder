---
type: user-role
product: zoom-phone
title: Account Owner / Administrator
sources:
  - article_id: KB0085762
    title: Manually synchronizing data in Zoom Phone Local Survivability
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085762
  - article_id: KB0085763
    title: Deploying the Call Bridge service for Zoom Phone Local Survivability
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085763
  - article_id: KB0085766
    title: Configuring call forwarding for Zoom Phone Local Survivability
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085766
  - article_id: KB0085804
    title: Configuring Zoom Phone Local Survivability with a Session Border Controller (SBC)
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085804
  - article_id: KB0085809
    title: Configuring Zoom Phone Local Survivability with a Node group
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085809
confidence: high
last_reviewed: 2026-05-18
conflict_flag: multiple-sources
---

# Account Owner / Administrator

## Summary

The only role that can configure call forwarding mappings and enable forwarding during an outage. This places a critical burden on admins during emergency situations -- they must be able to quickly access the portal and execute the enable workflow. Designers should prioritize discoverability and speed of the enable action.

## Key points

- Requires account owner or admin privileges
- Must have permission to edit account settings
- Accessed via Phone System Management > Company Info
- Requires account owner or admin privileges with edit access
- Must access both Node Management and Phone System Management interfaces
- Task spans two separate admin workflows (deploy and assign)
- Configures forwarding rules before outage (planning phase)
- Manually enables forwarding during outage (emergency phase)
- Accesses Number Management > BYOC Configuration for SBC and route group setup
- Multiple configuration areas: SBC details, route groups, routing rules
- Creates node groups, enables redundancy, adds modules
- Assigns groups to sites and route groups
- Cannot manually control user distribution (automated round-robin)

## Related

_None yet_
