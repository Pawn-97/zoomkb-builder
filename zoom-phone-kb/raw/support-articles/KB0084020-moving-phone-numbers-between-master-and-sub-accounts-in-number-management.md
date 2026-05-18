---
source_type: zoom_support_article
product: zoom-phone
article_id: KB0084020
title: Moving phone numbers between master and sub-accounts in Number Management
source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084020
captured_at: 2026-05-18T09:09:38.931723+00:00
retrieval_tool: jsonld
relevance_score: 11
confidence: high
content_hash: sha256:2a41fab95b5baa26303888eb9499b563d27d9284f8c34ba18a37a13e7bc535f6
status: raw
---

# Moving phone numbers between master and sub-accounts in Number Management

Account owners and admins can transfer phone numbers between related [master and sub-accounts](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0076468) in [Number Management](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0074457) without requiring support tickets or extended downtime. Admins can move numbers from sub-accounts to their master account before deleting the sub-accounts, preventing number loss or quarantine placement.

All number types are supported and can be moved into unallocated, Zoom Phone (ZP), or Zoom Contact Center (ZCC) products in the destination account through individual transfers, bulk operations, or CSV import functionality. This feature requires numbers to be in an unassigned state before moving. For native numbers, the destination account must have an appropriate business address. Business address validation provides eligibility for native numbers, while BYOC numbers can move freely between accounts.

Learn more about [managing Number Management master and sub accounts](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0076468) and [migrating phone numbers across Zoom Phone and BYOC services in Number Management](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0083730).

**Notes** :

  * All number types are supported to be moved.
  * [Contact Zoom Support](https://support.zoom.com/hc/en/contact?id=contact_us) to enable this feature.



### Requirements for moving phone numbers between master and sub-accounts in Number Management

  * Must have a master account  
**Note** : Master account and sub-accounts must have the Zoom Global Phone Number SKU.
  * The receiving account has a verified and relevant business address created in a verified state for the number being transferred.
  * Account owner or admin with the privilege to[ manage sub accounts](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0066764)
  * A license for the product you want to manage in Number Management: 
    * Zoom Contact Center license
    * Zoom Phone license: Zoom Phone Pro, a Zoom Phone calling plan, or Zoom Workplace bundles containing Zoom Phone



### Limitations for moving phone numbers between master and sub-accounts in Number Management

Moving phone numbers between master and sub-accounts in Number Management has the following limitations:

  * This option should only be visible when its master or sub account classification.
  * The move is only allowed if the appropriate business address exists in the destination account for native numbers. This requirement is not needed for BYOC numbers.
  * If the number had messaging service, SPAM monitoring, CNAM, branded calling, or associated features enabled on this number before the move, then those features must be configured again once the number is received in the sub-account. For example, this could mean creating a sub-account-specific 10DLC brand and campaign.
  * If the user chooses to eliminate the sub-account and still wants to retain the number, then it is the customer admin’s responsibility to move the numbers back to the master account before deleting the sub-account, or else the numbers will be deleted from the account completely and released from the Zoom system.



## Table of Contents

  * How to move phone numbers between master and sub-accounts in Number Management
    * Move a selected number
    * Move multiple selected numbers
    * Move numbers through CSV upload



## How to move phone numbers between master and sub-accounts in Number Management

### Move a selected number

#### Move native phone numbers

  1. Sign in to the [Zoom web portal](https://zoom.us/profile?_ga=2.111323140.1807109990.1712696386-119871112.1669604209) as an admin with the privilege to edit account settings.
  2. In the navigation menu, click **Number Management** then **Phone Numbers**.
  3. To the right of the phone number you want to move, click the ellipsis , then click **Move to account**.  
A pop-up window will appear.
  4. In the window, click the dropdown and select information for the following fields: 
     * **Choose an account to transfer to**
     * **Product**
     * **Subscription**
     * **Division**
     * **SIP group**
  5. Click **Next**.
  6. Under **Business address & documents**, click the dropdown and select the business address.
  7. Click **Move**.  
The numbers will be moved to the specified account.



#### Move BYOC phone numbers

  1. Sign in to the [Zoom web portal](https://zoom.us/profile?_ga=2.111323140.1807109990.1712696386-119871112.1669604209) as an admin with the privilege to edit account settings.
  2. In the navigation menu, click **Number Management** then **Phone Numbers**.
  3. To the right of the phone number you want to move, click the ellipsis , then click **Move to account**.  
A pop-up window will appear.
  4. In the window, click the dropdown and select information for the following fields: 
     * **Choose an account to transfer to**
     * **Product**
     * **Subscription**
     * **Division**
     * **SIP group**
  5. Click **Move**.  
The numbers will be moved to the specified account.



### Move multiple selected numbers

  1. Sign in to the [Zoom web portal](https://zoom.us/profile?_ga=2.111323140.1807109990.1712696386-119871112.1669604209) as an admin with the privilege to edit account settings.
  2. In the navigation menu, click **Number Management** then **Phone Numbers**.
  3. To the left of the phone numbers you want to move, select the checkboxes.  
**Note** : In the top-left corner of the page, to the left of **Number** , select the checkbox to select all numbers.
  4. At the top of the page, click **Move numbers between master/sub account**.  
**Note** : If native numbers were selected, a pop-up window will appear where you must select and/or verify the business address and documents. After verifying the business address, click **Move**.  
The numbers will be moved to the specified account.



### Move numbers through CSV upload

  1. Sign in to the [Zoom web portal](https://zoom.us/profile?_ga=2.111323140.1807109990.1712696386-119871112.1669604209) as an admin with the privilege to edit account settings.
  2. In the navigation menu, click **Number Management** then **Phone Numbers**.
  3. At the top of the page, click **Related features** then **Move number between master/sub via CSV**.  
A pop-up window will appear.
  4. In the window, download the **CSV Sample** file and edit it with the required information:  
**Note** : Maximum records must be less than 10000.  

     * **Phone Number (required)** : Include only 1 number per row.  
**Note** : Only the E.164 format is supported. For example, the E.164 format of a US number is +16992520210.
     * **Allocate to (required)** : Specify a product.
     * **Target account (Required)** : Specify the target account’s name in which you want to move the numbers.
     * **Division name**(Required for ZCC): If allocating to Zoom Contact Center, specify a division name where you want to move your number. Only the unassigned numbers' division name can be updated. This field only applies to numbers that have been allocated to Zoom Contact Center.
     * **Site name (Required for Zoom Phone)** : Specify a site name where you want to move your number. Only the unassigned numbers' site name can be updated. This field only applies to numbers that have been allocated to Zoom Phone.
     * **Subscription (required)** : Each product belongs to a subscription, which is a bundle of licenses and plans under your account. This helps Zoom assign phone numbers and features to the right billing package.
     * **SIP group** : Specify a SIP group where you want to move your number.
  5. After editing the CSV Sample file, select the following checkbox: **I acknowledge that by checking this box, I attest that the phone numbers to be imported belong to me or my organization**.
  6. Click **Upload CSV**.  
The numbers will be moved to the specified account.
