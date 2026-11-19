---
id: KB-019
title: Lost or Stolen Laptop or Phone
category: Security
level: L1
tags: [lost-device, stolen, security, intune, remote-wipe, incident]
estimated_time: 20 min
last_reviewed: 2026-11-17
---

# Lost or Stolen Laptop or Phone

## Summary

The immediate steps when a company laptop or a phone with company data is lost or stolen: protect the account, secure the device remotely and document the incident.

## Applies to

- Company laptops and phones enrolled in Intune
- Personal phones with Outlook/Teams (app protection policies)

## Symptoms

- The user reports a device left in a taxi, stolen from a car, lost while travelling, etc.

## Cause

Loss or theft. Company data on the device may be at risk if it was unlocked or the password was written down.

## Resolution

**Treat as a P2 security incident. Speed matters.**

1. **Collect facts**: device type and name/serial, when and where it was lost, was it locked/powered off, any passwords written on or near it.
2. **Protect the account**:
    - Reset the user's password (KB-001) and **revoke all sessions** in Entra ID.
    - Review recent sign-ins for unknown locations.
3. **Secure the device in Intune** (Intune admin center > **Devices > [device]**):
    - Company laptop: **Remote lock**, then **Wipe** after manager/security approval if it is not recovered within the agreed time. BitLocker protects data at rest.
    - Company phone: **Remote lock** and **Wipe**.
    - Personal phone (BYOD): **Retire** / selective wipe removes only company apps and data.
4. **Disable the device** in Entra ID so it cannot be used to sign in.
5. **Advise the user** to report theft to the police and get a report number (needed for insurance).
6. **Arrange a replacement** device through the onboarding process (KB-020) once the incident is logged.
7. Notify **Security** and the user's manager; record every action with timestamps in the ticket.

## Escalation criteria

Escalate to **Security** immediately if:

- The device was unlocked when lost, or passwords were stored with it.
- The user handles sensitive data (HR, Finance, Legal, executives).
- Suspicious sign-ins appear after the loss.

## Related articles

- [KB-014 BitLocker Recovery Key Requested at Startup](kb-014-bitlocker-recovery.md)
- [KB-001 Reset a Forgotten Microsoft 365 Password](kb-001-reset-m365-password.md)
- [KB-018 Report a Suspicious Email (Phishing)](kb-018-phishing-suspicious-email.md)

## Last reviewed

2026-11-17 by Service Desk.
