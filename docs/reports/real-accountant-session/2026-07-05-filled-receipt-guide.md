# Real Accountant Filled Receipt Guide

> Scope: operator guide for filling the RS2 invite-send receipt after a real manual send.

## One-Line Result

After the reviewer invite is actually sent, fill the receipt template with public-safe facts, apply it through the receipt validator, then verify the outreach ledger routes to sent-state handling.

## Template

- `docs/reports/real-accountant-session/invite-send-receipt.template.json`

## Required Edits After Manual Send

- Set manual_send_completed to true only after the invite was actually sent.
- Set sent_at to the actual YYYY-MM-DD send date.
- Keep reviewer_alias public-safe, for example reviewer-001.
- Keep no_raw_identifiers_requested true.
- Keep operator_attestation free of names, emails, customer identifiers, source bodies, credentials, and secrets.

## Apply

Run only after the receipt is filled from an actual manual send:

```powershell
python scripts\real_accountant_apply_invite_receipt.py --receipt docs\reports\real-accountant-session\invite-send-receipt.template.json --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --format text
```

## Verify

Confirm the ledger now routes to the post-invite reviewer response path:

```powershell
python scripts\real_accountant_outreach_transition_verify.py --expected-status sent --format text
```

## Boundaries

- This guide does not send the reviewer invite.
- This guide does not mark actual send evidence.
- Do not fill or apply the receipt until the invite was actually sent.
- Use the receipt-apply command instead of directly editing the outreach ledger.

## Machine Result

```json
{
  "title": "Real Accountant Filled Receipt Guide",
  "template_path": "docs/reports/real-accountant-session/invite-send-receipt.template.json",
  "report_path": "docs/reports/real-accountant-session/2026-07-05-filled-receipt-guide.md",
  "required_edits_after_manual_send": [
    "Set manual_send_completed to true only after the invite was actually sent.",
    "Set sent_at to the actual YYYY-MM-DD send date.",
    "Keep reviewer_alias public-safe, for example reviewer-001.",
    "Keep no_raw_identifiers_requested true.",
    "Keep operator_attestation free of names, emails, customer identifiers, source bodies, credentials, and secrets."
  ],
  "apply_command": "python scripts\\real_accountant_apply_invite_receipt.py --receipt docs\\reports\\real-accountant-session\\invite-send-receipt.template.json --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --format text",
  "verify_command": "python scripts\\real_accountant_outreach_transition_verify.py --expected-status sent --format text",
  "boundaries": [
    "This guide does not send the reviewer invite.",
    "This guide does not mark actual send evidence.",
    "Do not fill or apply the receipt until the invite was actually sent.",
    "Use the receipt-apply command instead of directly editing the outreach ledger."
  ],
  "next_action": "send_reviewer_invite_then_fill_receipt_apply_and_verify"
}
```
