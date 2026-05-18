---
type: concept
product: zoom-phone
title: eSIM Activation Message
sources:
  - article_id: KB0084361
    title: Using Zoom Phone eSIM numbers
    source_url: https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0084361
confidence: high
last_reviewed: 2026-05-18
---

# eSIM Activation Message

## Summary

An email automatically sent to users when an admin issues an eSIM, containing a QR code, manual activation codes, and installation instructions. Designers should ensure this email is mobile-optimized since users will likely open it on the device they are activating, and that QR codes are prominently displayed with clear fallback instructions for manual entry.

## Key points

- Contains QR code, manual activation codes (SM-DP+ address, activation code), and step-by-step instructions
- Delivered both via email and accessible through the Zoom web portal under Phone > Settings > eSIM
- QR codes are single-use only and become invalid after successful installation
- On mobile: sign into email, find activation email, view QR code and instructions
- On web: navigate to Phone > Settings > eSIM > View QR Code to open a pop-up window
- Both channels display the same information: QR code, manual codes, and installation instructions

## Related

- [[esim-activation-message]]
- [[zoom-phone-esim]]
