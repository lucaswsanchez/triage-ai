---
id: KB-002
title: Set Up or Reset Multi-Factor Authentication (MFA)
category: Accounts & Identity
level: L1
tags: [mfa, authenticator, microsoft-365, new-phone, sign-in]
estimated_time: 15 min
last_reviewed: 2026-11-17
---

# Set Up or Reset Multi-Factor Authentication (MFA)

## Summary

How to register Microsoft Authenticator for MFA, move it to a new phone, and how the Service Desk resets MFA when the user has lost access to their verification method.

## Applies to

- All Microsoft 365 accounts at Acme Corp (MFA is mandatory)
- Microsoft Authenticator on iOS and Android

## Symptoms

- "More information required" prompt at sign-in.
- The user got a new phone and no longer receives approval notifications.
- "We didn't receive a response" or the user is stuck in an MFA loop.
- The user receives MFA prompts they did not request.

## Cause

- First sign-in: MFA has not been registered yet.
- The phone was replaced, reset or lost, so the Authenticator account is gone.
- The phone's clock is wrong, or notifications are disabled for Authenticator.
- **Unexpected prompts mean someone else may know the password.**

## Resolution

### First-time setup

1. Install **Microsoft Authenticator** from the App Store or Google Play.
2. On a computer, go to **<https://aka.ms/mfasetup>** and sign in.
3. Choose **Add sign-in method > Authenticator app** and scan the QR code with the app.
4. Approve the test notification and enter the number shown on screen.
5. Add a **second method** (phone number) as a backup.

### Moving to a new phone (old phone still available)

1. On the new phone, install Authenticator.
2. On a computer, open <https://mysignins.microsoft.com/security-info>.
3. **Add sign-in method > Authenticator app**, scan the QR code with the new phone.
4. Set the new phone as the **default sign-in method**, then delete the old device entry.

### Service Desk reset (user lost all methods)

1. **Verify identity** with a call-back to the HR directory number or manager confirmation on Teams.
2. In the **Entra admin center** open **Users > [user] > Authentication methods**.
3. Click **Require re-register multifactor authentication** and, if needed, delete the stale methods.
4. Optionally issue a **Temporary Access Pass** (1 hour, one-time use) so the user can register again.
5. Ask the user to follow *First-time setup* above while you stay on the call.

### Unexpected MFA prompts

1. Tell the user to **deny** the prompt and report it.
2. Reset the password immediately (KB-001) and revoke sessions: **Entra admin center > Users > [user] > Revoke sessions**.
3. Raise a **P2 security incident** and follow KB-018.

## Escalation criteria

Escalate to **L2 Identity / Security** if:

- The user received MFA prompts they did not initiate (possible password compromise).
- A Temporary Access Pass cannot be issued or the policy blocks registration.
- The user is a privileged administrator (admins are reset only by L2).

## Related articles

- [KB-001 Reset a Forgotten Microsoft 365 Password](kb-001-reset-m365-password.md)
- [KB-018 Report a Suspicious Email (Phishing)](kb-018-phishing-suspicious-email.md)

## Last reviewed

2026-11-17 by Service Desk.
