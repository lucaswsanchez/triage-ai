---
id: KB-021
title: Employee Offboarding (IT Deprovisioning)
category: Onboarding & Offboarding
level: L2
tags: [offboarding, leaver, deprovisioning, active-directory, mailbox, security]
estimated_time: 45 min
last_reviewed: 2026-11-17
---

# Employee Offboarding (IT Deprovisioning)

## Summary

How to securely remove a leaving employee's access on their last day while preserving the data the business needs (mailbox, OneDrive files).

## Applies to

- Employees, contractors and interns leaving Acme Corp
- Hybrid Active Directory + Microsoft 365, Intune-managed devices

## Symptoms

- HR submits a **Leaver** service request with the last working day and time.
- Urgent variant: **immediate termination** (access must be removed within 1 hour).

## Cause

Standard service request; not a fault.

## Resolution

Do the account steps **at the agreed time** (end of the last day, or immediately for terminations).

1. **Confirm the request** with HR: name, last day and time, manager, who receives the mailbox and files.
2. **Disable sign-in**:

    ```powershell
    Disable-ADAccount -Identity jdoe
    Set-ADUser -Identity jdoe -Description "Disabled $(Get-Date -Format yyyy-MM-dd) - leaver, ticket REQ-1234"
    ```

    Reset the password to a random value and **revoke all sessions** in Entra ID.
3. **Remove access**: remove the user from security and distribution groups (record the list in the ticket first), remove admin roles, and move the account to the *Disabled Users* OU.
4. **Mailbox**: convert to a **shared mailbox** (keeps data without a license) and grant the manager access, or set an auto-reply agreed with HR.
5. **OneDrive**: give the manager access to the OneDrive files (retention: 30 days by default).
6. **Licenses**: remove Microsoft 365 licenses after the mailbox conversion.
7. **Devices**: collect the laptop, phone and badge. Wipe and re-provision via Intune/Autopilot. Retire the user from personal phones (selective wipe).
8. **Other systems**: VPN, SaaS apps with separate accounts, shared passwords the person knew (rotate them).
9. Close the ticket with the checklist completed and timestamps.

!!! info "Inactive accounts review"
    Accounts of people who left but were never deprovisioned are a security risk. The toolkit script `Get-InactiveAccount.ps1` lists accounts with no sign-in for 90+ days for a monthly review.

## Escalation criteria

Escalate to **Security and the team lead** if:

- It is an immediate or hostile termination.
- The person had administrator or finance system access.
- Devices are not returned within 5 business days.

## Related articles

- [KB-020 New Employee Onboarding (IT Setup)](kb-020-employee-onboarding.md)
- [KB-019 Lost or Stolen Laptop or Phone](kb-019-lost-stolen-device.md)
- [KB-008 Access a Shared Mailbox in Outlook](kb-008-shared-mailbox-access.md)

## Last reviewed

2026-11-17 by Service Desk.
