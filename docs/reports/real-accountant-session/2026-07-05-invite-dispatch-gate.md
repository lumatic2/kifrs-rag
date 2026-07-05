# RS2 Invite Dispatch Gate

> Scope: pre-send gate for the real accountant reviewer invite and post-send ledger update path.

## 한 줄 결론

The reviewer invite is ready for manual dispatch. This gate proves the current ledger is still `not_sent`, the invite packet uses a public-safe alias, and the generated post-send command can move a copied ledger to `sent` without protected identifiers.

## Current State

- ok: True
- invite: `docs/reports/real-accountant-session/2026-07-05-session-invite.md`
- ledger: `docs/reports/real-accountant-session/outreach-log.sample.jsonl`
- reviewer alias: `reviewer-001`
- subject: 회계 AI PoC 30분 피드백 요청 초안
- current outreach counts: {'completed': 0, 'declined': 0, 'not_sent': 1, 'responded': 0, 'scheduled': 0, 'sent': 0}
- current next action: Send reviewer invite and update outreach ledger to sent.

## After Manual Send

Run this command after the operator actually sends the invite:

```powershell
python scripts\real_accountant_outreach_update.py --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status sent --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes "invite sent"
```

## Post-Send Simulation

- ok: True
- counts after simulation: {'completed': 0, 'declined': 0, 'not_sent': 0, 'responded': 0, 'scheduled': 0, 'sent': 1}
- simulated row: `{'reviewer_alias': 'reviewer-001', 'status': 'sent', 'invite_sent': True, 'channel': 'manual', 'contacted_at': '2026-07-05', 'follow_up_by': '2026-07-08', 'notes': 'invite sent'}`

## Boundary

- This gate does not send the invite.
- The operator must send the message manually and then run the generated ledger update command.
- No raw contracts, customer identifiers, company names, or private source bodies should be requested.

## Next Leaf

operator sends reviewer invite, updates outreach ledger to sent, then schedules RS2 session

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "gate_id": "rs2-invite-dispatch-gate",
  "invite_path": "docs/reports/real-accountant-session/2026-07-05-session-invite.md",
  "ledger_path": "docs/reports/real-accountant-session/outreach-log.sample.jsonl",
  "reviewer_alias": "reviewer-001",
  "subject": "회계 AI PoC 30분 피드백 요청 초안",
  "current_outreach_counts": {
    "completed": 0,
    "declined": 0,
    "not_sent": 1,
    "responded": 0,
    "scheduled": 0,
    "sent": 0
  },
  "current_next_action": "Send reviewer invite and update outreach ledger to sent.",
  "post_send_update_command": "python scripts\\real_accountant_outreach_update.py --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status sent --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes \"invite sent\"",
  "post_send_simulation": {
    "ok": true,
    "errors": [],
    "counts": {
      "completed": 0,
      "declined": 0,
      "not_sent": 0,
      "responded": 0,
      "scheduled": 0,
      "sent": 1
    },
    "row": {
      "reviewer_alias": "reviewer-001",
      "status": "sent",
      "invite_sent": true,
      "channel": "manual",
      "contacted_at": "2026-07-05",
      "follow_up_by": "2026-07-08",
      "notes": "invite sent"
    }
  },
  "boundary": [
    "This gate does not send the invite.",
    "The operator must send the message manually and then run the generated ledger update command.",
    "No raw contracts, customer identifiers, company names, or private source bodies should be requested."
  ],
  "report_path": "docs/reports/real-accountant-session/2026-07-05-invite-dispatch-gate.md",
  "next_leaf": "operator sends reviewer invite, updates outreach ledger to sent, then schedules RS2 session"
}
```
