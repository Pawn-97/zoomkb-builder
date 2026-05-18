---
type: concept
product: zoom-phone
title: ZPLS Node Group
sources:
  - article_id: KB0085809
    title: Configuring Zoom Phone Local Survivability with a Node group
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085809
confidence: high
last_reviewed: 2026-05-18
---

# ZPLS Node Group

## Summary

A form-based creation workflow where admins name the group, optionally add a description, enable redundancy, and add ZPLS modules. The interface lists only unassigned modules, preventing configuration errors. When redundancy is enabled, backup node selection appears with the 2:1 ratio requirement. This is a multi-step setup where later steps depend on earlier selections.

## Key points

- Supports up to 20 ZPLS modules in a single group
- Capacity scales: supports up to 100,000 users without redundancy, 50,000 with redundancy
- Users and common areas automatically distributed across nodes via round-robin
- Only unassigned modules (not tied to a site or other group) can be added
- Navigate: Phone System Management > Company Info > Account Settings > Zoom Node > Local Survivability > Manage > Node groups tab > New
- Enter Group Name, optional Description, enable Redundancy toggle
- Add up to 20 unassigned ZPLS modules
- If redundancy enabled, select backup nodes at 2:1 ratio

## Related

- [[node-group-redundancy]]
- [[zpls-node-group]]
