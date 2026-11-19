---
id: KB-012
title: Printer Shows Offline or Jobs Are Stuck in the Queue
category: Hardware & Printing
level: L1
tags: [printer, print-queue, spooler, offline, printing]
estimated_time: 15 min
last_reviewed: 2026-11-17
---

# Printer Shows Offline or Jobs Are Stuck in the Queue

## Summary

How to bring a network printer back online and clear stuck print jobs, including a safe reset of the Windows Print Spooler.

## Applies to

- Office network printers and multifunction devices (MFPs) at Acme Corp
- Windows 10/11 laptops and desktops

## Symptoms

- Printer status shows **Offline** in **Settings > Bluetooth & devices > Printers & scanners**.
- Documents stay in the queue with status *Error* or *Printing* and nothing comes out.
- "Windows cannot connect to the printer."
- Other users can print, but this user cannot (or vice versa).

## Cause

- The printer is off, asleep, out of paper/toner, or has a paper jam.
- The PC is on guest Wi-Fi or VPN that cannot reach the printer network.
- A corrupted job is blocking the queue.
- Print Spooler service stopped or hung.
- The printer's IP address changed, or an outdated driver.

## Resolution

1. **Check the printer itself**: powered on, no error on the display (paper, toner, jam), network light on. Print a configuration page from the printer panel to see its IP address.
2. **Is it one user or everyone?** If everyone on the floor is affected, it is the printer or the network: go to *Escalation criteria*.
3. **Check the network**: the user must be on the `ACME-CORP` Wi-Fi or wired network (not guest). Test reachability with the printer IP:

    ```powershell
    Test-NetConnection 10.10.3.25 -Port 9100
    ```

4. **Cancel stuck jobs**: open the printer queue (**Printers & scanners > [printer] > Open print queue**) and **Cancel all documents**.
5. **Uncheck "Use Printer Offline"**: in the queue window open the **Printer** menu and make sure *Use Printer Offline* is not ticked.
6. **Reset the Print Spooler** if jobs will not cancel. Use the toolkit script (admin rights required):

    ```powershell
    .\Reset-PrintSpooler.ps1 -WhatIf   # preview what will happen
    .\Reset-PrintSpooler.ps1           # stop spooler, clear queue, start spooler
    ```

7. **Remove and re-add the printer** from **Printers & scanners > Add device**, or reinstall it from the Company Portal.
8. Print a test page and confirm with the user.

## Escalation criteria

Escalate to **L2 Desktop / Facilities** if:

- The printer shows a hardware error code or repeated jams (vendor service call).
- The printer is unreachable from every PC (network or printer fault).
- The driver cannot be installed or the printer must be re-mapped on the print server.

## Related articles

- [KB-010 Wi-Fi Connected but No Internet (DNS and Connectivity)](kb-010-wifi-dns-troubleshooting.md)
- [KB-013 Computer Is Running Slow](kb-013-slow-computer.md)

## Last reviewed

2026-11-17 by Service Desk.
