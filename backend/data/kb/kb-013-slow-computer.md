---
id: KB-013
title: Computer Is Running Slow
category: Hardware & Printing
level: L1
tags: [performance, slow, disk-space, ram, task-manager, startup]
estimated_time: 30 min
last_reviewed: 2026-11-17
---

# Computer Is Running Slow

## Summary

A structured way to find out why a Windows PC is slow (CPU, memory, disk, startup apps, updates) and fix the most common causes without reinstalling.

## Applies to

- Acme Corp Windows 10/11 laptops and desktops

## Symptoms

- Apps take a long time to open or freeze ("Not responding").
- The fan is constantly loud, or the laptop is hot.
- Boot and sign-in take several minutes.
- Low disk space warnings.

## Cause

- The computer has not been restarted in days or weeks (high uptime).
- Too many startup apps or browser tabs; RAM fully used.
- Disk almost full (less than 10% free).
- Windows Update or antivirus scan running in the background.
- Failing disk or overheating (dust, blocked vents).

## Resolution

1. **Ask when it started** and what changed (new software, update, after a trip).
2. **Check uptime and restart**: in Task Manager > **Performance > CPU**, look at *Up time*. If it is more than 3 days, **restart** (not shut down: Fast Startup keeps the session).
3. **Run the diagnostics script** to capture a baseline (OS, disk, RAM, uptime, network) as an HTML report:

    ```powershell
    .\Get-SystemDiagnostics.ps1 -OutputPath "$env:USERPROFILE\Desktop"
    ```

4. **Task Manager** (++ctrl+shift+esc++) > **Processes**, sort by *CPU*, *Memory* and *Disk*. Identify the top consumer. Close unneeded apps and browser tabs.
5. **Disable unnecessary startup apps**: **Task Manager > Startup apps**, disable non-business apps with *High* impact.
6. **Free disk space** if less than 10% free:
    - **Settings > System > Storage > Temporary files** and remove them, or run the toolkit script `Clear-TempFiles.ps1` (preview first with `-WhatIf`).
    - Empty the Recycle Bin, move large personal files to OneDrive (set to *Free up space*).
7. **Check Windows Update**: **Settings > Windows Update**. Install pending updates and restart.
8. **Check the disk health**:

    ```powershell
    Get-PhysicalDisk | Select-Object FriendlyName, MediaType, HealthStatus, OperationalStatus
    ```

9. **Physical check**: vents not blocked, laptop on a hard surface, power plan set to *Balanced* or *Best performance* when plugged in.
10. Confirm with the user after a restart and attach the before/after diagnostics reports to the ticket.

## Escalation criteria

Escalate to **L2 Desktop** if:

- Disk `HealthStatus` is not *Healthy* or there are disk errors in Event Viewer (back up data first).
- RAM is consistently above 90% with only business apps (possible hardware upgrade request).
- Malware is suspected (unknown processes, pop-ups, browser redirects): treat as a **security incident**.
- The device is older than the 4-year replacement cycle.

## Related articles

- [KB-007 OneDrive Is Not Syncing](kb-007-onedrive-not-syncing.md)
- [KB-006 Microsoft Teams Has No Audio or Camera](kb-006-teams-audio-camera.md)
- [KB-018 Report a Suspicious Email (Phishing)](kb-018-phishing-suspicious-email.md)

## Last reviewed

2026-11-17 by Service Desk.
