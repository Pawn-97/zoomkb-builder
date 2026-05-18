---
type: task-flow
product: zoom-phone
title: Configure Transferring Call Data Policy for Zoom Contact Center
sources:
  - article_id: KB0084608
    title: Configuring caller data sharing between Zoom Phone and Zoom Contact Center
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084608
confidence: high
last_reviewed: 2026-05-18
---

# Configure Transferring Call Data Policy for Zoom Contact Center

## Summary

Admins configure which data fields are shared when Contact Center transfers calls to Zoom Phone. This is a more complex configuration with multiple data options (original caller info, transfer initiator details with sub-options, consumer sentiment, conversation summary, CRM ticket info, variables, address book custom fields) and sub-configuration flows for CRM variables and custom fields. The complexity here suggests a need for progressive disclosure in the admin UI.

## Key points

- Navigate to Contact Center Management > Preferences > Account tab
- Select from data options: Original caller information (always available), Transfer initiator (agent name, queue name), Consumer Sentiment, Conversation Summary, CRM ticket info, Variables, Address book custom fields
- CRM ticket info, Variables, and Address book custom fields each have sub-configuration modals for selecting specific fields
- Optional locking prevents all users from changing the setting

## Related

- [[configure-transferring-call-data-policy-for-zoom-phone]]
- [[transferring-call-data-policy]]
