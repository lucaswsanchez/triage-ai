---
id: KB-009
title: VPN Does Not Connect
category: Network
level: L1
tags: [vpn, remote-work, network, mfa, connectivity]
estimated_time: 20 min
last_reviewed: 2026-11-17
---

# VPN Does Not Connect

## Summary

Troubleshooting steps when the Acme Corp VPN client fails to connect, disconnects repeatedly, or connects but internal resources are not reachable.

## Applies to

- Acme Corp VPN client on company Windows 10/11 laptops
- Remote employees working from home, hotels or client sites

## Symptoms

- "Unable to connect to the gateway" or "Connection timed out".
- "Authentication failed" or no MFA prompt appears.
- VPN shows *Connected* but intranet sites, file shares or Remote Desktop do not work.
- VPN drops every few minutes.

## Cause

- No working internet connection, or a public Wi-Fi captive portal (hotel login page) not yet accepted.
- Wrong or expired password, account locked, or MFA not approved.
- Network blocks VPN traffic (some guest or hotel networks).
- DNS not switching to internal servers after connecting.
- Outdated VPN client or a conflict with another VPN.

## Resolution

1. **Check the internet first.** Open <https://www.microsoft.com>. If a hotel/guest login page appears, accept it first. If nothing loads, follow KB-010.
2. **Check credentials.** Can the user sign in to <https://portal.office.com>? If not, see KB-001 and KB-003. Make sure they **approve the MFA prompt** within 60 seconds.
3. **Restart the VPN client** completely (exit from the system tray), then connect again.
4. **Try another network**: phone hotspot. If it works there, the original network is blocking VPN; the user should use the hotspot or ask the venue.
5. **Disconnect other VPNs** (personal VPN apps) and pause any third-party firewall.
6. **Connected but nothing works internal?** Test DNS and reachability:

    ```powershell
    ipconfig /all            # the VPN adapter should list Acme DNS servers
    nslookup intranet.acme.example
    Test-NetConnection fileserver01.acme.example -Port 445
    ```

    If DNS fails, run `ipconfig /flushdns`, disconnect and reconnect.
7. **Run the toolkit script** `Test-Connectivity.ps1` and attach its output to the ticket.
8. **Restart the laptop** and check for client updates through the Company Portal.

## Escalation criteria

Escalate to **L2 Network** if:

- Several remote users report VPN problems at the same time (possible gateway outage: P2 or P1).
- Authentication fails with correct credentials and MFA approved.
- The client shows certificate errors.
- The connection drops repeatedly on a stable network.

Include: time of failure, public network type (home/hotel/hotspot), client error message, and the `Test-Connectivity.ps1` output.

## Related articles

- [KB-010 Wi-Fi Connected but No Internet (DNS and Connectivity)](kb-010-wifi-dns-troubleshooting.md)
- [KB-003 Active Directory Account Locked Out](kb-003-ad-account-locked-out.md)
- [KB-002 Set Up or Reset Multi-Factor Authentication (MFA)](kb-002-mfa-setup-and-reset.md)

## Last reviewed

2026-11-17 by Service Desk.
