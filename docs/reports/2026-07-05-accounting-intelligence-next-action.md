# Accounting Intelligence Next Action

> Scope: the single next operator-facing action from the Accounting Intelligence decision queue.

## 한 줄 결론

Next: send the real accountant reviewer invite; implementation expansion should wait for actual feedback evidence.

## Next Action

- decision: `send_reviewer_invite`
- status: needs_user_action
- operator action required: True
- decide: Which reviewer should receive the invite, and should the invite be sent now?
- blocker: reviewer invite has not been sent
- command: `python scripts\real_accountant_invite_packet.py --format text --write`
- receipt: `python scripts\real_accountant_invite_send_receipt.py --write-template --format text --write`
- after: `python scripts\real_accountant_outreach_update.py --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status sent --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes "invite sent"`
- verify: `python scripts\real_accountant_outreach_transition_verify.py --expected-status sent --format text`
- evidence: `docs/reports/real-accountant-session/2026-07-05-operator-execution-brief.md`

## Queue Snapshot

- mode: cached_reports
- open decisions: 4
- operator action required: 2
- decision queue report: `docs/reports/2026-07-05-accounting-intelligence-decision-queue.md`

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "title": "Accounting Intelligence Next Action",
  "mode": "cached_reports",
  "recommended_next_decision": "send_reviewer_invite",
  "status": "needs_user_action",
  "operator_action_required": true,
  "user_decision": "Which reviewer should receive the invite, and should the invite be sent now?",
  "current_blocker": "reviewer invite has not been sent",
  "next_command": "python scripts\\real_accountant_invite_packet.py --format text --write",
  "receipt_command": "python scripts\\real_accountant_invite_send_receipt.py --write-template --format text --write",
  "after_command": "python scripts\\real_accountant_outreach_update.py --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status sent --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes \"invite sent\"",
  "verify_command": "python scripts\\real_accountant_outreach_transition_verify.py --expected-status sent --format text",
  "evidence": "docs/reports/real-accountant-session/2026-07-05-operator-execution-brief.md",
  "open_decision_count": 4,
  "operator_action_required_count": 2,
  "report_path": "docs/reports/2026-07-05-accounting-intelligence-next-action.md",
  "decision_queue_report": "docs/reports/2026-07-05-accounting-intelligence-decision-queue.md"
}
```
