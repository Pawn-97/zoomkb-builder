---
source_type: zoom_support_article
product: zoom-phone
article_id: KB0084727
title: Japan SMS registration guide for Zoom Phone and Contact Center
source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084727
captured_at: 2026-05-18T09:08:58.995569+00:00
retrieval_tool: jsonld
relevance_score: 17
confidence: high
content_hash: sha256:b4e607d43496f3488451dc01e46a417afc0b2f6c795d3f49b5d0684a2b1d960e
status: raw
---

# Japan SMS registration guide for Zoom Phone and Contact Center

Japan SMS registration is required by Japan mobile carriers to enable business-to-consumer (A2P) messaging on Japan-based phone numbers. This feature enables account owners and admins to sign up their organization for Japan A2P messaging to use SMS with Zoom Phone and Zoom Contact Center.

The entire process, which includes external approval from mobile carriers, takes a minimum of 2 weeks. Business registration doesn't need approval. However, if any inconsistencies are flagged during approval of SMS registration, then the customer may have to go back and update the business registration accordingly. Numbers are assigned to the SMS registration before it is sent out for approval.

**Note** : Zoom suggests that you start this process as early as possible to help ensure that the external approvals align with your implementation timelines.

### Requirements for Japan SMS registration

  * Zoom Phone account owner, or account owner or admin with****[SMS setup privileges](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0064983)
  * A compliant privacy policy that states you do not share/sell your customers' mobile information with third parties



### Limitations for Japan A2P SMS capabilities granted through Japan SMS registrations

  * Business registration and SMS registration processes are mandatory for enabling A2P SMS on Japanese phone numbers.
  * SMS capabilities are only available for outbound direction. For example, from numbers assigned to the SMS registration towards end customers/consumers.
  * For SoftBank network recipients, the actual phone number will not appear as the sender ID. Instead, SoftBank displays a unique sender ID for all SMS messages, regardless of your registered business or assigned number. 
    * This restriction is imposed by SoftBank and applies to all A2P SMS messages from any SMS aggregator.
    * SoftBank assigns a unique sender ID to each SMS aggregator.



## Table of Contents

  * How to access SMS registration in the Zoom web portal
  * How to create a business registration to register the business information
    * Managing the life cycle of business registration
  * How to create an SMS registration
    * 1\. Create an SMS registration
    * 2\. Configure SMS registration
    * 3\. Configure the sample message
  * How to manage the SMS registration lifecycle
  * How to manage the number assignment to the SMS registration



## How to access SMS registration in the Zoom web portal

  1. Sign in to the[ Zoom web portal](https://www.zoom.us/signin) as an admin with the privilege to edit account settings.
  2. In the navigation menu, click **Number Management** , then click **SMS Setup**.
  3. Click **Add country/region** and then select **Japan**.



## How to create a business registration to register the business information

You can create a business registration to register your business information with the Japan-based mobile carriers. This is required to use SMS with Zoom.

Business registration is mandatory before creating an SMS registration.

**Notes** :

  * Business registration does not have a separate approval process. Instead, the business information will be validated by Japan-based carriers when the SMS registration approval request is submitted to them.
  * Information under business registration can be updated at any time, unless the SMS registration associated with this business is in pending or active status.


  1. If you are adding a business registration for the first time, click **Add country/region** and select **Japan** as the country.  
If you already have an existing business registration for Japan, access **Japan** on the SMS setup page and click **Add** to create a new business registration.
  2. On the **New business registration page** , enter the following: 
     * **Prefecture**
     * **Legal company** **name** : This legal company should be the owner of the corporate number, which will be entered in the next steps.
     * **Department Name** : Enter the brand or department name that will use this SMS service within your organization.
     * **Corporate Number** : Enter a valid corporate number that will be verified against your legal company name by mobile carriers. This verification is essential for completing the SMS registration process.
     * **Website** : Add the official working website representing the legal company name.
     * Your company’s **Legal Form**



### **Managing the life cycle of business registration**

  1. Japan-based business registrations are accessible within Japan via SMS setup.
  2. Business information can be updated or deleted anytime unless it has any active or pending SMS registrations.
  3. You may be asked to update business registration information depending on the rejected reason.



## How to create an SMS registration

### 1\. Create an SMS registration

Once the business registration is created, you can create an SMS registration. The SMS registration will be used to assign your company phone numbers and enable SMS.

  1. [Access ](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0059336#h_17720208614621734474046221)**[Japan SMS registration](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0059336#h_17720208614621734474046221)** in the Zoom web portal.  
You will be directed to the **Checklist Requirement** page, where you will be presented with a link to review the Japan SMS registration creation checklist.
  2. Click the[ Japan SMS registration creation checklist link](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0010208).  
**Note** : You are required to open and view the link before continuing.
  3. After opening and reviewing the link, select the **I confirm that I have read and understood the Japan SMS registration creation checklist** checkbox.  
Once this is done, the registration details section will display. On this page, you will complete the requirements and details.



### 2\. Configure SMS registration

  1. Configure your SMS registration as follows: 
     1. **SMS registration details:**
        * **Registered business** : Select the registered business from the drop-down.
        * **Registration name** : Enter a name for your registration.
        * **Usage purpose:** enter the purpose for which SMS is sent out. For example, appointment reminders, sending out the survey link, and booking confirmation.
        * **Description** : Describe how your organization uses SMS. Provide details that cover who will message, who will receive messages, what kind of content is being sent, what kind of content will not be sent, and the frequency of sending these messages.  
**Note** : Provide as much detail as possible. Insufficient or unclear details will result in rejection.
        * Choose **SMS Volume Tier** for your registration. The default volume tier is **High Volume**. This is to help you get the maximum possible throughput allowed for your business. You will also have an option to choose to register your registration with the **Low Volume** tier.
        * **Usage time** : Call out the duration for sending out SMS. For example, SMS against this SMS registration will be sent between 9 am and 5 pm, or 11 am and 10 pm.
     2. **Sender ID_Number assignment to the SMS registration:** Assign Japan-based phone numbers as Sender IDs. You can use either Zoom's native numbers (0ABJ, 050, 0120, or 0800) or your own numbers that you have added to the Zoom platform via BYOC (Bring Your Own Carrier). 
        * Zoom native numbers: No additional proof is required when assigning these numbers to SMS registration. Zoom will automatically create the Letter of Authorization (LOA) and share it with the mobile carriers.
        * BYOC numbers: To establish ownership of your selected numbers, you must upload proof that links them to your registered business. Acceptable documents include invoices, order forms, or contracts between your business and the carrier. 
          * Screenshot of the website showing these numbers will be an added advantage to make the case strong.
        * SMS Registration Number Capacity: You can assign up to 50 phone numbers to a single SMS registration. Note that approval time increases proportionally with the number of phone numbers included in the registration.
        * SMS registration number rejection: Mobile carriers may reject certain numbers assigned to your SMS registration. In such cases, the registration will only be approved for the numbers that pass carrier validation.
     3. **SMS consent Management:** In the **Consent to SMS Messaging** section, under **How are you gathering consent to send SMS/MMS?** , provide details of how you are gathering consent from SMS recipients by selecting the following options that apply to your registration.  
**Note** : You must select at least one of these options. When you select one of the options, you will see examples of that option. 
        * Complete the description for each option and explain how you gather consent in your own words.  
**Note** : You can only send texts to consumers who have provided you consent. Provide as much detail as possible. If you collect any phone numbers from your website, you must select the website option and provide details of how you gather consent. Otherwise, your registration will be rejected. 
          * **Verbal** : For example, while on the phone with the user, you ask the customer to confirm if they wish to receive additional information via SMS. If the user agrees, the information is sent.  
**Note** : This description is required and cannot be edited. The **Verbal** option is selected as a default consent method, and the description is pre-populated. If you are not using this as a consent method, uncheck this box.
          * **Website** : For example, on your website, users opt-in to receive messages, and they select a checkbox to receive further communications via SMS. If the box is not checked, they will not receive messages. 
            * Enter the brand website in the **URL** field.
          * **Email** : For example, you send out a marketing email with a button that asks users to opt in to receive text messages.
          * **Written Form** : For example, when a patient comes to your office, you provide a paper form with a checkbox that opts them in to receive messages.
          * **Other** : For example, you provide a button to your social media groups on Facebook and Instagram that asks users to opt into receiving messages.
  2. Click **Continue** to the sample message section.



### 3\. Configure the sample message

Configure the sample message:

  1. In the **Sample Messages** section, enter the following:  
**Note** : You can provide up to five sample messages of the type you expect your company to send. 
     1. In **Sample Message 1** , type your first sample message. Ensure that the name of your business/brand is mentioned. Otherwise, your registration will be rejected.
     2. In **Sample Message 2** , type your second sample message. Ensure that the name of your business/brand is mentioned. Otherwise, your registration will be rejected.
     3. Optional) Click **+ Add another Sample Message** to add additional sample messages.
  2. Click **Submit**.



## How to manage the SMS registration lifecycle

**Note** : You cannot edit registration in active or pending status. They must be rejected in order to edit them.

  1. Access **SMS registration** in the Zoom web portal.
  2. Under **SMS registra** tion, click the name of the registration you want to manage.  
You will be directed to the registration details page. The **Edit** option is available for all editable fields in the registration.
  3. To the right of the field you want to edit, click **Edit** and make the changes.
  4. Click **Save**.
  5. Click **Resubmit** to resubmit the registration with all your changes.  
You can also assign additional phone numbers as a sender ID for active SMS registration.



## How to manage the number assignment to the SMS registration

  * Number assignments are mandatory during SMS registration creation.
  * Assigned numbers may get approved or rejected depending on the ownership proof shared for those numbers. 
    * Approval status of individual numbers will be reflected in the Sender ID section.
    * Status will be reflected as rejected for the numbers that are rejected by mobile carriers.
  * Additional numbers can be assigned to the active SMS registrations through the SMS registration section.
