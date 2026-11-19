---
id: KB-015
title: External Monitor or Docking Station Not Working
category: Hardware & Printing
level: L1
tags: [monitor, docking-station, usb-c, display, hardware]
estimated_time: 15 min
last_reviewed: 2026-11-17
---

# External Monitor or Docking Station Not Working

## Summary

Steps to fix "No signal" on external monitors, a dock that does not charge the laptop, or USB devices on the dock that stop working.

## Applies to

- Acme Corp standard USB-C / Thunderbolt docking stations and desk monitors
- Windows 10/11 laptops

## Symptoms

- Monitor shows **No signal** or stays black.
- Only one of two monitors works.
- Wrong resolution, flickering or blurry text.
- Keyboard, mouse or Ethernet on the dock do not work; laptop not charging.

## Cause

- Loose cable or monitor on the wrong input source.
- Laptop connected to a USB-C port that does not support video.
- Dock firmware or display driver outdated.
- Windows display settings set to *Duplicate* or *Show only on 1*.

## Resolution

1. **Check the basics**: monitor powered on, correct **input source** (HDMI/DisplayPort) selected with the monitor buttons, cables firmly connected on both ends.
2. **Reconnect in order**: unplug the dock's USB-C cable from the laptop, wait 10 seconds, plug it back into the port with the **Thunderbolt/DisplayPort icon**.
3. **Power-cycle the dock**: unplug its power adapter for 30 seconds.
4. **Detect displays**: press ++win+p++ and select **Extend**. Then **Settings > System > Display > Multiple displays > Detect**.
5. **Set resolution**: in *Display* settings select each monitor and choose the *(Recommended)* resolution and scale.
6. **Update drivers and firmware**: run Windows Update (including optional driver updates) and the dock firmware update from the Company Portal.
7. **Swap to isolate**: try another cable, another monitor, or another desk's dock. Note which part follows the fault.
8. Restart the laptop with the dock connected and confirm with the user.

## Escalation criteria

Escalate to **L2 Desktop** if:

- The fault follows a specific dock, cable or monitor (hardware replacement request).
- The laptop does not charge from any dock or charger.
- The display driver fails to install or shows an error in Device Manager.

## Related articles

- [KB-006 Microsoft Teams Has No Audio or Camera](kb-006-teams-audio-camera.md)
- [KB-013 Computer Is Running Slow](kb-013-slow-computer.md)

## Last reviewed

2026-11-17 by Service Desk.
