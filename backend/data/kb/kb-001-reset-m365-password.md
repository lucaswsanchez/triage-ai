---
id: KB-001
title: Reset a Forgotten Microsoft 365 Password
category: Accounts & Identity
level: L1
tags: [password, microsoft-365, sspr, entra-id, sign-in]
estimated_time: 10 min
last_reviewed: 2026-11-17
---

# Reset a Forgotten Microsoft 365 Password

## Summary

How a user can reset their own Microsoft 365 (Entra ID) password with Self-Service Password Reset (SSPR), and how the Service Desk resets it when self-service is not possible.

## Applies to

- All Acme Corp employees and contractors with a Microsoft 365 account
- Windows 10/11 laptops joined to Entra ID or hybrid-joined to Active Directory
- Web sign-in (outlook.office.com, portal.office.com) and the Windows sign-in screen

## Symptoms

- "Your account or password is incorrect. If you don't remember your password, reset it now."
- The user forgot their password after a vacation or a forced password change.
- The password expired and the user cannot sign in to Outlook, Teams or the laptop.

## Cause

- The user forgot the password or it expired under the password policy.
- The password was changed on another device and cached credentials are out of date.

## Resolution

### Option A: Self-service (preferred, the user does it)

1. On any device, open **<https://aka.ms/sspr>** (or click **Forgot my password** on the Microsoft sign-in page).
2. Enter the work email address (`firstname.lastname@acme.example`) and complete the captcha.
3. Verify identity with the registered method (Authenticator notification, SMS or phone call).
4. Choose a new password that meets the policy: at least 14 characters, not used before, no name or company name. A short passphrase works well, for example three unrelated words plus a number.
5. Sign in again at <https://portal.office.com> to confirm.
6. On the laptop, **lock the screen** (++win+l++) and unlock it with the new password while connected to the office network or VPN so Windows updates its cached credentials.

### Option B: Service Desk reset (the user cannot use SSPR)

1. **Verify the caller's identity** before doing anything: call back on the number in the HR directory or confirm with the user's manager on Teams. Never reset based on email alone.
2. In the **Microsoft 365 admin center** go to **Users > Active users**, select the user, then **Reset password**.
3. Select **Automatically create a password** and **Require this user to change their password when they first sign in**.
4. Deliver the temporary password through the verified channel (phone call), never in the ticket notes or by email.
5. Ask the user to sign in, set a new password and confirm they can open Outlook and Teams.
6. Document in the ticket *how* identity was verified (not the password).

!!! warning "Hybrid accounts"
    If the account is synced from on-premises Active Directory, reset the password in **Active Directory Users and Computers** (or with `Set-ADAccountPassword`) instead, then wait for the next sync or ask L2 to run a delta sync.

## Escalation criteria

Escalate to **L2 Identity** if:

- The reset fails with "password writeback" or sync errors.
- The account is disabled, deleted or shows risky sign-ins in Entra ID.
- The user's identity cannot be verified.
- The account is locked again within minutes of the reset (possible attack or a device with old credentials, see KB-003).

Include: user principal name, time of the attempt, exact error text and how identity was verified.

## Related articles

- [KB-002 Set Up or Reset Multi-Factor Authentication (MFA)](kb-002-mfa-setup-and-reset.md)
- [KB-003 Active Directory Account Locked Out](kb-003-ad-account-locked-out.md)
- [KB-018 Report a Suspicious Email (Phishing)](kb-018-phishing-suspicious-email.md)

## Last reviewed

2026-11-17 by Service Desk.
