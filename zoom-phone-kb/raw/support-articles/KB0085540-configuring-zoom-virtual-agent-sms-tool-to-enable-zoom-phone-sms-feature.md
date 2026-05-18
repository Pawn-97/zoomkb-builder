---
source_type: zoom_support_article
product: zoom-phone
article_id: KB0085540
title: Configuring Zoom Virtual Agent SMS tool to enable Zoom Phone SMS feature
source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085540
captured_at: 2026-05-18T09:08:58.074551+00:00
retrieval_tool: jsonld
relevance_score: 30
confidence: high
content_hash: sha256:03971031753844258d2b5f32cf4ca0e77fe52b99fc27f5581474a0af4b9dbf85
status: raw
---

# Configuring Zoom Virtual Agent SMS tool to enable Zoom Phone SMS feature

Zoom Virtual Agent (ZVA) and Zoom Phone (ZP) customers can leverage ZP’s SMS capabilities directly within ZVA to enhance voice interactions. During a live call, agents can send customizable SMS messages containing dynamic text, URLs, or survey links. This enables customers to receive detailed information that may be difficult to convey over voice alone.

This article walks you through how to configure the SMS tool in Zoom Virtual Agent and set up the required Zoom Phone components to enable SMS messaging functionality.

### Requirements for configuring the Zoom Virtual Agent SMS tool to enable the Zoom Phone SMS feature

  * Account owner or admin privileges; or relevant [role/privilege](https://support.zoom.us/hc/en-us/articles/12200826942093)
  * Zoom Virtual Agent and Zoom Phone licenses



## Table of Contents

  * How to configure the SMS tool within the voice agent
  * How to configure the Zoom Phone Auto Receptionist to enable the SMS feature



## How to configure the SMS tool within the voice agent

Follow these steps to configure the SMS tool within your voice agent:

  1. [Create or edit an instruction-based voice agent](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0081096#mcetoc_1it2u8igtl).
  2. In the **Skills** section, enter a skill name and define a trigger description.
  3. In the **Instruction** section, click **Insert** , then search for and select the **SMS** tool. 

**Tip** : You can also use the forward slash (/) key to insert variables or tools.

  4. For **Sender phone number** , select **Entry point number**.
  5. For **Recipient** **phone** **number** , select the variable containing the recipient’s phone number.
  6. In the **Content** box, enter your SMS message content. Use the forward slash (/) key to insert variables for dynamic text.
  7. Click **Save and add**.
  8. Publish the voice agent to apply the changes.



## How to configure the Zoom Phone Auto Receptionist to enable the SMS feature

To enable SMS functionality in your Zoom Phone Auto Receptionist:

  1. Sign in to the Zoom web portal.
  2. In the navigation menu, go to **Phone System Management** then **AI Receptionist**.
  3. Click the **Virtual** **Agent** tab.
  4. Select the Zoom Phone Auto Receptionist associated with your voice agent.
  5. Next to **Number(s)** , click **Add** and assign a 10-digit phone number. 

**Note** : Ensure the assigned number has an **Approved Messaging Campaign**. Create one if it does not yet exist.

  6. Go to the **Policy** tab.
  7. Under the **General** section, enable the **SMS** toggle.
  8. Click **Allow List** and add at least one Zoom Phone user.   
These users will be able to view incoming SMS replies from customers.



Note: This article applies to Zoom Virtual Agent voice agent. If you are using other Zoom Virtual Agent types, such as [chat agent](https://support.zoom.com/hc/en/article?id=zm_kb&amp;amp;sysparm_article=KB0058248#mcetoc_1it40jn5eho)or [classic chatbot](https://support.zoom.com/hc/en/article?id=zm_kb&amp;amp;sysparm_article=KB0058248#h_01GPSJPRT0517R7QGVPRBV9RBC), refer to their respective documentation for setup and channel deployment instructions.
