---
id: KB-005
title: Outlook Is Not Syncing Email
category: Microsoft 365
level: L1
tags: [outlook, email, exchange-online, sync, ost, profile]
estimated_time: 20 min
last_reviewed: 2026-11-17
---

# Outlook Is Not Syncing Email

## Summary

Steps to fix the classic Outlook desktop app when new email does not arrive, sent items stay in the Outbox or the status bar shows "Disconnected".

## Applies to

- Classic Outlook for Microsoft 365 (desktop) on Windows 10/11
- Exchange Online mailboxes

## Symptoms

- No new email for hours, while Outlook on the web (<https://outlook.office.com>) shows new messages.
- Status bar says **Disconnected**, **Trying to connect** or **Working offline**.
- Messages stuck in the **Outbox**.
- "Your mailbox is almost full" or "Mailbox full" warnings.

## Cause

- Outlook set to **Work Offline**, or no network connection.
- Corrupted local cache file (`.ost`) or Outlook profile.
- Mailbox over its quota (50 GB).
- Large attachment stuck in the Outbox.
- Outdated Office build or a faulty add-in.

## Resolution

1. **Compare with the web.** Ask the user to open <https://outlook.office.com>. If email is missing there too, it is a server or mail-flow issue: go to *Escalation criteria*.
2. **Check offline mode.** In Outlook go to **Send / Receive** and make sure **Work Offline** is *not* highlighted.
3. **Check the network.** Open any website. If it fails, follow KB-010.
4. **Clear the Outbox.** Move large stuck messages to Drafts, reduce attachment size (share a OneDrive link instead) and resend.
5. **Restart Outlook in safe mode** to rule out add-ins: press ++win+r++, run `outlook.exe /safe`. If it syncs, disable add-ins in **File > Options > Add-ins > COM Add-ins**.
6. **Check mailbox size**: **File > Info > Mailbox Settings**. If near quota, enable the Online Archive or ask the user to empty Deleted Items.
7. **Update Office**: **File > Office Account > Update Options > Update Now**.
8. **Rebuild the cache**: close Outlook, open `%localappdata%\Microsoft\Outlook`, rename the `.ost` file to `.ost.old` and start Outlook. It will re-download the mailbox (may take a while on large mailboxes).
9. **Create a new profile** if the above fails: **Control Panel > Mail (Microsoft Outlook) > Show Profiles > Add**, set it as default and start Outlook.
10. Confirm with the user by sending a test email to them and receiving their reply.

## Escalation criteria

Escalate to **L2 Messaging** if:

- Email is missing in Outlook on the web too (mail flow problem).
- Several users report the same issue at the same time (check the Microsoft 365 Service Health dashboard first).
- A new profile does not fix it.
- The mailbox is at quota and the user needs more space or archiving enabled.

## Related articles

- [KB-010 Wi-Fi Connected but No Internet (DNS and Connectivity)](kb-010-wifi-dns-troubleshooting.md)
- [KB-007 OneDrive Is Not Syncing](kb-007-onedrive-not-syncing.md)

## Last reviewed

2026-11-17 by Service Desk.
