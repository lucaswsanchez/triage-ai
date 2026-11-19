---
id: KB-007
title: OneDrive Is Not Syncing
category: Microsoft 365
level: L1
tags: [onedrive, sync, sharepoint, files, storage]
estimated_time: 20 min
last_reviewed: 2026-11-17
---

# OneDrive Is Not Syncing

## Summary

How to fix OneDrive for Business when files do not upload, show a red X, or the cloud icon says sync is paused or has errors.

## Applies to

- OneDrive for Business sync client on Windows 10/11
- Known Folder Move (Desktop, Documents, Pictures) and synced SharePoint libraries

## Symptoms

- Red **X** or "Sync pending" icons on files.
- OneDrive cloud icon is grey, shows a pause symbol or a red error badge.
- "You're not signed in to OneDrive" or "Your OneDrive is full".
- A colleague cannot see the latest version of a shared file.

## Cause

- Sync paused, user signed out, or no network.
- File name contains invalid characters (`" * : < > ? / \ |`), or the full path is longer than 400 characters.
- File is open/locked by another program, or larger than 250 GB.
- OneDrive storage quota full (1 TB) or local disk full.
- Corrupted sync client state.

## Resolution

1. Click the **OneDrive cloud icon** in the system tray and read the message. If it says **Paused**, click **Resume syncing**.
2. If it asks to sign in, sign in with the work account.
3. Open **View sync problems** (in the OneDrive menu) to see the exact file and reason.
4. **Fix file names and paths**: rename files with invalid characters and shorten very long folder paths.
5. **Close the file** in Word/Excel/other apps and wait a minute for it to upload.
6. **Check space**: OneDrive menu > **Settings > Account** shows quota; **This PC** shows local disk free space. Free disk space if under 10% (see KB-013).
7. **Restart OneDrive**: OneDrive menu > **Settings (gear) > Quit OneDrive**, then open OneDrive from the Start menu.
8. **Reset OneDrive** if errors persist (files already in the cloud are safe; local-only changes should be backed up first):

    ```powershell
    & "$env:LOCALAPPDATA\Microsoft\OneDrive\OneDrive.exe" /reset
    ```

    If OneDrive does not reopen within two minutes, start it manually from the Start menu. Resync can take a while.
9. Confirm with the user that the file shows a **green check** and is visible on <https://www.office.com> under *My files*.

## Escalation criteria

Escalate to **L2 Collaboration** if:

- The issue affects a SharePoint library for several users.
- Files are missing from both the PC and OneDrive online (check the OneDrive **Recycle bin** first; restores beyond 93 days need L2).
- The user needs more than 1 TB of storage.
- Reset does not resolve the sync errors.

## Related articles

- [KB-005 Outlook Is Not Syncing Email](kb-005-outlook-not-syncing.md)
- [KB-013 Computer Is Running Slow](kb-013-slow-computer.md)

## Last reviewed

2026-11-17 by Service Desk.
