---
id: KB-017
title: Windows Update Fails to Install
category: Software
level: L2
tags: [windows-update, patching, sfc, dism, error-code]
estimated_time: 45 min
last_reviewed: 2026-11-17
---

# Windows Update Fails to Install

## Summary

How to troubleshoot Windows updates that fail repeatedly, are stuck downloading, or roll back after a restart.

## Applies to

- Windows 10/11 Enterprise devices managed by Intune (Windows Update for Business)

## Symptoms

- **Settings > Windows Update** shows "Install error" with a code such as `0x80070002`, `0x800f081f` or `0x80073712`.
- Update stuck at 0% or a fixed percentage for hours.
- "We couldn't complete the updates. Undoing changes."
- Intune compliance reports the device as out of date.

## Cause

- Not enough free disk space (feature updates need about 20 GB).
- Corrupted Windows Update cache or system files.
- Pending restart from a previous update.
- Third-party drivers or software blocking the update.

## Resolution

1. **Restart** the device and try again: a pending reboot is the most common cause.
2. **Check free space** on `C:` (at least 20 GB). Free space with `Clear-TempFiles.ps1` or **Storage Sense**.
3. **Run the troubleshooter**: **Settings > System > Troubleshoot > Other troubleshooters > Windows Update**.
4. **Repair system files** (elevated PowerShell):

    ```powershell
    DISM /Online /Cleanup-Image /RestoreHealth
    sfc /scannow
    ```

5. **Reset the Windows Update cache** (elevated):

    ```powershell
    Stop-Service wuauserv, bits -Force
    Rename-Item "$env:SystemRoot\SoftwareDistribution" SoftwareDistribution.old
    Start-Service wuauserv, bits
    ```

    Then check for updates again.
6. **Search the error code** in Microsoft documentation and check the event log: **Event Viewer > Applications and Services Logs > Microsoft > Windows > WindowsUpdateClient > Operational**.
7. **Install manually** from the Microsoft Update Catalog only if the specific KB is approved by the patching team.

## Escalation criteria

Escalate to **L3 Endpoint Management** if:

- DISM cannot repair the image.
- The same update fails on several devices (possible bad update or policy issue: pause the ring).
- The device is out of compliance for more than 14 days (security risk).

## Related articles

- [KB-013 Computer Is Running Slow](kb-013-slow-computer.md)
- [KB-016 Install Approved Software from Company Portal](kb-016-install-approved-software.md)
- [KB-014 BitLocker Recovery Key Requested at Startup](kb-014-bitlocker-recovery.md)

## Last reviewed

2026-11-17 by Service Desk.
