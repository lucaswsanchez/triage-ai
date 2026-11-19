---
id: KB-018
title: Report a Suspicious Email (Phishing)
category: Security
level: L1
tags: [phishing, security, email, report, incident, outlook]
estimated_time: 10 min
last_reviewed: 2026-11-17
---

# Report a Suspicious Email (Phishing)

## Summary

What a user should do with a suspicious email, and what the Service Desk must do if the user already clicked a link, opened an attachment or entered their password.

## Applies to

- All Acme Corp users with a Microsoft 365 mailbox
- Outlook desktop, Outlook on the web and Outlook mobile

## Symptoms

The email shows one or more red flags:

- Urgency or threats: "Your account will be closed in 24 hours", "Invoice overdue".
- Sender address does not match the display name or uses a look-alike domain (`acme-corp-support.com`, `rnicrosoft.com`).
- Unexpected attachment (`.html`, `.zip`, `.iso`, macro-enabled Office files) or a QR code.
- Links whose real address (hover to see it) is not the expected site.
- Requests for passwords, MFA codes, gift cards or bank detail changes.
- An **[EXTERNAL]** tag on a message that claims to be from a colleague.

## Cause

Attackers impersonate trusted brands or colleagues to steal credentials, deliver malware or trick people into payments.

## Resolution

### If the user did NOT click anything

1. **Do not** click links, open attachments, reply or forward the email to colleagues.
2. Use the **Report** button in Outlook (**Home > Report > Report phishing**). This sends it to the security team and removes it from the inbox.
3. If the Report button is not available, forward it **as an attachment** to `phishing@acme.example`, then delete it.
4. Thank the user: reporting is always the right call, even for false alarms.

### If the user clicked a link, opened an attachment or entered credentials

Treat as a **P2 security incident** (P1 if a privileged account or many users are involved). Act immediately:

1. **Disconnect the device from the network** (turn off Wi-Fi / unplug cable) if an attachment was opened or software was downloaded. Do not shut it down.
2. **Reset the user's password** (KB-001) from a different, clean device and **revoke all sessions** in Entra ID.
3. Check **MFA methods** for anything the user did not add, and review recent sign-ins for unknown locations.
4. Check Outlook **inbox rules** and forwarding for rules the user did not create (attackers hide replies this way).
5. Collect for the security team: the original email (as attachment), time of click, what was entered or opened, device name.
6. Escalate to **Security** following the escalation flow; do not try to clean malware at L1.

## Escalation criteria

Escalate to **Security (L2/L3)** immediately if:

- Credentials were entered, an attachment was opened or software was run.
- The email came from a real internal account (account compromise).
- Several users received the same email and some clicked.
- The email requests payment or bank detail changes (also notify Finance).

## Related articles

- [KB-001 Reset a Forgotten Microsoft 365 Password](kb-001-reset-m365-password.md)
- [KB-002 Set Up or Reset Multi-Factor Authentication (MFA)](kb-002-mfa-setup-and-reset.md)

## Last reviewed

2026-11-17 by Service Desk.
