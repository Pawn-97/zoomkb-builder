---
type: ux-pattern
product: zoom-phone
title: Two-Phase Service Setup Pattern (Deploy then Assign)
sources:
  - article_id: KB0085763
    title: Deploying the Call Bridge service for Zoom Phone Local Survivability
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085763
confidence: high
last_reviewed: 2026-05-18
---

# Two-Phase Service Setup Pattern (Deploy then Assign)

## Summary

The Call Bridge follows a two-phase setup: first deployment via Node Management (a technical infrastructure step), then assignment via Phone System Management (a business configuration step). This separation of concerns is logical but creates a disjointed experience across two admin areas. Designers should consider whether a unified wizard or post-deployment prompt would improve completion rates.

## Key points

- Phase 1: Node Management > Modules > Services tab (infrastructure)
- Phase 2: Phone System Management > Company Info (business configuration)
- Assignment step explicitly prompts manual data sync as final action
- Two separate navigation paths; no wizard connecting them

## Related

- [[zpls-data-synchronization]]
