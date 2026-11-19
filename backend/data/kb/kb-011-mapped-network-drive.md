---
id: KB-011
title: Mapped Network Drive Is Missing or Disconnected
category: Network
level: L1
tags: [mapped-drive, file-share, smb, network, net-use, group-policy]
estimated_time: 15 min
last_reviewed: 2026-11-17
---

# Mapped Network Drive Is Missing or Disconnected

## Summary

How to restore a mapped department drive (for example `S:` or `P:`) that shows a red X, is missing from *This PC* or asks for credentials.

## Applies to

- Windows 10/11 company devices
- Drives mapped by Group Policy at sign-in (`S:` Shared, `P:` Projects, `H:` Home)

## Symptoms

- Drive shows a red **X** and "Disconnected network drive".
- Drive letter missing from *This PC*.
- "The network path was not found" (error 0x80070035).
- Repeated credential prompts when opening the drive.

## Cause

- The device is off the corporate network and VPN is not connected.
- The drive mapping ran before the network was ready (common on Wi-Fi at sign-in).
- Saved credentials in Credential Manager are outdated after a password change.
- The user lost group membership that grants access.

## Resolution

1. **Check the connection**: at the office (corporate Wi-Fi/cable) or connected to VPN? If not, connect VPN (KB-009).
2. **Test the server**:

    ```powershell
    Test-NetConnection fileserver01.acme.example -Port 445
    ```

    `TcpTestSucceeded : False` means a network/VPN problem, not a drive problem.
3. **Open the path directly**: press ++win+r++ and type `\\fileserver01\Shared`. If it opens, only the mapping is broken.
4. **Re-apply the mappings**:

    ```powershell
    gpupdate /force
    ```

    Sign out and back in.
5. **Map manually** if still missing (temporary fix):

    ```powershell
    net use S: \\fileserver01\Shared /persistent:yes
    ```

6. **Clear old credentials**: **Control Panel > Credential Manager > Windows Credentials**, remove entries for `fileserver01`, then reopen the drive.
7. If you get "Access denied", follow KB-004 (permissions request).

## Escalation criteria

Escalate to **L2 Infrastructure** if:

- The file server is unreachable for several users (possible server outage: P2 or P1).
- `gpupdate` reports errors applying Group Policy.
- The mapping is missing for a whole department.

## Related articles

- [KB-004 Request or Grant Access to a Shared Folder](kb-004-shared-folder-permissions.md)
- [KB-009 VPN Does Not Connect](kb-009-vpn-not-connecting.md)
- [KB-010 Wi-Fi Connected but No Internet (DNS and Connectivity)](kb-010-wifi-dns-troubleshooting.md)

## Last reviewed

2026-11-17 by Service Desk.
