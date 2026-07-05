# Accounting Intelligence Decision Queue

> Scope: user-owned decisions that unblock the Accounting Intelligence Expansion objective.

## 한 줄 결론

No user-owned decision is currently required by the tracked gates.

## Summary

- ok: True
- mode: cached_reports
- decisions: 4
- open decisions: 4
- operator action required: 0
- recommended next decision: None

## Decision Queue

| Priority | Decision | Status | What User Decides | Unblocks |
|---:|---|---|---|---|
| 1 | `external_accountant_feedback` | parked_by_user_request | No active decision. External accountant outreach is excluded until the user explicitly asks for it. | future external validation only; not part of the current active plan |
| 2 | `approve_external_body_authorization_record` | parked_until_explicit_authorization | No active decision. Fill a source-specific authorization record only when live local-private body ingestion becomes the chosen horizon. | external source body connector implementation |
| 3 | `approve_local_private_parser_adapter` | waiting_on_eval_evidence | Whether to authorize real private-file parser work after stronger internal evaluation evidence exists. | real local file upload/OCR/parser/deletion automation |
| 4 | `approve_default_retriever_promotion` | waiting_on_eval_evidence | Whether to promote the opt-in repair retriever to default after stronger internal evaluation evidence exists. | default retriever change from hybrid to ifrs1109_classification_hybrid stack |

## Details

### 1. Park external accountant feedback loop

- status: parked_by_user_request
- gate ok: True
- operator action required: False
- user decision: No active decision. External accountant outreach is excluded until the user explicitly asks for it.
- unblocks: future external validation only; not part of the current active plan
- current blocker: parked by user request
- next command: none
- receipt command: none
- after command: none
- verify command: none
- evidence: `ROADMAP.md`

### 2. Approve source-specific external body authorization record

- status: parked_until_explicit_authorization
- gate ok: True
- operator action required: False
- user decision: No active decision. Fill a source-specific authorization record only when live local-private body ingestion becomes the chosen horizon.
- unblocks: external source body connector implementation
- current blocker: authorized_by is required
- next command: Fill `docs/reports/external-source-body-authorization-record.template.json`, then run the external body authorization gate with that record.
- receipt command: none
- after command: none
- verify command: Run the external body authorization gate with the approved record path.
- evidence: `docs/reports/external-source-body-authorization-record.template.json`

### 3. Approve real local-private parser adapter

- status: waiting_on_eval_evidence
- gate ok: True
- operator action required: False
- user decision: Whether to authorize real private-file parser work after stronger internal evaluation evidence exists.
- unblocks: real local file upload/OCR/parser/deletion automation
- current blocker: stronger internal evaluation evidence and explicit authorization are required
- next command: python scripts\client_private_local_parser_real_adapter_decision_gate.py --format text
- receipt command: none
- after command: none
- verify command: python scripts\client_private_local_parser_real_adapter_decision_gate.py --format text
- evidence: `docs\reports\2026-07-05-lprd1-local-parser-real-adapter-decision-gate.md`

### 4. Approve opt-in retriever default promotion

- status: waiting_on_eval_evidence
- gate ok: True
- operator action required: False
- user decision: Whether to promote the opt-in repair retriever to default after stronger internal evaluation evidence exists.
- unblocks: default retriever change from hybrid to ifrs1109_classification_hybrid stack
- current blocker: stronger internal evaluation evidence and explicit authorization are required
- next command: python scripts\opt_in_retriever_promotion_decision_gate.py --format text
- receipt command: none
- after command: none
- verify command: python scripts\opt_in_retriever_promotion_decision_gate.py --format text
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
  "operator_action_required_count": 0,
  "recommended_next_decision": null,
  "decisions": [
    {
      "id": "external_accountant_feedback",
      "title": "Park external accountant feedback loop",
      "priority": 1,
      "status": "parked_by_user_request",
      "gate_ok": true,
      "errors": [],
      "operator_action_required": false,
      "user_decision": "No active decision. External accountant outreach is excluded until the user explicitly asks for it.",
      "unblocks": "future external validation only; not part of the current active plan",
      "current_blocker": "parked by user request",
      "next_command": "none",
      "receipt_command": "none",
      "after_command": "none",
      "verify_command": "none",
      "evidence": "ROADMAP.md"
    },
    {
      "id": "approve_external_body_authorization_record",
      "title": "Approve source-specific external body authorization record",
      "priority": 2,
      "status": "parked_until_explicit_authorization",
      "gate_ok": true,
      "errors": [],
      "operator_action_required": false,
      "user_decision": "No active decision. Fill a source-specific authorization record only when live local-private body ingestion becomes the chosen horizon.",
      "unblocks": "external source body connector implementation",
      "current_blocker": "authorized_by is required",
      "next_command": "Fill `docs/reports/external-source-body-authorization-record.template.json`, then run the external body authorization gate with that record.",
      "receipt_command": "none",
      "after_command": "none",
      "verify_command": "Run the external body authorization gate with the approved record path.",
      "evidence": "docs/reports/external-source-body-authorization-record.template.json"
    },
    {
      "id": "approve_local_private_parser_adapter",
      "title": "Approve real local-private parser adapter",
      "priority": 3,
      "status": "waiting_on_eval_evidence",
      "gate_ok": true,
      "errors": [],
      "operator_action_required": false,
      "user_decision": "Whether to authorize real private-file parser work after stronger internal evaluation evidence exists.",
      "unblocks": "real local file upload/OCR/parser/deletion automation",
      "current_blocker": "stronger internal evaluation evidence and explicit authorization are required",
      "next_command": "python scripts\\client_private_local_parser_real_adapter_decision_gate.py --format text",
      "receipt_command": "none",
      "after_command": "none",
      "verify_command": "python scripts\\client_private_local_parser_real_adapter_decision_gate.py --format text",
      "evidence": "docs\\reports\\2026-07-05-lprd1-local-parser-real-adapter-decision-gate.md"
    },
    {
      "id": "approve_default_retriever_promotion",
      "title": "Approve opt-in retriever default promotion",
      "priority": 4,
      "status": "waiting_on_eval_evidence",
      "gate_ok": true,
      "errors": [],
      "operator_action_required": false,
      "user_decision": "Whether to promote the opt-in repair retriever to default after stronger internal evaluation evidence exists.",
      "unblocks": "default retriever change from hybrid to ifrs1109_classification_hybrid stack",
      "current_blocker": "stronger internal evaluation evidence and explicit authorization are required",
      "next_command": "python scripts\\opt_in_retriever_promotion_decision_gate.py --format text",
      "receipt_command": "none",
      "after_command": "none",
      "verify_command": "python scripts\\opt_in_retriever_promotion_decision_gate.py --format text",
      "evidence": "docs\\reports\\2026-07-05-orpd1-opt-in-retriever-promotion-decision-gate.md"
    }
  ],
  "report_path": "docs/reports/2026-07-05-accounting-intelligence-decision-queue.md"
}
```
