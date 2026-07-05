# Accounting Intelligence Decision Queue

> Scope: user-owned decisions that unblock the Accounting Intelligence Expansion objective.

## 한 줄 결론

The next useful user-owned decision is sending the real accountant reviewer invite; other implementation approvals should wait for actual feedback evidence.

## Summary

- ok: True
- mode: cached_reports
- decisions: 4
- open decisions: 4
- operator action required: 2
- recommended next decision: send_reviewer_invite

## Decision Queue

| Priority | Decision | Status | What User Decides | Unblocks |
|---:|---|---|---|---|
| 1 | `send_reviewer_invite` | needs_user_action | Which reviewer should receive the invite, and should the invite be sent now? | RS2 actual accountant session, RS3 actual notes capture, RS4 close gate |
| 2 | `approve_external_body_authorization_record` | needs_user_action | Whether to fill a source-specific authorization record for live local-private body ingestion. | external source body connector implementation |
| 3 | `approve_local_private_parser_adapter` | waiting_on_accountant_evidence | Whether to authorize real private-file parser work after actual accountant evidence exists. | real local file upload/OCR/parser/deletion automation |
| 4 | `approve_default_retriever_promotion` | waiting_on_accountant_evidence | Whether to promote the opt-in repair retriever to default after actual accountant evidence exists. | default retriever change from hybrid to ifrs1109_classification_hybrid stack |

## Details

### 1. Send real accountant reviewer invite

- status: needs_user_action
- gate ok: True
- operator action required: True
- user decision: Which reviewer should receive the invite, and should the invite be sent now?
- unblocks: RS2 actual accountant session, RS3 actual notes capture, RS4 close gate
- current blocker: reviewer invite has not been sent
- next command: python scripts\real_accountant_invite_packet.py
- evidence: `docs/reports/real-accountant-session/2026-07-05-operator-execution-brief.md`

### 2. Approve source-specific external body authorization record

- status: needs_user_action
- gate ok: True
- operator action required: True
- user decision: Whether to fill a source-specific authorization record for live local-private body ingestion.
- unblocks: external source body connector implementation
- current blocker: authorized_by is required
- next command: Fill `docs/reports/external-source-body-authorization-record.template.json`, then run the external body authorization gate with that record.
- evidence: `docs/reports/external-source-body-authorization-record.template.json`

### 3. Approve real local-private parser adapter

- status: waiting_on_accountant_evidence
- gate ok: True
- operator action required: False
- user decision: Whether to authorize real private-file parser work after actual accountant evidence exists.
- unblocks: real local file upload/OCR/parser/deletion automation
- current blocker: actual accountant feedback evidence is required before real private-file parser work
- next command: python scripts\client_private_local_parser_real_adapter_decision_gate.py --format text
- evidence: `docs\reports\2026-07-05-lprd1-local-parser-real-adapter-decision-gate.md`

### 4. Approve opt-in retriever default promotion

- status: waiting_on_accountant_evidence
- gate ok: True
- operator action required: False
- user decision: Whether to promote the opt-in repair retriever to default after actual accountant evidence exists.
- unblocks: default retriever change from hybrid to ifrs1109_classification_hybrid stack
- current blocker: actual accountant feedback evidence is required before default retriever promotion
- next command: python scripts\opt_in_retriever_promotion_decision_gate.py --format text
- evidence: `docs\reports\2026-07-05-orpd1-opt-in-retriever-promotion-decision-gate.md`

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "title": "Accounting Intelligence Decision Queue",
  "mode": "cached_reports",
  "decision_count": 4,
  "open_decision_count": 4,
  "operator_action_required_count": 2,
  "recommended_next_decision": "send_reviewer_invite",
  "decisions": [
    {
      "id": "send_reviewer_invite",
      "title": "Send real accountant reviewer invite",
      "priority": 1,
      "status": "needs_user_action",
      "gate_ok": true,
      "errors": [],
      "operator_action_required": true,
      "user_decision": "Which reviewer should receive the invite, and should the invite be sent now?",
      "unblocks": "RS2 actual accountant session, RS3 actual notes capture, RS4 close gate",
      "current_blocker": "reviewer invite has not been sent",
      "next_command": "python scripts\\real_accountant_invite_packet.py",
      "evidence": "docs/reports/real-accountant-session/2026-07-05-operator-execution-brief.md"
    },
    {
      "id": "approve_external_body_authorization_record",
      "title": "Approve source-specific external body authorization record",
      "priority": 2,
      "status": "needs_user_action",
      "gate_ok": true,
      "errors": [],
      "operator_action_required": true,
      "user_decision": "Whether to fill a source-specific authorization record for live local-private body ingestion.",
      "unblocks": "external source body connector implementation",
      "current_blocker": "authorized_by is required",
      "next_command": "Fill `docs/reports/external-source-body-authorization-record.template.json`, then run the external body authorization gate with that record.",
      "evidence": "docs/reports/external-source-body-authorization-record.template.json"
    },
    {
      "id": "approve_local_private_parser_adapter",
      "title": "Approve real local-private parser adapter",
      "priority": 3,
      "status": "waiting_on_accountant_evidence",
      "gate_ok": true,
      "errors": [],
      "operator_action_required": false,
      "user_decision": "Whether to authorize real private-file parser work after actual accountant evidence exists.",
      "unblocks": "real local file upload/OCR/parser/deletion automation",
      "current_blocker": "actual accountant feedback evidence is required before real private-file parser work",
      "next_command": "python scripts\\client_private_local_parser_real_adapter_decision_gate.py --format text",
      "evidence": "docs\\reports\\2026-07-05-lprd1-local-parser-real-adapter-decision-gate.md"
    },
    {
      "id": "approve_default_retriever_promotion",
      "title": "Approve opt-in retriever default promotion",
      "priority": 4,
      "status": "waiting_on_accountant_evidence",
      "gate_ok": true,
      "errors": [],
      "operator_action_required": false,
      "user_decision": "Whether to promote the opt-in repair retriever to default after actual accountant evidence exists.",
      "unblocks": "default retriever change from hybrid to ifrs1109_classification_hybrid stack",
      "current_blocker": "actual accountant feedback evidence is required before default retriever promotion",
      "next_command": "python scripts\\opt_in_retriever_promotion_decision_gate.py --format text",
      "evidence": "docs\\reports\\2026-07-05-orpd1-opt-in-retriever-promotion-decision-gate.md"
    }
  ],
  "report_path": "docs/reports/2026-07-05-accounting-intelligence-decision-queue.md"
}
```
