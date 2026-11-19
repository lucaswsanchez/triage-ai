---
title: Priority Matrix & SLAs
---

# Priority Matrix & SLAs

Priority is **not** how loud the caller is. It is calculated from two factors:

- **Impact**: how many people or how much of the business is affected.
- **Urgency**: how fast the impact grows, or whether there is a workaround.

## Impact

| Level | Definition | Examples |
|---|---|---|
| **High** | Whole company, a site, a department, or a business-critical service. | Email down for everyone, VPN gateway down, ransomware. |
| **Medium** | A team or a group of users, or a VIP whose work affects many. | One floor without Wi-Fi, a team's shared mailbox unavailable. |
| **Low** | A single user. | One laptop slow, one user's Outlook not syncing. |

## Urgency

| Level | Definition | Examples |
|---|---|---|
| **High** | Work stopped, no workaround, or financial/security/legal exposure now. | Cannot sign in at all, phishing link clicked, payroll deadline today. |
| **Medium** | Work degraded, a workaround exists but is painful. | Outlook desktop broken but Outlook on the web works. |
| **Low** | Inconvenience, work continues normally. | Second monitor flickers, cosmetic issue. |

## Matrix

<div class="matrix-table" markdown>

| Impact ↓ / Urgency → | **High** | **Medium** | **Low** |
|---|---|---|---|
| **High** | <span class="badge badge--p1">P1 Critical</span> | <span class="badge badge--p2">P2 High</span> | <span class="badge badge--p3">P3 Medium</span> |
| **Medium** | <span class="badge badge--p2">P2 High</span> | <span class="badge badge--p3">P3 Medium</span> | <span class="badge badge--p4">P4 Low</span> |
| **Low** | <span class="badge badge--p3">P3 Medium</span> | <span class="badge badge--p4">P4 Low</span> | <span class="badge badge--p4">P4 Low</span> |

</div>

## SLA targets

Targets are measured in **business hours** (Mon–Fri 08:00–18:00) except P1, which is 24/7.

| Priority | First response | Resolution target | Update frequency | Who is notified |
|---|---|---|---|---|
| <span class="badge badge--p1">P1 Critical</span> | 15 min | 4 hours | Every 30 min | Team lead, IT manager, status page |
| <span class="badge badge--p2">P2 High</span> | 30 min | 8 business hours | Every 2 hours | Team lead |
| <span class="badge badge--p3">P3 Medium</span> | 4 business hours | 3 business days | Daily | — |
| <span class="badge badge--p4">P4 Low</span> | 1 business day | 5 business days | Every 2 days | — |

**Service requests** use the fulfillment time of their catalog item instead (for example: new hire account 5 business days, shared folder access 2 business days, software from Company Portal same day).

!!! note "SLA clock"
    The resolution clock **pauses** while the ticket is *Pending user* (waiting for information the user must provide) and resumes when they reply. It never pauses for internal escalations.

## Examples

| Ticket | Impact | Urgency | Priority |
|---|---|---|---|
| Exchange Online outage, no one can send email | High | High | **P1** |
| CEO's laptop will not boot, board meeting in 1 hour | Medium (VIP) | High | **P2** |
| User clicked a phishing link and entered their password | Low (one user) → treat as Medium (security) | High | **P2** |
| Sales team's shared mailbox missing, workaround via web | Medium | Medium | **P3** |
| One user's Outlook desktop not syncing, web works | Low | Medium | **P4** |
| Printer on floor 2 offline, floor 1 printer works | Medium | Low | **P4** |

!!! tip "Re-prioritize when facts change"
    If a P4 "my Outlook is slow" becomes five calls from the same office in 20 minutes, it is now a **P2** with a potential major incident. Link the tickets to one parent incident.
