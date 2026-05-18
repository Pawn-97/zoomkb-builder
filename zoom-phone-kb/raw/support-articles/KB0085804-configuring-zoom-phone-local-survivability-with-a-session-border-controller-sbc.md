---
source_type: zoom_support_article
product: zoom-phone
article_id: KB0085804
title: Configuring Zoom Phone Local Survivability with a Session Border Controller (SBC)
source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085804
captured_at: 2026-05-18T08:38:00.602327+00:00
retrieval_tool: jsonld
relevance_score: 23
confidence: high
content_hash: sha256:dd4801e252098bd0ba1198671109e0dce6ed11b155f60d780eb8a168122937f9
status: raw
---

# Configuring Zoom Phone Local Survivability with a Session Border Controller (SBC)

Zoom Phone Local Survivability (ZPLS) can connect to a customer-provided Session Border Controller (SBC) to maintain PSTN services and third-party system connectivity during outages. When integrated with an SBC, both inbound and outbound calls are routed through the SBC to PSTN SIP trunks.

Additionally, customers can integrate third-party PBX systems through the SBC, enabling seamless dialing between ZPLS and these external systems even during service disruptions.

To ensure optimal call handling in normal mode, it is recommended to integrate the SBC with Zoom using a [BYOC-P (Bring Your Own Carrier - Premises) configuration](https://support.zoom.com/hc/article?id=zm_kb&sysparm_article=KB0079203#mcetoc_1iisfgan27h). This setup allows phone number calls to be processed through the standard Zoom cloud infrastructure. When connectivity to the Zoom cloud is lost, calls will automatically be rerouted to the ZPLS (Zoom Phone Local Survivability) system to maintain service continuity.

### Requirements for configuring Zoom Phone Local Survivability with a Session Border Controller (SBC)

  * Business, Education, or Enterprise account
  * Zoom Node subscription
  * Zoom Phone subscription
  * Account owner or admin privilege
  * A deployed instance of the [Zoom Phone Local Survivability service](https://support.zoom.com/hc?id=zm_kb&sysparm_article=KB0061895)
  * [Multiple Sites](https://support.zoom.com/hc/article?id=zm_kb&sysparm_article=KB0069716) is enabled for Zoom Phone
  * Session Border Controller meets the [general SBC requirements](https://support.zoom.com/hc/article?id=zm_kb&sysparm_article=KB0079203#mcetoc_1iisfgan27h)



## Table of Contents

  * Considerations when configuring a SBC with Zoom Phone Local Survivability
    * Default configuration
    * SBC connectivity to ZPLS
  * How to integrate an SBC with Zoom Phone Local Survivability
  * How to create a Route group for Zoom Phone Local Survivability
  * How to configure routing rules for Zoom Phone Local Survivability
  * How to configure the Emergency number pool for survivability mode
  * How to configure the Outbound Caller ID for non BYOC-P users/devices



## Considerations when configuring a SBC with Zoom Phone Local Survivability

### Default configuration

When a Session Border Controller (SBC) is integrated with both Zoom cloud (primary and secondary destinations) and ZPLS (tertiary destination), proper configuration is essential to ensure automatic call re-routing during Zoom cloud connectivity failures. The SBC should be configured to automatically redirect calls to ZPLS under the following conditions:

  1. OPTIONS ping requests from the SBC to both Zoom primary and secondary destinations fail
  2. Zoom Cloud returns a SIP 503 Service Unavailable response



The following providers have provided tested and validated configuration guides for ZPLS:

  * [Audiocodes](https://www.audiocodes.com/media/membqkr1/mediant-800c-sbc-with-zoom-phone-local-survivability-deployment-guide.pdf)
  * [Oracle](https://www.oracle.com/a/otn/docs/zoomphonelocalsurvivabiltyvga1.0.pdf)
  * [Ribbon](https://publicdoc.rbbn.com/spaces/IOT/pages/548733043/Ribbon+SBC+Edge+R12.2+Interop+with+Zoom+Phone+Local+Survivability+Interoperability+Guide)



### SBC connectivity to ZPLS

**Single Node:** When configuring the SBC to route traffic to ZPLS, ensure that the SBC is configured with the ZPLS node IP address. This prevents outages that may occur due to internet failures.

**Node Group:** When configuring the SBC to route traffic to a node group, ensure it routes traffic to at least 2 ZPLS node IP addresses. This configuration eliminates a single point of failure if the primary node in the node group fails.

## How to integrate an SBC with Zoom Phone Local Survivability

  1. In the navigation menu, click **Number Management** , then **BYOC Configuration**.
  2. To the right of **Session Border Controllers** , click **Manage**.
  3. Locate the **Session Border Controllers** that will be integrated with ZPLS
  4. Click on the **Name** of the Session Border Controller
  5. Scroll down to the **Survivability IP Address section** and enter the IP address of the SBC.  
**Note:** In most deployments, the SBC communicates directly with the ZPLS module on the customer's internal network. Enter the SBC's internal IP address (RFC1918) to be used to send traffic to the ZPLS module. Ensure that ports and protocols listed[ here](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058005) are allowed.
  6. Click **Save**



## How to create a Route group for Zoom Phone Local Survivability

  1. In the navigation menu, click **Number Management** , then **BYOC Configuration**
  2. To the right of **Route Groups** , click **Manage**.
  3. Select either the **Common** tab or the **Zoom Phone** tab, depending on your configuration needs. Most customers will use the **Common** tab.
  4. Click **Add**
  5. Enter a **Display Name** for the route group being created.
  6. Select **Survivability** as **Type**
  7. Select the **Session Border Controllers** that will be assigned to the Local Survivability module
  8. Click **Save****  
****Note** : Enable Options Ping in the Session Border Controller configuration to maintain continuous connectivity monitoring between the SBC and ZPLS.



## How to configure routing rules for Zoom Phone Local Survivability

**Note** : Typically, **Routing Rules** are used for customized call routing for BYOC-P in addition to preserving users’ legacy dialing habits. When routing rules are used by ZPLS, the Routing Path (SIP Group or PSTN) is ignored; however, number translations are preserved. During survivability mode, routing rules configured with the Routing Path "**Other sites** " are limited to calls between extensions within the same site only.

[Routing Rules](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0083637#mcetoc_1jbnf507o3a) used under normal conditions can be preserved while survivability is active.

  1. Sign in to the Zoom web portal as an admin with the privilege to edit account settings.
  2. In the navigation menu, click **Phone System Management** , then click **Company Info**.
  3. Click the name of the desired **Site**.
  4. Under the **Zoom Node** section, **Enable Routing Rules**.
  5. Click **Save**.  
**Note** : Routing Rules defined at the **Site** level can be preserved by ZPLS. Rules at the account level will not be preserved.



## How to configure the Emergency number pool for survivability mode

Each site can be configured with an **Emergency Number Pool** , which serves as the caller ID when users or devices without a BYOC number place calls to emergency services.

  1. Sign in to the Zoom web portal.
  2. In the navigation menu, click **Phone System Management** , then click **Company Info**.
  3. Click on the name of the desired **Site**.
  4. Click the **Settings** tab.
  5. Under **Zoom Node** , navigate to the **Emergency Number Pool** setting.
  6. Click **Add** and enter a**Display Name**
  7. Click **Add** next to **ELINs** to add BYOC-P numbers to the Emergency Number Pool
  8. Select a BYOC-P number from the list displayed.  
**Note** : The BYOC numbers must be unassigned. In addition, you can assign multiple numbers that will be used as outbound caller IDs when calling emergency services while in survivability mode.
  9. To verify the ELIN number, click **Phone System Management** , then click **Phone Numbers**.  
The BYOC number assigned as the ELIN will be displayed as assigned to Local Survivability.
  10. Select the users who will use this Emergency Number Pool.   
**Note** : If you don't select any users, all users at this site without a BYOC-P number will automatically use this pool. When no users or common area devices are selected, the interface will display as **Default**.
  11. Select the Common Areas that will use this Emergency Number Pool.   
**Note** : If no common areas are selected, all Common Areas at this site without a BYOC-P number will automatically use this pool.
  12. (Optional) If users or common area devices with BYOC-P numbers need to use numbers from the Emergency Number Pool, enable the option **Allow extensions with BYOC-P numbers to use ELINs as outbound caller ID for emergency calls.**



To ensure emergency services arrive at the correct location, customers must work with their BYOC-P PSTN carrier to assign emergency addresses to the phone numbers configured in the Emergency Number Pool. These addresses will be displayed to emergency personnel when a call reaches the Public Safety Answering Point (PSAP).

## How to configure the Outbound Caller ID for non BYOC-P users/devices

In some cases, not all users or common areas at a site have an assigned BYOC-P number. When this occurs, outbound calls through an SBC may fail. To maintain outbound calling functionality during an outage, you can assign an outbound caller ID at the site level for all users and devices. This approach ensures call continuity without requiring individual BYOC-P numbers for every user or device at the site.

  1. Sign in to the Zoom web portal.
  2. In the navigation menu, click **Phone System Management** , then click **Company Info**.
  3. Click on the name of the desired **Site**.
  4. Click the **Settings** tab.
  5. Under **Zoom Node** , navigate to the **Outbound Caller ID** section.
  6. Click on **Add BYOC-P number** and select a BYOC-P number from the list that is available.  
**Note** : To enable callbacks to this number, assign the BYOC-P to a Survivable Distribution Group. This ensures that calls are routed and handled correctly during survivability scenarios.
