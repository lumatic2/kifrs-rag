# Real Accountant Invite Receipt Apply

> Scope: validate a filled invite-send receipt before applying the `sent` outreach ledger update.

## 한 줄 결론

Filled receipt is valid; dry run did not mutate the outreach ledger.

## Apply Result

- ok: True
- dry run: True
- receipt: `docs/reports/real-accountant-session/invite-receipt-apply.demo.json`
- ledger: `docs/reports/real-accountant-session/outreach-log.sample.jsonl`
- receipt ok: True
- actual send attested: True
- ledger updated: False

## Boundary

- This command does not send the reviewer invite.
- It only applies a ledger update when a filled receipt already attests manual send.
- Do not run this against the real ledger until the invite was actually sent.

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "title": "Real Accountant Invite Receipt Apply",
  "dry_run": true,
  "receipt_path": "docs/reports/real-accountant-session/invite-receipt-apply.demo.json",
  "ledger": "docs/reports/real-accountant-session/outreach-log.sample.jsonl",
  "receipt_ok": true,
  "actual_send_attested": true,
  "ledger_updated": false,
  "row": null,
  "transition": null,
  "report_path": "docs/reports/real-accountant-session/2026-07-05-invite-receipt-apply.md"
}
```
