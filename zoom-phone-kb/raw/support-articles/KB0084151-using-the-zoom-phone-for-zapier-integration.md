---
source_type: zoom_support_article
product: zoom-phone
article_id: KB0084151
title: Using the Zoom Phone for Zapier integration
source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084151
captured_at: 2026-05-18T09:09:42.106981+00:00
retrieval_tool: jsonld
relevance_score: 19
confidence: high
content_hash: sha256:db206e9cd16e4599f5991ca7c3ed4aa6b13074b66c29ef2a94ba6fee1043a92e
status: raw
---

# Using the Zoom Phone for Zapier integration

Zoom Phone and Zapier can be connected to automate your phone-related actions. You can trigger actions when a phone call ends or when other actions like call recording, voicemail, and SMS are completed.

Users can integrate Zoom Phone with Zapier to automate workflows for call management and other phone activities. After authenticating their Zoom Phone account, they can connect it with Zapier-supported applications like CRMs, emails, etc., and configure trigger events such as incoming, outgoing, or missed calls, voicemails, and SMS messages. These triggers can automatically perform actions like creating CRM contacts with caller information, sending emails with call information, and so on. The integration supports multiple third-party applications and field mapping between Zoom Phone data and connected services, enabling better follow-ups, streamlined communication workflows, and reduced manual data entry.

### Requirements for using the Zoom Phone for Zapier integration

  * Either a Zoom Workplace license with Phone included, or a standalone Zoom Phone calling plan
  * Zapier has been added to your Zoom App Marketplace account
  * To trigger this integration for all users, you must be added as a user to the Zoom App Marketplace with either **User** with**Shared Access** or **Admin** permissions.



## Table of Contents

  * How to connect Zoom to Zapier
  * How to connect (authorize) your Zoom account to Zapier when creating a Zap
    * Available Zoom Phone trigger events
    * Available Zoom Phone action events
    * Available Zoom Phone fields
  * How to remove the Zapier for Zoom Phone app
  * How your data is used



## How to connect Zoom to Zapier

To create an app connection to Zoom on Zapier:

  1. [Access the Zapier Apps page](https://zapier.com/app/assets/connections/apps).
  2. Click **+ Add connection**.  
A new dialog box will appear.
  3. Search for and select **Zoom Phone for Zapier**.
  4. Click **Add connection**.  
A new browser tab or window will open.
  5. Sign in to Zoom to authenticate.
  6. If prompted, grant Zapier permission to access your account.
  7. To trigger for all users, select the **Allow this app to use the share access permissions** checkbox.



The Zapier app will be connected to Zoom Phone in the Zapier platform, enabling users to automate workflows and integrate with thousands of popular apps. With this integration, users can set up triggers to monitor events, such as new channel creations, mentions, or messages, and create workflows that automatically send channel or direct messages back into Zoom Phone.

## How to connect (authorize) your Zoom account to Zapier when creating a Zap

To use Zoom Phone in a Zap, you must first connect your Zoom account to Zapier.

  1. Sign in to [Zapier](https://zapier.com/app/home).
  2. Create a Zap. Learn more about [getting started with Zapier](https://zapier.com/resources/guides/quick-start/create-zap).
  3. In your Zap trigger or action, search for **Zoom Phone**.
  4. Select an event.
  5. In the **Account** tab, select **Connect a new account**.
  6. Sign in to Zoom, review the requested permissions, and click **Allow**.



### Available Zoom Phone trigger events

You can choose one of the trigger events from the Zoom Phone app in Zapier:

  * Phone call connected Event: Triggers when a phone call connects.
  * Phone call ended Event: Triggers when a phone call ends.
  * Phone call history completed Event: Triggers when a phone call is completed.
  * Phone call recording completed Event: Triggers when a phone call recording is completed.
  * Phone call voice mail received event: Triggers when voicemail is received.



### Available Zoom Phone action events

You can send an SMS to up to 10 recipients from the Zoom Phone app in Zapier, triggered by other Zapier-supported apps.

### Available Zoom Phone fields

The next app you choose in the Zap flow (for example, Gmail) can help you trigger an email with values from Zoom Phone, such as:

  * Callee Name
  * Caller Name
  * Forwarded By Name
  * Event
  * Call Id
  * Callee Extension Id
  * Callee Extension Number
  * Callee Extension Type
  * Callee Phone Number
  * Caller Extension Id
  * Caller Extension Number
  * Caller Extension Type
  * Caller Phone Number
  * Date Time
  * Direction



## **How to remove the Zapier for Zoom Phone app**

  1. Sign in to Zapier.
  2. [Access the **Manage Connections** page](https://zapier.com/app/connections).
  3. Select the **Zoom Phone** app.
  4. Delete your connected account(s).
  5. Sign in to the [Zoom App Marketplace](https://marketplace.zoom.us/) with your Zoom account.
  6. In the top-right corner of the page, click **Manage**.
  7. In the navigation menu, click **Added Apps**.
  8. Next to the **Zapier for Phone** app, click **Remove**.  
A pop-up window will appear.
  9. In the window, confirm the dialogue and click **Remove**.



## **How your data is used**

This integration accesses and uses the following information from your Zoom Phone account to automate workflows:

  * **Caller and Callee Identity Information** (Caller/Callee Name, Phone Number, Extension ID, Extension Number, Extension Type): This is used to identify the parties involved in a call and populate fields in third-party actions (e.g., inserting the Caller Name into a Gmail subject line).
  * **Call Metadata** (Call ID, Date Time, Direction, Forwarded By Name): This is used to provide specific context about the call instance when triggering automations or logging call history.
  * **Call Status Events** (Call connected, Call ended, Call history completed): This is used as triggers to initiate workflows immediately when a phone call begins, finishes, or when the call log is finalized.
  * **Media and Messaging Events** (Recording completed, Voicemail received): This is used to trigger actions specifically when a call recording finishes or a new voicemail is deposited.
  * **Account Authentication** : This is used to securely connect the specific Zoom user to the Zapier platform; credentials are encrypted and can be removed at any time.
