# Real Accountant Invite Send Receipt

> Scope: public-safe manual-send receipt template and validator for RS2 reviewer invite.

## 한 줄 결론

Receipt template is ready. It does not claim the invite was sent.

## Receipt Fields

- reviewer alias: `reviewer-001`
- manual send completed: False
- channel: manual
- sent at: YYYY-MM-DD
- no raw identifiers requested: True

## Required After Manual Send

Run this ledger update only after the invite was actually sent:

```powershell
python scripts\real_accountant_outreach_update.py --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status sent --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes "invite sent"
```

Then verify the transition:

```powershell
python scripts\real_accountant_outreach_transition_verify.py --expected-status sent --format text
```

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "title": "Real Accountant Invite Send Receipt",
  "actual_send_attested": false,
  "require_sent": false,
  "receipt": {
    "reviewer_alias": "reviewer-001",
    "manual_send_completed": false,
    "channel": "manual",
    "sent_at": "YYYY-MM-DD",
    "invite_packet_path": "docs/reports/real-accountant-session/2026-07-05-reviewer-invite-action-packet.md",
    "ledger_update_command": "python scripts\\real_accountant_outreach_update.py --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status sent --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes \"invite sent\"",
    "no_raw_identifiers_requested": true,
    "operator_attestation": "Fill after manual send. Do not include names, emails, customer identifiers, or source bodies."
  },
  "template_path": "docs/reports/real-accountant-session/invite-send-receipt.template.json",
  "report_path": "docs/reports/real-accountant-session/2026-07-05-invite-send-receipt.md",
  "next_action": "send_reviewer_invite_then_fill_receipt"
}
```
