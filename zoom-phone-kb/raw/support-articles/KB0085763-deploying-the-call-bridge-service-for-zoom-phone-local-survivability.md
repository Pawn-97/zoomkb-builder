---
source_type: zoom_support_article
product: zoom-phone
article_id: KB0085763
title: Deploying the Call Bridge service for Zoom Phone Local Survivability
source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085763
captured_at: 2026-05-18T09:08:55.509661+00:00
retrieval_tool: jsonld
relevance_score: 15
confidence: high
content_hash: sha256:09c148743a2db55850b6e318996f0acd8df8f1d20e5ba5650c60e6df09963095
status: raw
---

# Deploying the Call Bridge service for Zoom Phone Local Survivability

The Call Bridge (also known as Shared Database Nodes) enables call routing between ZPLS modules or node groups during internet outages, allowing users and devices at different sites to communicate while in survivability mode. To ensure functionality during network failures between customer locations and Zoom data centers, the Call Bridge must be deployed on a standalone Node server that remains accessible to all ZPLS modules. The Call Bridge synchronizes state information across ZPLS modules while allowing users to dial between sites even when connectivity to Zoom's cloud infrastructure is unavailable.

The Call Bridge service is supported in the following cases:

  * ZPLS Node to ZPLS Node Group communication
  * ZPLS Node to ZPLS Node communication
  * ZPLS Node Group to ZPLS Node Group communication



**Note** : Communication between ZPLS nodes within a Node group does not require a Call Bridge.

When deploying the Call Bridge service, it's important to consider the resiliency of your network topology. During survivability mode, calls between users registered to different ZPLS nodes or node groups rely on the Call Bridge to route traffic correctly. Specifically, when a user on one ZPLS node attempts to call a user on another ZPLS node or node group, the originating node must query the Call Bridge to determine the destination node's location. If connectivity to the Call Bridge is lost, the originating node cannot identify the destination node, resulting in a call failure.

### Requirements for manually synchronizing data with Zoom Phone Local Surviability

  * Business, Education, or Enterprise account
  * Zoom Node subscription
  * Zoom Phone subscription
  * Account owner or admin privilege
  * A deployed Zoom Phone Local Survivability service module



## Table of Contents

  * How to deploy the Call Bridge service
  * How to assign a Call Bridge to a Local survivability module or Node group



## How to deploy the Call Bridge service

Once the ZPLS service has been deployed and registered, the Call Bridge module can be deployed on the server.

  1. Sign in to the [Zoom Web Portal](https://zoom.us/signin). 
  2. In the navigation menu, click**Node Management,** then click **Modules**.
  3. Click the drop-down button , and click **Phone Local Survivability**.
  4. Click the **Services** tab.
  5. Click **Add Services**.
  6. In the new dialog window, click **Call Bridge**.
  7. In the next window, fill in the following information 
     * **Install on a node:** Select the Zoom Node Phone server where the module will be deployed.
     * **Internal IP** : The internal IP address utilized for the module.   
**Note** : This address needs to be one that was assigned to the Node server during the initial configuration.
  8. (Optional) Add a prefix for the **Internal domain**.
  9. Click **Add**.



## How to assign a Call Bridge to a Local survivability module or Node group

  1. Sign in to the Zoom web portal as an admin with the privilege to edit account settings.
  2. In the navigation menu, click **Phone System Management** , then click **Company Info**.
  3. Click **Account Settings**.
  4. Under Zoom Node, locate **Local Survivability**.
  5. Navigate to **Shared database nodes**.
  6. Click the **More** icon  , then click **Edit**.
  7. Assign the ZPLS Node or Node Group by selecting it from the corresponding tab.
  8. Once the bridge has been assigned, [manually synchronize the data for ZPLS](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085762).
