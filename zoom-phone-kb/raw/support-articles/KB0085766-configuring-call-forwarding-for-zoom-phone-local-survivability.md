---
source_type: zoom_support_article
product: zoom-phone
article_id: KB0085766
title: Configuring call forwarding for Zoom Phone Local Survivability
source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085766
captured_at: 2026-05-18T09:08:53.995941+00:00
retrieval_tool: jsonld
relevance_score: 36
confidence: high
content_hash: sha256:60b351bdf6d417145aea6cef83c335453975370dbf4ce7e3f231865cb150178f
status: raw
---

# Configuring call forwarding for Zoom Phone Local Survivability

### Requirements for configuring call forwarding for Zoom Phone Local Survivability

  * Business, Education, or Enterprise account
  * Zoom Node subscription
  * Zoom Phone subscription
  * Account owner or admin privilege
  * A deployed Zoom Phone Local Survivability service module



## Table of Contents

  * How to configure call forwarding and BYOC numbers for ZPLS
    * Configure Call Forwarding numbers
  * How to enable call forwarding for Zoom Phone Local Survivability



## How to configure call forwarding and BYOC numbers for ZPLS

To invoke Call Forwarding Local Survivability of native Zoom Phone numbers (or Provider Exchange numbers) to users and devices located within the site undergoing an outage, BYOC numbers associated with the PSTN connection attached to the survivability SBC must be acquired. The number of BYOC extensions required is determined by the number of unique extensions needed during a failover.

For example, if 100 users require a Direct Inward Dial service during an outage, 100 extensions must be acquired from the BYOC provider, and 100 Zoom Native numbers can subsequently be forwarded to those 100 BYOC numbers.

**Note** : Zoom Native numbers can only be forwarded to BYOC numbers assigned to users within the 

Site that is being configured for Call forwarding Local Survivability.

In addition to Call Forwarding, at least one BYOC number is required for emergency services support. This unique BYOC number can be configured as the Emergency Location Identification Number (ELIN) for the specific Site and must not be assigned to any user or Zoom Phone entity.

### Configure Call Forwarding numbers

Before any outage, administrators should set up call-forwarding logic to determine how Zoom Native numbers are redirected during an outage. To set up call forwarding:

  1. Sign in to the Zoom web portal as an admin with the privilege to edit account settings.
  2. In the navigation menu, click **Phone System Management** , then click **Company Info**.
  3. Click the name of the desired **Site**.
  4. Click the **Settings** tab.
  5. Under **Zoom Node** , navigate to the **Call Forwarding Local Survivability** setting.
  6. Click **Manage**.
  7. Click **Add**.
  8. For the **Source Number(s)** , select the numbers being forwarded (can be a number or extension assigned to Users, Common Area Phones, Share Line Groups, Call Queues, and Auto Receptionists).  
**Note** : Multiple source numbers can be forwarded to a single destination number.
  9. For the **Destination Number** , select the [BYOC numbers enabled for Local Survivability](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0063728#h_01GSB46AYAVD8RRBFTV7QJDGJR) that have been assigned to users within the site.
  10. Click **Save**.  
**Note** : By default, the forwarding status of each source number is disabled. The main company number cannot be configured for Call Forwarding Local Survivability



## How to enable call forwarding for Zoom Phone Local Survivability

During an outage, admins will need to access the web portal and enable Call Forwarding for the selected numbers (the **Select All** option can be utilized to enable forwarding for all defined S**ource Numbers**). To enable **Call Forwarding Local Survivability** :

  1. Sign in to the Zoom web portal as an admin with the privilege to edit account settings.
  2. In the navigation menu, click **Phone System Management** , then click **Company Info**.
  3. Click on the name of the desired **Site**.
  4. Click the **Settings** tab.
  5. Under **Zoom Node** , navigate to the **Call Forwarding Local Survivability** setting.
  6. Click **Manage**.
  7. Click **Enable Forwarding**.



Call Forwarding Local Survivability enables calls to Zoom-provided phone numbers (or Provider Exchange numbers) to be automatically forwarded to BYOC-P numbers when the system enters survivability mode. During an internet outage, incoming calls are rerouted through the PSTN network to the local site where ZPLS is configured, ensuring uninterrupted call handling even without internet connectivity.

To maintain call availability during internet outages, ensure that your PSTN services and local site internet connection use separate network infrastructure. If both services share the same local loop network, an outage will affect both systems simultaneously.
