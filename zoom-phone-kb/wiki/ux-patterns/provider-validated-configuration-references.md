---
type: ux-pattern
product: zoom-phone
title: Provider-Validated Configuration References
sources:
  - article_id: KB0085804
    title: Configuring Zoom Phone Local Survivability with a Session Border Controller (SBC)
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085804
confidence: high
last_reviewed: 2026-05-18
---

# Provider-Validated Configuration References

## Summary

The article references tested configuration guides from specific SBC providers (Audiocodes, Oracle, Ribbon). This external validation pattern means the Zoom admin interface does not need to provide SBC-specific configuration -- instead it can link to provider documentation. This is an intentional design decision to keep the Zoom UI hardware-agnostic.

## Key points

- SBC device configuration handled via provider-specific guides, not Zoom UI
- Zoom admin portal focuses on logical association (IP, route groups) only
- Provider guides referenced for Audiocodes, Oracle, and Ribbon SBCs

## Related

_None yet_
