---
id: KB-008
title: Access a Shared Mailbox in Outlook
category: Microsoft 365
level: L1
tags: [outlook, shared-mailbox, exchange-online, permissions, send-as]
estimated_time: 15 min
last_reviewed: 2026-11-17
---

# Access a Shared Mailbox in Outlook

## Summary

How to open a shared mailbox (for example `sales@acme.example`) in Outlook desktop and on the web, and what to check when it does not appear or the user cannot send from it.

## Applies to

- Exchange Online shared mailboxes
- Classic Outlook for Microsoft 365 and Outlook on the web

## Symptoms

- The shared mailbox does not appear in the Outlook folder list.
- "You do not have permission to send the message on behalf of the specified user."
- The mailbox appears but folders are empty or will not expand.

## Cause

- The user has not been granted **Full Access** (to read) or **Send As** (to send) permission.
- Permissions were granted recently: auto-mapping can take up to 60 minutes.
- Outlook cache needs a restart, or the mailbox was added as a second account incorrectly.

## Resolution

### Request access

1. Open a **service request** "Shared mailbox access" with the mailbox address and whether you need to **read** and/or **send**.
2. The mailbox **owner must approve**.

### Grant access (technician, Exchange admin)

1. In the **Exchange admin center** go to **Recipients > Mailboxes**, select the shared mailbox, **Delegation**.
2. Add the user to **Read and manage (Full Access)** and, if approved, **Send as**.
3. Or with Exchange Online PowerShell:

    ```powershell
    Add-MailboxPermission -Identity sales@acme.example -User jdoe@acme.example -AccessRights FullAccess -AutoMapping $true
    Add-RecipientPermission -Identity sales@acme.example -Trustee jdoe@acme.example -AccessRights SendAs -Confirm:$false
    ```

### Open it

1. **Outlook desktop**: wait up to 60 minutes, then **restart Outlook**. The mailbox appears in the folder pane automatically.
2. If it does not appear: **File > Account Settings > Account Settings > [your account] > Change > More Settings > Advanced > Add** and type the mailbox name.
3. **Outlook on the web**: right-click **Folders** > **Add shared folder or mailbox** and type the address.
4. **To send from it**: in a new email click **From** (enable it in **Options > Show From**) and select the shared address.
5. Send a test email from the shared mailbox and confirm it lands in *Sent Items*.

## Escalation criteria

Escalate to **L2 Messaging** if:

- Permissions are correct but the mailbox does not load after 2 hours and a restart.
- Sent emails from the shared mailbox are not saved to its *Sent Items* folder (requires a mailbox setting change).
- A new shared mailbox needs to be created.

## Related articles

- [KB-005 Outlook Is Not Syncing Email](kb-005-outlook-not-syncing.md)
- [KB-004 Request or Grant Access to a Shared Folder](kb-004-shared-folder-permissions.md)

## Last reviewed

2026-11-17 by Service Desk.
