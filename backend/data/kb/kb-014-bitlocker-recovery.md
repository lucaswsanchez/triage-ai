---
id: KB-014
title: BitLocker Recovery Key Requested at Startup
category: Hardware & Printing
level: L1
tags: [bitlocker, recovery-key, encryption, startup, intune, entra-id]
estimated_time: 15 min
last_reviewed: 2026-11-17
---

# BitLocker Recovery Key Requested at Startup

## Summary

What to do when a laptop shows the blue **BitLocker recovery** screen at startup, how the user can find their own key, and how the Service Desk provides it securely.

## Applies to

- Acme Corp Windows 10/11 laptops encrypted with BitLocker (keys escrowed to Entra ID / Intune)

## Symptoms

- Blue screen at startup: "BitLocker recovery – Enter the recovery key for this drive", showing a **Recovery key ID**.
- Happens after a BIOS/firmware update, docking station change, hardware repair or several wrong PIN attempts.

## Cause

BitLocker detected a change in the boot environment (firmware update, TPM reset, boot order change, motherboard repair) and needs the 48-digit recovery key to confirm the owner is authorized.

## Resolution

### Self-service (user has another device)

1. On a phone or other computer, go to **<https://myaccount.microsoft.com>** > **Devices**.
2. Select the laptop > **View BitLocker Keys**.
3. Match the **Key ID** shown on the blue screen (first 8 characters) and type the 48-digit recovery key.

### Service Desk provides the key

1. **Verify the caller's identity** (call-back to the HR directory number or manager confirmation). The recovery key unlocks all data on the device.
2. Ask the user to read the **first 8 characters of the Recovery key ID** from the screen.
3. In the **Intune admin center**: **Devices > [device] > Recovery keys** (or **Entra admin center > Devices > [device] > BitLocker keys**). Match the Key ID.
4. **Read the key to the user by phone.** Never email or paste it into a chat or ticket.
5. After the device boots, ask the user to **restart once more** to make sure it does not ask again.
6. If the key was disclosed, **rotate it**: in Intune, **Devices > [device] > BitLocker key rotation**.
7. Record in the ticket: device name, Key ID, how identity was verified (not the key itself).

## Escalation criteria

Escalate to **L2 Desktop** if:

- No recovery key is found for the Key ID (the device data may not be recoverable: do not reinstall Windows without approval).
- The device asks for the key on every boot (TPM or firmware issue).
- The device was reported lost or stolen (see KB-019).

## Related articles

- [KB-019 Lost or Stolen Laptop or Phone](kb-019-lost-stolen-device.md)
- [KB-017 Windows Update Fails to Install](kb-017-windows-update-failing.md)

## Last reviewed

2026-11-17 by Service Desk.
