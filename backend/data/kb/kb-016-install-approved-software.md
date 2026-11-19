---
id: KB-016
title: Install Approved Software from Company Portal
category: Software
level: L1
tags: [software, company-portal, intune, installation, license, approval]
estimated_time: 10 min
last_reviewed: 2026-11-17
---

# Install Approved Software from Company Portal

## Summary

How users install pre-approved applications themselves from **Company Portal**, and how to request software that is not in the catalog.

## Applies to

- Acme Corp Windows 10/11 devices managed by Microsoft Intune
- Standard users (no local administrator rights)

## Symptoms

- "Do you want to allow this app to make changes?" asks for an administrator password.
- The user needs an application for their job and does not know how to get it.
- An install from the Company Portal shows **Failed** or stays at *Pending*.

## Cause

Users do not have local admin rights (a security control). Software is delivered through Intune so it is licensed, patched and approved.

## Resolution

### Install from the catalog

1. Open **Company Portal** from the Start menu.
2. Browse or search for the app (for example *7-Zip*, *Adobe Acrobat Reader*, *Zoom*, *Power BI Desktop*).
3. Click **Install**. Keep the laptop on and connected; progress shows under **Downloads & updates**.
4. If it fails: restart the laptop, open Company Portal > **Settings > Sync** and try again.

### Request software not in the catalog

1. Open a **service request** "New software" with: application name and version, vendor website, business reason, number of users, whether a paid license is required.
2. The request needs **manager approval**; paid software also needs a cost center.
3. IT Security reviews new software (vendor reputation, data handling) before it is packaged.
4. Approved apps are added to Company Portal; the user is notified in the ticket.

!!! warning "Not allowed"
    Do not install software from personal downloads, USB sticks or "portable" versions to bypass controls. Do not share admin passwords. Browser extensions also need approval.

## Escalation criteria

Escalate to **L2 Desktop / Endpoint Management** if:

- A catalog install fails after a restart and sync (attach the error code).
- The app needs local admin rights to run.
- The request is urgent for a client deadline (flag to the team lead).

## Related articles

- [KB-017 Windows Update Fails to Install](kb-017-windows-update-failing.md)
- [KB-020 New Employee Onboarding (IT Setup)](kb-020-employee-onboarding.md)

## Last reviewed

2026-11-17 by Service Desk.
