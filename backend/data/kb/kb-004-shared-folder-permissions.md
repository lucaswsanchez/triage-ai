---
id: KB-004
title: Request or Grant Access to a Shared Folder
category: Accounts & Identity
level: L2
tags: [permissions, file-share, ntfs, security-groups, access-request, active-directory]
estimated_time: 20 min
last_reviewed: 2026-11-17
---

# Request or Grant Access to a Shared Folder

## Summary

How users request access to a department file share, and how L2 grants it correctly through Active Directory security groups (never by adding individual users to folder permissions).

## Applies to

- Department shares on the Acme Corp file server (`\\fileserver01\<Department>`)
- Active Directory security groups following the naming standard `FS-<Share>-<RO|RW>`

## Symptoms

- "You don't currently have permission to access this folder."
- "Access is denied" when opening, saving or deleting a file.
- A new hire or someone who moved departments cannot see a share their team uses.

## Cause

- The user is not a member of the security group that grants access.
- The user was added to the group recently but has not signed out since (the Kerberos ticket still has the old group list).
- The user has read-only access but needs to edit.

## Resolution

### For the user (L1 / self-service)

1. Open a **service request** "Access to shared folder" with: the full folder path, **read** or **read/write**, and a business reason.
2. Your **manager or the folder owner must approve** the request. The Service Desk cannot grant access without approval.

### For the technician (L2)

1. **Confirm approval** from the data owner listed for the share. Attach it to the ticket.
2. **Find the right group**. Check which groups are on the folder: right-click the folder > **Properties > Security > Advanced**, or:

    ```powershell
    (Get-Acl '\\fileserver01\Finance').Access |
        Select-Object IdentityReference, FileSystemRights, AccessControlType
    ```

3. **Add the user to the group** (least privilege: RO unless RW was approved):

    ```powershell
    Add-ADGroupMember -Identity 'FS-Finance-RO' -Members jdoe
    Get-ADUser jdoe -Properties MemberOf | Select-Object -ExpandProperty MemberOf
    ```

4. Ask the user to **sign out and sign back in** (or restart) so the new group membership applies, then open the share.
5. Record the group change and approver in the ticket.

!!! danger "Do not"
    - Do not add individual user accounts directly to the folder ACL.
    - Do not grant *Full control* to users.
    - Do not copy another user's group memberships ("make them like Jane") without approval for each group.

## Escalation criteria

Escalate to **L3 / Infrastructure** if:

- No suitable group exists and a new share or group must be created.
- Inheritance is broken or the permissions on the folder look wrong.
- The request is for sensitive data (HR, Payroll, Legal): requires security team review.

## Related articles

- [KB-011 Mapped Network Drive Is Missing or Disconnected](kb-011-mapped-network-drive.md)
- [KB-020 New Employee Onboarding (IT Setup)](kb-020-employee-onboarding.md)
- [KB-003 Active Directory Account Locked Out](kb-003-ad-account-locked-out.md)

## Last reviewed

2026-11-17 by Service Desk.
