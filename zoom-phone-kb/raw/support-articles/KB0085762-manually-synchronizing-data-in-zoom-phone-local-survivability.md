---
source_type: zoom_support_article
product: zoom-phone
article_id: KB0085762
title: Manually synchronizing data in Zoom Phone Local Survivability
source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085762
captured_at: 2026-05-18T09:08:52.743970+00:00
retrieval_tool: jsonld
relevance_score: 20
confidence: high
content_hash: sha256:1d7414befea4f57ceb0b43adede4f9af32ba8a563137514189325b35e2ce6871
status: raw
---

# Manually synchronizing data in Zoom Phone Local Survivability

Zoom Phone Local Survivability (ZPLS) is fully managed from the cloud, with configurations automatically synchronized to ZPLS nodes and node groups at regular intervals. Data synchronization is required whenever changes are made to the Local Survivability configuration. This includes adding new users, common areas, phone numbers, Survivable Distribution Groups, and other configuration updates.

Full data synchronization occurs in the following scenarios:

  * When a ZPLS node boots up with network connectivity available
  * Automatically every 10 hours for all ZPLS nodes
  * When an administrator manually initiates synchronization from the Zoom admin portal



### Requirements for manually synchronizing data with Zoom Phone Local Surviability

  * Business, Education, or Enterprise account
  * Zoom Node subscription
  * Zoom Phone subscription
  * Account owner or admin privilege
  * A deployed Zoom Phone Local Survivability service module



## Table of Contents

  * How to manually synchronize data with ZPLS



## How to manually synchronize data with ZPLS

**Note** : Manual synchronization is limited to once every 30 minutes

Administrators can initiate data synchronization manually directly from the Zoom admin portal by following the steps outlined below:

  1. Sign in to the Zoom web portal as an admin with the privilege to edit account settings.
  2. In the navigation menu, click **Phone System Management** , then click **Company Info**.
  3. Select the site that is assigned to the ZPLS node you want to sync.
  4. Click the **Settings** tab, and then scroll down to the **Zoom Node** section.
  5. Next to **Local Survivability** , click **Manage**.
  6. To sync the data, do one of the following: 
     * If syncing an individual ZPLS node, scroll down to the **Status** section and click **Sync.**
     * If syncing a ZPLS node group, scroll down to the **Site** section and click **Sync.**
