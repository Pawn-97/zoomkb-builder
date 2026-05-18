---
source_type: zoom_support_article
product: zoom-phone
article_id: KB0085809
title: Configuring Zoom Phone Local Survivability with a Node group
source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085809
captured_at: 2026-05-18T08:37:59.186389+00:00
retrieval_tool: jsonld
relevance_score: 15
confidence: high
content_hash: sha256:f8e3da243de85ea0c426cb2258d4a18b44cc8e5cd9a40792b3da571c69d29e6c
status: raw
---

# Configuring Zoom Phone Local Survivability with a Node group

Zoom Phone Local Survivability (ZPLS) can support up to 100,000 users through the addition of multiple modules within a node group. Node groups can be configured with redundancy to ensure continuous operation if individual modules fail, maintaining service availability across the entire group. With redundancy enabled, a node group configured with 20 ZPLS modules can support up to 50,000 users.

### Requirements for configuring Zoom Phone Local Survivability with a Node group

  * Business, Education, or Enterprise account
  * Zoom Node subscription
  * Zoom Phone subscription
  * Account owner or admin privilege
  * A deployed instance of the[ Zoom Phone Local Survivability service](https://support.zoom.com/hc?id=zm_kb&sysparm_article=KB0061895)
  * [Zoom Phone Local Survivability](https://support.zoom.com/hc?id=zm_kb&sysparm_article=KB0062795) enabled
  * A [Session Border Controller configured with ZPLS](https://support.zoom.com/hc/article?id=zm_kb&sysparm_article=KB0085804)



## Table of Contents

  * How to create a node group
  * How to assign a Node group to a site and a Survivability route group
  * How to validate the Local Survivability configuration has been updated to the Zoom client



## How to create a node group

  1. Sign in to the Zoom web portal as an administrator with privileges to edit account settings.
  2. In the navigation menu, click **Phone System Management** , then select **Company Info**.
  3. Click the **Account Settings** tab.
  4. Under the **Zoom Node** section, click **Manage** next to **Local Survivability**.
  5. Select the **Node groups** tab.
  6. Click **New** to create a new node group.
  7. Enter a **Group Name** for the node group. Optionally, add a **Description** to provide additional context.
  8. Enable the **Redundancy** option if high availability is required for this node group.
  9. Click **Save**
  10. On the **Node group** detail page, add the ZPLS modules that will be part of this node group by clicking **Add**. You can add up to 20 ZPLS modules to the list.  
**Note** : You can only add ZPLS modules that are currently unassigned - meaning they are not already associated with a **Site** or another **Node group**.
  11. If **Redundancy** is enabled, select **Backup nodes** from the list.  
**Note:** For redundancy to function properly, backup nodes should be configured in a 2:1 ratio with primary nodes. This means that for every 2 ZPLS primary nodes, there must be at least 1 ZPLS backup node.



## How to assign a Node group to a site and a Survivability route group

  1. Sign in to the Zoom web portal as an admin with the privilege to edit account settings.
  2. In the navigation menu, click **Phone System Management** , then click **Company Info**.
  3. Click **Account Settings**.
  4. Under **Zoom Node** , locate **Local Survivability**.
  5. Click **Manage** and select the**Node groups** tab
  6. Scroll to the right and click "…" and select **Edit**
  7. In the window that appears, click **Edit**.
  8. Select the **Site** where you want to use the ZPLS.
  9. Select the **Route Group** that was created and that will be used by ZPLS.
  10. Click **Save.**



**Note** : When a Node group is assigned to a site, users and common areas are automatically distributed across individual ZPLS nodes using a round-robin strategy. The Zoom cloud manages this distribution to ensure optimal balance across nodes. This assignment process is automated and cannot be manually controlled or modified through the administration portal.

## How to validate the Local Survivability configuration has been updated to the Zoom client

To verify that the ZPLS Node IPs have been successfully updated on the Zoom client, follow these steps:

  1. Log in to the Zoom client.
  2. Click on your profile picture in the top right corner and select **Settings**.
  3. Navigate to the **Statistics** tab, then select the **Phone** tab.
  4. Confirm that the Local Survivability status shows **Configured** and verify that the displayed IP address is correct.  
**Note:** The status will change from **Configured** to **Registered** once the Zoom client successfully registers with ZPLS.



Once validation is complete, it is recommended that the [configuration be fully tested with a simulated failover](https://support.zoom.com/hc/article?id=zm_kb&sysparm_article=KB0064538#h_01GSB5J7GG7MD2Y3ZPHCYP2D36).
