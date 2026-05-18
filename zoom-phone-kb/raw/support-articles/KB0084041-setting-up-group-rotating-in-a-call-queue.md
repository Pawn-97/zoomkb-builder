---
source_type: zoom_support_article
product: zoom-phone
article_id: KB0084041
title: Setting up group rotating in a call queue
source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084041
captured_at: 2026-05-18T09:09:06.676136+00:00
retrieval_tool: jsonld
relevance_score: 20
confidence: high
content_hash: sha256:028bd9e09073ec0d9e16284d4992173c9a0d2fac28e4ce8fe1619c1d42a68826
status: raw
---

# Setting up group rotating in a call queue

Group rotating is a call distribution method that rings subsets of call queue members instead of ringing all members at the same time.

When a call comes in:

  * A defined number of members (the **Group member size**) are rung first.
  * If no one answers, the call rings the next group of members.
  * This continues until all members have been attempted.
  * If no one answers, the call follows the **Overflow** settings.



For example, if a call queue has 25 members and the group member size is set to 5:

  * The first 5 members ring.
  * If unanswered, the next 5 members ring.
  * This repeats until all members are tried.
  * If the call is still unanswered, it goes to overflow.



Learn more about [changing business hours, holiday hours, and overflow settings](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0069616) and [managing Zoom Phone call queues](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0064844).

### Requirements for managing Zoom Phone call queues

  * Either a Zoom Workplace license with Phone included, or a standalone Zoom Phone calling plan
  * Account owner or admin privileges
  * [Initial Zoom Phone setup](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060257#h_5ae26a3a-290c-4a8d-b3b0-6384ed267b13) to create and manage call queues



## Table of Contents

  * How to configure group rotating for a call queue
  * How to configure named rotation groups using multiple call queues
    * (1) Create the first call queue (primary group)
    * (2) Create the second call queue (secondary group)
    * Call flow behavior



## How to configure group rotating for a call queue

  1. Sign in to the Zoom web portal as an account owner or admin.
  2. In the navigation menu, click **Phone System Management** then **Call Queues**.
  3. Click the name of the call queue.
  4. Click the **Profile** tab.
  5. In the **Business Hours** section, click the **Call Distribution** dropdown and select **Group Rotating**.
  6. Set the **Group member size** to the number of members you want to ring at one time.
  7. Set the **Ringing duration for each group**.
  8. Click **Confirm**.
  9. [Configure **Overflow** behavior](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0069616) (for example, voicemail or call forwarding).
  10. Click **Save**.



## How to configure named rotation groups using multiple call queues

If you want specific members to be rung first, followed by a second set of members if no one answers, use multiple call queues with overflow routing.

### (1) Create the first call queue (primary group)

  1. [Create or edit a call queue](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0064844#h_e81faeeb-9184-429a-aaea-df49ff5ff413).
  2. Add the primary group members.
  3. Set **Call Distribution** to **Simultaneous**.
  4. [Configure **Business Hours Overflow**](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0069616) to transfer to a second call queue.
  5. Click **Save**.



### (2) Create the second call queue (secondary group)

  1. [Create a second call queue](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0064844#h_e81faeeb-9184-429a-aaea-df49ff5ff413).
  2. Add the secondary group members.
  3. [Configure **Business Hours Overflow**](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0069616) to transfer to: 
     * The voicemail of the first call queue, or
     * Another destination of your choice.
  4. Click **Save**.



### Call flow behavior

  * Calls ring all members in the first call queue simultaneously.
  * If no one answers, the call is routed to the second call queue.
  * If still unanswered, the call follows the overflow settings of the second queue.
