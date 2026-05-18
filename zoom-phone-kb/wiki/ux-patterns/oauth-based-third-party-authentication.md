---
type: ux-pattern
product: zoom-phone
title: OAuth-Based Third-Party Authentication
sources:
  - article_id: KB0084151
    title: Using the Zoom Phone for Zapier integration
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084151
confidence: high
last_reviewed: 2026-05-18
---

# OAuth-Based Third-Party Authentication

## Summary

Zoom Phone connects to Zapier via a standard OAuth flow: the user is redirected to a Zoom sign-in page in a new browser tab/window, reviews requested permissions, and grants access. The Shared Access checkbox is presented during this consent step for account-wide scope.

## Key points

- New browser tab/window for OAuth sign-in
- Permission consent screen with explicit Allow button
- Shared Access checkbox embedded in consent flow
- After authentication, user returns to Zapier to continue building the Zap

## Related

- [[shared-access]]
- [[zoom-phone-for-zapier-integration]]
