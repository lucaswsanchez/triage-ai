---
id: KB-020
title: New Employee Onboarding (IT Setup)
category: Onboarding & Offboarding
level: L2
tags: [onboarding, new-hire, active-directory, microsoft-365, licensing, provisioning]
estimated_time: 60 min
last_reviewed: 2026-11-17
---

# New Employee Onboarding (IT Setup)

## Summary

The technical steps to provision a new employee's account, licenses, access and device so they are productive on day one. The process-level checklist lives in [Onboarding & Offboarding](../processes/onboarding-offboarding.md).

## Applies to

- New employees, contractors and interns
- Hybrid Active Directory + Microsoft 365 environment, Intune-managed laptops

## Symptoms

- HR submits a **New hire** service request (at least 5 business days before the start date).

## Cause

Standard service request; not a fault.

## Resolution

1. **Validate the request**: HR ticket includes full name, job title, department, manager, start date, location and required access. Missing data? Ask HR before starting.
2. **Create the AD account** following the naming standard `firstname.lastname`. For several hires at once, use the toolkit script with a CSV:

    ```powershell
    .\New-BulkADUser.ps1 -CsvPath .\new-hires.csv -WhatIf   # preview
    .\New-BulkADUser.ps1 -CsvPath .\new-hires.csv           # create
    ```

3. **Set attributes**: department, title, manager, office. Place the account in the correct OU so the right Group Policies apply.
4. **Add groups** according to the role template (department share groups, distribution lists, Teams). Only what the manager approved (least privilege).
5. **Sync and license**: after the directory sync, assign the **Microsoft 365 E3** license (or the group that assigns it) in the admin center.
6. **Prepare the device**: assign a laptop in Intune (Autopilot) to the user, confirm it is encrypted and compliant.
7. **Credentials**: generate a temporary password and a **Temporary Access Pass** for MFA registration. Deliver them to the manager or in person on day one, never by email to a personal address.
8. **Day one**: the user signs in, registers MFA (KB-002), opens Outlook and Teams, and confirms access to the department share.
9. Close the ticket with a summary of groups, license and device serial number.

## Escalation criteria

Escalate to **L3 / team lead** if:

- The start date is less than 2 business days away (risk of a non-productive first day).
- Access to sensitive systems (Finance ERP, HR, admin roles) is requested: needs extra approval.
- No laptop is in stock.

## Related articles

- [KB-021 Employee Offboarding (IT Deprovisioning)](kb-021-employee-offboarding.md)
- [KB-002 Set Up or Reset Multi-Factor Authentication (MFA)](kb-002-mfa-setup-and-reset.md)
- [KB-004 Request or Grant Access to a Shared Folder](kb-004-shared-folder-permissions.md)
- [KB-016 Install Approved Software from Company Portal](kb-016-install-approved-software.md)

## Last reviewed

2026-11-17 by Service Desk.
