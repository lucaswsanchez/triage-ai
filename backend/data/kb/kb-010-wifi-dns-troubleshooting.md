---
id: KB-010
title: Wi-Fi Connected but No Internet (DNS and Connectivity)
category: Network
level: L1
tags: [wifi, dns, ipconfig, nslookup, ping, tracert, network]
estimated_time: 15 min
last_reviewed: 2026-11-17
---

# Wi-Fi Connected but No Internet (DNS and Connectivity)

## Summary

A layered method (adapter > IP > gateway > DNS > internet) to find out why a Windows laptop shows "Connected, no internet" or cannot open websites, using `ipconfig`, `ping`, `nslookup` and `tracert`.

## Applies to

- Windows 10/11 laptops on office Wi-Fi (`ACME-CORP`), guest Wi-Fi or home networks
- Wired Ethernet with the same symptoms

## Symptoms

- Network icon shows **No internet** or a yellow warning.
- "DNS server isn't responding" or `DNS_PROBE_FINISHED_NXDOMAIN` in the browser.
- Some sites load and others do not.
- Teams and Outlook show "Disconnected".

## Cause

- Weak signal or connected to the wrong network.
- No valid IP address from DHCP (address starts with `169.254.x.x`).
- Gateway unreachable (router or access point problem).
- DNS server not responding or stale DNS cache.
- Proxy or VPN misconfiguration.

## Resolution

Work from the bottom layer up and **stop at the first failing test**.

1. **Basics**: Wi-Fi is on, Airplane mode off, connected to the right network, signal at least 2 bars. Try forgetting the network and reconnecting.
2. **Check the IP configuration**:

    ```powershell
    ipconfig /all
    ```

    - `IPv4 Address` of `169.254.x.x` means no DHCP lease. Run `ipconfig /release` then `ipconfig /renew`.
    - Note the **Default Gateway** and **DNS Servers**.
3. **Ping the gateway** (replace with the value from step 2):

    ```powershell
    ping 192.168.1.1
    ```

    Fails? The problem is local (Wi-Fi, access point or router). Restart the adapter: **Settings > Network & internet > Advanced network settings > Disable / Enable**.
4. **Ping an internet IP** (no DNS involved):

    ```powershell
    ping 1.1.1.1
    ```

    Gateway works but this fails? The internet link or firewall is down: escalate if at the office.
5. **Test DNS**:

    ```powershell
    nslookup www.microsoft.com
    nslookup www.microsoft.com 1.1.1.1
    ```

    If the first fails and the second works, the configured DNS server is the problem. Flush the cache and retry:

    ```powershell
    ipconfig /flushdns
    ```

6. **Trace the path** when a specific site is slow or unreachable:

    ```powershell
    tracert www.microsoft.com
    ```

    Note at which hop the timeouts (`* * *`) start and include it in the ticket.
7. **Reset the network stack** (requires admin; restart afterwards):

    ```powershell
    netsh winsock reset
    netsh int ip reset
    ```

8. Run `Test-Connectivity.ps1` from the toolkit to capture all of the above in one report.

## Escalation criteria

Escalate to **L2 Network** if:

- Several users on the same floor or network are affected (possible access point or DHCP outage).
- The gateway is unreachable for everyone.
- DNS fails on internal names only (internal DNS server problem).

Include: `ipconfig /all` output, which step failed, location (floor/room) and the `Test-Connectivity.ps1` report.

## Related articles

- [KB-009 VPN Does Not Connect](kb-009-vpn-not-connecting.md)
- [KB-005 Outlook Is Not Syncing Email](kb-005-outlook-not-syncing.md)

## Last reviewed

2026-11-17 by Service Desk.
