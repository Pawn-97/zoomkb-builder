---
source_type: zoom_support_article
product: zoom-phone
article_id: KB0084977
title: Zoom Phone caller ID and routing issues
source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084977
captured_at: 2026-05-18T09:09:11.806842+00:00
retrieval_tool: jsonld
relevance_score: 41
confidence: high
content_hash: sha256:8a36c6ea51e67862378b30d8287199e8d729e3474b004045a88521b79517f3ad
status: raw
---

# Zoom Phone caller ID and routing issues

### **Limitations for Caller ID**

  * The +81 country code prefixes for Japanese numbers cannot be changed through Zoom Phone settings, as this is standard E.164 formatting. The display behavior may vary depending on the recipient's device, carrier, and phone settings.
  * The outbound caller ID dropdown has a maximum display limit of 100 phone numbers.



## Table of Contents

  * Issue
  * Environment
  * Cause
  * Resolution
    * Configure auto-receptionist caller ID to prevent call failures
    * Manage outbound caller ID selection for call queue members



## **Issue**

You may experience caller ID display and call routing configuration issues in Zoom Phone that affect how caller information appears to recipients and how calls are transferred or forwarded. Common symptoms include:

  * Original caller ID not displaying when calls are transferred to external numbers, showing the transferring number instead.
  * Caller ID appearing with international country code prefixes instead of local number format.
  * Auto receptionist caller ID settings causing intermittent call failures.
  * Outbound caller ID dropdown not displaying all available phone numbers when users are assigned to multiple call queues.
  * Users unable to select caller ID numbers from call queues they are not members of.
  * Call forwarding between separate corporate tenants not displaying original caller information.



## **Environment**

  * Zoom Phone service with call forwarding, transfer, and caller ID configuration features.
  * Auto receptionist and IVR systems with external number routing.
  * Call queues with multiple phone number assignments.
  * Multi-extension Zoom Phone deployments with call forwarding between organizations.
  * Integration with third-party systems requiring caller ID management.



## **Cause**

Caller ID display and routing issues in Zoom Phone may occur due to several factors:

  * Zoom Phone uses E.164 international formatting for caller ID display, which includes country codes by default and cannot be disabled.
  * Call forwarding to external numbers displays the forwarding source number rather than the original caller ID.
  * Caller ID configuration requires explicit setup in the web portal.
  * Outbound caller ID selection is restricted to numbers assigned to users' accounts, company main numbers, or call queues that they are members of.



## **Resolution**

Use the solutions below to resolve caller ID display and call routing configuration issues based on your specific scenario.

### **Configure auto-receptionist caller ID to prevent call failures**

As the account owner or admin, if you determine that a user’s calls are failing because their outbound caller ID is set to the auto receptionist, follow the steps below to ensure it's set up properly or change it to a different outbound caller ID.

  1. Sign in to the Zoom web portal.
  2. In the navigation menu, click **Phone System Management,** then click **Users & Rooms**.
  3. Click the **Users** tab.
  4. Click the name of the user who needs to make outbound calls using the auto-receptionist number.
  5. Click the **Profile** tab.
  6. Under [Outbound Caller ID](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058307), select the appropriate number (such as the auto-receptionist number).
  7. Click **Save**.
  8. Test outbound calls to verify the configured number.



**Note:** Ensure the user has at least one valid outbound caller ID number assigned and allowed by policy. If calls are still failing, review[ Zoom Phone error codes](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0069786) and[ anti-spam](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0062095) guidance, verify the user’s calling plan/policies, and check network/firewall configuration.

### **Manage outbound caller ID selection for call queue members**

If a user is unable to choose a call queue number as their outbound caller ID, the account owner or admin can add them to that call queue as a member. Once added, the user can make outbound calls and display the call queue’s number. Follow one of the following sections to add your user to a call queue.

#### **Add users as members of a call queue**

  1. Sign in to the[ Zoom web portal](https://support.zoom.com/www.zoom.us/signin).
  2. In the navigation menu, click **Phone System Management,** then [Call Queues](https://zoom.us/pbx/page/telephone/groups#/groups).
  3. Click the name of the call queue you want to edit.
  4. Click the **Profile** tab.
  5. To the right of **Members(s)** , click **View or Edit** , then do one of the following: 
     * In the **Search for members** box, enter the name of the user to ensure the user is a member of the call queue.
     * Click **Add.**
     * Click the **Users** tab to add the user if the user is not a member of the call queue.
     * Click **OK**.



#### **Add a call queue number to a phone user 's profile**

  1. Sign in to the[ Zoom web portal](https://support.zoom.com/www.zoom.us/signin).
  2. In the navigation menu, click **Phone System Management** , then **Users & Rooms**.
  3. Click the **Users** tab.
  4. Click the name of the phone user.
  5. Click the **Profile** tab.
  6. To the right of **Outbound Caller ID** , select the appropriate call queue phone number.
  7. Click **Save**.
  8. (Optional) Under **Customize Numbers** , click **Add** to add more phone numbers as outbound caller IDs for the user. 
     * Under the **Zoom Phone** tab, select the phone number of the call queue.
     * Click **Save**.



**Note:** Users can only select caller IDs from numbers assigned to their account, the company's main number, or call queues where they are members.
