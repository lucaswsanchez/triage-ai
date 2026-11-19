---
id: KB-006
title: Microsoft Teams Has No Audio or Camera
category: Microsoft 365
level: L1
tags: [teams, audio, microphone, camera, headset, privacy]
estimated_time: 15 min
last_reviewed: 2026-11-17
---

# Microsoft Teams Has No Audio or Camera

## Summary

How to fix Teams meetings where the user cannot hear others, others cannot hear the user, or the camera shows a black screen or "No camera available".

## Applies to

- New Microsoft Teams (work or school) on Windows 10/11
- USB and Bluetooth headsets, built-in and USB webcams, docking stations

## Symptoms

- "We can't find a microphone" or "No camera available".
- Others say the user is silent, or the user hears nothing.
- The camera preview is black or shows a slashed camera icon.
- Audio works in other apps but not in Teams.

## Cause

- Teams is using the wrong audio or video device (common after docking or pairing a headset).
- Windows privacy settings block microphone or camera access.
- Another app (Zoom, browser tab, camera software) is holding the camera.
- Physical mute switch, camera shutter or function key (++f8++ / ++f10++) turned on.
- Outdated drivers or Teams cache problems.

## Resolution

1. **Quick physical checks**: headset mute switch, laptop camera shutter, keyboard camera/mic keys, USB cable firmly connected (try another port, not a hub).
2. **Pick the right device** in Teams: **Settings and more (…) > Settings > Devices**. Select the headset under *Speaker* and *Microphone*, and the correct *Camera*. Click **Make a test call**.
3. **During a meeting**: **More > Settings > Device settings** lets you switch devices without leaving.
4. **Windows privacy settings**: **Settings > Privacy & security > Microphone** and **Camera**. Turn on *Microphone access*, *Camera access*, *Let apps access…* and *Let desktop apps access…*.
5. **Close other apps** that may use the camera (Zoom, Webex, browser tabs with video, the Windows Camera app), then restart Teams.
6. **Check Windows sound**: right-click the speaker icon > **Sound settings**. Make sure the headset is the default output and input and that the input level moves when speaking.
7. **Clear the Teams cache**: quit Teams from the system tray, then run in PowerShell:

    ```powershell
    Get-Process ms-teams -ErrorAction SilentlyContinue | Stop-Process -Force
    Remove-Item "$env:LOCALAPPDATA\Packages\MSTeams_8wekyb3d8bbwe\LocalCache\Microsoft\MSTeams" -Recurse -Force
    ```

    Start Teams again (the user stays signed in).
8. **Update drivers**: run Windows Update including *Optional updates > Driver updates*, or install the manufacturer's camera/audio driver.
9. Confirm with a **test call** and a short meeting with the user.

## Escalation criteria

Escalate to **L2 Desktop** if:

- The device is not detected in **Device Manager** at all, or shows an error code.
- The issue happens on a known-good second headset/camera (possible hardware or driver fault: arrange a replacement).
- Teams crashes or cannot be reinstalled.

## Related articles

- [KB-013 Computer Is Running Slow](kb-013-slow-computer.md)
- [KB-005 Outlook Is Not Syncing Email](kb-005-outlook-not-syncing.md)

## Last reviewed

2026-11-17 by Service Desk.
