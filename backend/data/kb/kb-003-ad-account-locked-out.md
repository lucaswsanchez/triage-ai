---
id: KB-003
title: Active Directory Account Locked Out
category: Accounts & Identity
level: L1
tags: [active-directory, lockout, password, unlock, powershell]
estimated_time: 10 min
last_reviewed: 2026-11-17
---

# Active Directory Account Locked Out

## Summary

How to unlock an Active Directory account and, more importantly, find the device that keeps locking it so the problem does not come back.

## Applies to

- On-premises Active Directory accounts (hybrid users)
- Windows sign-in, file shares, Wi-Fi (802.1X) and VPN that authenticate against AD
- Lockout policy: 10 failed attempts in 15 minutes locks the account for 30 minutes

## Symptoms

- "The referenced account is currently locked out and may not be logged on to."
- The user is locked out again shortly after being unlocked.
- Wi-Fi or VPN suddenly stops authenticating after a password change.

## Cause

- Too many wrong password attempts by the user.
- **A device or app still using the old password** after a password change: phone mail app, mapped drive with saved credentials, Windows Credential Manager entry, a second laptop, a scheduled task.
- Rarely, a password-spraying attack.

## Resolution

1. **Verify the user's identity** (call-back or manager confirmation).
2. Check the lockout status. In PowerShell with the RSAT ActiveDirectory module:

    ```powershell
    Get-ADUser -Identity jdoe -Properties LockedOut, BadLogonCount, LastBadPasswordAttempt, PasswordLastSet |
        Select-Object SamAccountName, LockedOut, BadLogonCount, LastBadPasswordAttempt, PasswordLastSet
    ```

3. Unlock the account:

    ```powershell
    Unlock-ADAccount -Identity jdoe
    ```

    Or in **Active Directory Users and Computers**: right-click the user > **Properties > Account** > tick **Unlock account**.

4. If the user does not know the password, reset it (KB-001, hybrid section) and tick **User must change password at next logon**.
5. **Find the source** if the account locks again:
    - Ask: *Did you change your password recently? Do you have work email on your phone? Another laptop?*
    - On a domain controller, look for **Event ID 4740** in the Security log; the *Caller Computer Name* shows the device sending bad passwords.
    - On the user's PC, open **Credential Manager > Windows Credentials** and remove old entries for file servers or Office.
    - Update the password on the phone's mail app or remove and re-add the account.
6. Ask the user to sign in and confirm access to email and a file share.

## Escalation criteria

Escalate to **L2 Identity** if:

- The account locks repeatedly and the source device cannot be identified within 30 minutes.
- Event 4740 shows an unknown or external computer name (possible attack: raise a security incident).
- Multiple accounts are locking out at the same time.

## Related articles

- [KB-001 Reset a Forgotten Microsoft 365 Password](kb-001-reset-m365-password.md)
- [KB-009 VPN Does Not Connect](kb-009-vpn-not-connecting.md)

## Last reviewed

2026-11-17 by Service Desk.
