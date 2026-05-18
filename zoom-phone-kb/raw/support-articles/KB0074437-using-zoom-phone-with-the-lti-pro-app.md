---
source_type: zoom_support_article
product: zoom-phone
article_id: KB0074437
title: Using Zoom Phone with the LTI Pro app
source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0074437
captured_at: 2026-05-18T09:09:31.870357+00:00
retrieval_tool: jsonld
relevance_score: 17
confidence: high
content_hash: sha256:6a901347a26cef045d0f90f502a590e780acf75ca89ae3830aed941a74297c6c
status: raw
---

# Using Zoom Phone with the LTI Pro app

With the Zoom Phone integration for LTI Pro, LTI Instructors and admins can utilize Zoom Phone directly within their course. This includes the ability to:

  * A simple click to automatically dial a phone number within LTI Pro
  * Manually dial a phone number
  * Access recordings within the call logs
  * Enjoy the high call quality and security that are provided by Zoom
  * Users can leverage additional features with the Zoom client



### Requirements for using Zoom Phone in LTI Pro

  * Pro, Business, or Enterprise account
  * [Zoom Phone license](https://zoom.us/pricing/zoom-phone)
  * [Zoom Phone configured](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060257)
  * [Automatic Calling from Third-Party Application](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0070147) enabled by admin



### Limitations of using Zoom Phone in LTI Pro

  * This feature is available for LTI 1.3 integrated with an LMS that supports the [NameRoleProvisionService](https://zoomvideo.atlassian.net/wiki/spaces/ZW/pages/2993823465/Zoom+Phone+LTI#Enabling-Names-and-Role-Provisioning-service) scope.
  * Only teachers or admins of the LMS Course have permission to use Zoom Phone in LTI Pro.
  * The phone numbers in the course contacts list are stored for 180 days.



## Table of Contents

  * How to enable Names and Role Provisioning service
  * How to set up Zoom Phone with LTI Pro
    * Configure LTI Pro for Zoom Phone
    * Authorize Zoom Phone in the LTI Pro app
    * Opening Zoom Phone in the LTI Pro app
  * How to use Zoom Phone in LTI Pro
    * Use LTI Contacts
    * Bulk import phone numbers into Contacts
  * Data Security



## How to enable Names and Role Provisioning service

Before setting up Zoom Phone with your LMS, the scope for Names and Role Provisioning Services (NRPS) will need to be enabled first. For more information on enabling this for your specific LMS, see below:

  * [Enabling the NRPS for Canvas](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0067133)
  * [Enabling the NRPS for Moodle](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058720)
  * [Enabling the NRPS for Blackboard](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058722)
  * [Enabling the NRPS for Brightspace](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058719)



## How to set up Zoom Phone with LTI Pro

### Configure LTI Pro for Zoom Phone

  1. Sign in to the[ Zoom Marketplace](http://marketplace.zoom.us/).
  2. Click **Manage** , then click **Apps on Account**.
  3. Find the**LTI Pro App**.
  4. Open the **LTI Pro App** , then click **Configure**.
  5. Select the configured LTI 1.3 credential, and click **Edit**. If the LTI 1.3 credential hasn’t been configured, then it will need to be configured before proceeding. Learn more about [configuring LTI Pro credentials](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0059624).
  6. Enable **Zoom Phone**.



### Authorize Zoom Phone in the LTI Pro app

  1. Launch the LTI Pro 1.3 app.
  2. In the LTI Pro app, click the **Phone** button.
  3. In the dialog window, click **Connect.**  
The user will be redirected to the login page.
  4. Log in using the Zoom user account.  
**Note** : The email of the Zoom user must be the same as the email used to log into the LMS.
  5. Click Allow, and the user should see a success message.  
**Note** : The user will need to be signed into the Zoom client as the Zoom Phone widget for LTI Pro uses the Zoom client to route calls



### Opening Zoom Phone in the LTI Pro app

  1. Log in to the Zoom client using the same Zoom user.
  2. Click the **Phone** button.  
Zoom Phone will open.



## How to use Zoom Phone in LTI Pro

You can generally find usage details for the Zoom Phone floating window in LTI Pro by referring to the [Zoom Phone Smart Embed](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0061862) feature. In addition, please refer to the following for more detailed information on using Zoom Phone:

  * [How to receive calls](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0061862#h_01GQFY9DSKQA95V586R3D120BS)
  * [How to make a call](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0061862#h_01GQFY9SA9W0HEV24WG508JNF2)
  * [How to send and receive SMS messages](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0061862#h_01GQFYA513CP9EVT6VDQYYMWQ0)
  * [How to view call history](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0061862#h_01GQFYBCKQXFE91D8VZS3JXJCK)



### Use LTI Contacts

  1. In the LTI Pro app, click the **Contacts** tab.  
The course class roster will be listed without phone numbers.
  2. Click **Edit**.
  3. Enter the desired number, and click **Add**.
  4. To start a phone call or send an SMS message with a contact, click the **Phone** icon or **SMS** icon.



### Bulk import phone numbers into Contacts

  1. In the Contacts tab, click **Import Phone Numbers**.
  2. The import dialog box will open. 
  3. Click **Download CSV Template**.
  4. Edit the downloaded CSV file.
  5. In the import window, click **Import Phone Numbers** and select the previously edited file.
  6. Click **Upload**.



## Data Security

  * The Zoom Phone integration in LTI Pro can view: 
    * Course roster information: **members of a course**.
    * User information: **first name** , **last name** , **email** , and **user id**.
  * Zoom Phone in LTI Pro can make calls using [Zoom Phone API](https://marketplace.zoom.us/docs/api-reference/phone/methods/#overview), as well as access call logs, voice mails, and SMS.
