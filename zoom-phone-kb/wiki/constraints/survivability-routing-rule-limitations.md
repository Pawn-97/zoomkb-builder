---
type: constraint
product: zoom-phone
title: Survivability Routing Rule Limitations
sources:
  - article_id: KB0085804
    title: Configuring Zoom Phone Local Survivability with a Session Border Controller (SBC)
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085804
confidence: high
last_reviewed: 2026-05-18
---

# Survivability Routing Rule Limitations

## Summary

During survivability mode, routing rules have reduced functionality: the Routing Path is ignored (only number translations apply), and the 'Other sites' routing path only supports same-site extension calls. These limitations mean the admin portal should clearly indicate which routing features are available in survivability vs. normal mode.

## Key points

- Routing Path (SIP Group/PSTN) ignored during survivability
- Number translations are preserved and still apply
- Other sites routing path: only same-site extension calls supported

## Related

- [[survivability-routing-rules]]
