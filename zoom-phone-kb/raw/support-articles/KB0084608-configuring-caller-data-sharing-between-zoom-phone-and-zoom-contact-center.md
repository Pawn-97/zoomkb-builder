---
source_type: zoom_support_article
product: zoom-phone
article_id: KB0084608
title: Configuring caller data sharing between Zoom Phone and Zoom Contact Center
source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084608
captured_at: 2026-05-18T09:09:03.399800+00:00
retrieval_tool: jsonld
relevance_score: 29
confidence: high
content_hash: sha256:4fbb4b6956e477447dfbf26ebb9526ca5c7e590b48adf21ad6cdff2ba119eacb
status: raw
---

# Configuring caller data sharing between Zoom Phone and Zoom Contact Center

Account owners and admins can configure what caller information is shared when transferring calls from Zoom Phone to Zoom Contact Center through the **Transferring Call Data** policy. The configurable data includes original caller information, transfer initiator details, and conversation summaries. Zoom Contact Center agents can view detailed caller information when receiving transferred calls from Zoom Phone users, queues, auto receptionists, or shared line groups. Zoom Contact Center agents receive this enriched information on incoming engagement notifications, active engagements, and completed engagement records.

By default, all available data is shared with Zoom Contact Center. This enhancement enables agents to better understand caller context and provide more informed support during transferred calls.

### Requirements for configuring caller data sharing

  * Account owner or admin privileges
  * Either a Zoom Workplace license with Phone included, or a standalone Zoom Phone calling plan
  * Zoom Contact Center license



## Table of Contents

  * How to configure the Transferring Call Data policy
    * Configure the Transferring Call Data policy for Zoom Phone
    * Configure the Transferring Call Data policy for Zoom Contact Center
  * How Contact Center agents view caller information
    * Incoming engagement notifications
    * Active engagements
    * Completed engagement records



## How to configure the Transferring Call Data policy

The **Transferring Call Data** policy allows you to control what information is sent from Zoom Phone when transferring calls to Contact Center or external parties. The caller name and caller ID are always included in all transferred calls.

**Note:** By default, all available data is shared with Zoom Contact Center.

### Configure the Transferring Call Data policy for Zoom Phone

  1. Sign in to the Zoom web portal as an admin with the privilege to edit account settings.
  2. In the navigation menu, click **Phone System Management** then **Company Info**.
  3. At the top of the page, click **Account Settings**.
  4. Click the **Settings** tab.
  5. In the **Preference** section, under the **Transferring call data to Contact Center** setting, select the **Conversation summary** checkbox to enable it. Deselect the checkbox to disable it.
  6. Click **Save** to apply changes.



### Configure the Transferring Call Data policy for Zoom Contact Center

Send certain information from Contact Center when transferring voice calls to Zoom Phone. The caller name or caller ID will be passed to all calls transferred to Zoom Phone.

  1. Sign in to the Zoom web portal as an admin with the privilege to edit account settings.
  2. In the navigation menu, click **Contact Center Management** then **Preferences**.
  3. Click the **Account** tab.
  4. In the **Voice and Video Engagements** section, under the **Transferring Call Data** setting, select from the following data options: 
     * **Original caller information** (always available)
     * **Transfer initiator**
       * **Agent name**
       * **Queue name**
     * **Consumer Sentiment**
     * **Conversation Summary**
     * **CRM ticket info  
Note**: If selected, click **Manage Variable** to choose the variables that will be passed on to Zoom Phone calls during the transfer, then click **Save**.
     * **Variables  
****Note** : If selected, click **+ Add variable(s)** to choose the variables that will be passed on to Zoom Phone calls during the transfer, then click **Save**.
     * **Address book custom fields  
Note**: If selected, click **+ Add custom field(s)** to choose the address book custom fields that will be passed on to Zoom Phone calls during the transfer, then click **Save**.
  5. Click **Save** to apply your changes.
  6. (Optional) To prevent all users in your account from changing this setting, click the lock icon , and then click **Lock** to confirm the setting.



## How Contact Center agents view caller information

Contact Center agents receive enriched caller information when calls are transferred from Zoom Phone users, queues, auto receptionists, or shared line groups. This information appears in three locations:

### Incoming engagement notifications

When receiving a transferred call from Zoom Phone, Contact Center agents see:

  * **Consumer information** : 
    * If the caller is a Contact Center address book contact: Both name and phone number
    * If the caller is not a Contact Center address book contact: Caller ID name and number
  * **Transfer initiator information** (if configured): 
    * From Zoom Phone user: User name, extension, and DID (if available)
    * From Zoom Phone queue: Queue name, extension, and DID (if available)
    * From auto receptionist: Auto receptionist name, extension, and DID (if available)
    * From shared line group: Shared line group name, extension, and DID (if available)
  * **IVR input** : Caller's menu selections if transferred directly from an auto receptionist
  * **Conversation summary** : Summary of the conversation between the caller and Zoom Phone user (if transferred from a user)



### Active engagements

While engaging with the consumer, agents can view all the same information listed above if they didn't have time to review it before accepting the engagement or if the engagement was auto-accepted.

### Completed engagement records

After the engagement ends, agents and supervisors can view the caller context information in the completed engagement records, including:

  * Consumer name or caller ID (name and number)
  * Transfer initiator information (based on admin configuration)
  * CRM ticket information (if available and related to the caller)



This enriched information helps agents better understand caller context and provide more informed support during transferred calls.
