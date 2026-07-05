# ORPD1 Opt-In Retriever Promotion Decision Gate

> Scope: stop/go gate before changing the default retriever from `hybrid` to the final opt-in repair stack.

## 한 줄 결론

`ifrs1109_classification_hybrid` remains opt-in. Retrieval metrics pass, but actual accountant feedback evidence and explicit authorization are still required before changing the default retriever.

## Decision

- Decision: defer
- Promote to default: False
- Target retriever: `ifrs1109_classification_hybrid`
- Demo validation ok: True
- Actual accountant evidence: False
- Explicit authorization: False

## Blockers

- actual accountant feedback evidence is required before default retriever promotion
- explicit user authorization is required before changing the default retriever

## Retrieval Evidence

- Demo validation report: `docs\reports\2026-07-05-odv1-opt-in-retriever-demo-validation.md`
- Target recall@20: 1.000
- Required-citation absent count: 0
- Target misses: 0
- Current default promotion state: deferred

## Real Accountant Session Snapshot

- Session mode: ready_to_schedule
- Outreach counts: {'completed': 0, 'declined': 0, 'not_sent': 1, 'responded': 0, 'scheduled': 0, 'sent': 0}
- Close ready: False
- Next action: Send reviewer invite and update outreach ledger to sent.

## Boundary

- This gate does not change runtime defaults.
- The current default retriever remains unchanged unless this gate returns `promote` and a separate implementation changes the default.
- Retrieval-only quality is not answer-quality proof and does not replace accountant review.

## Next Leaf

real-accountant-session RS2/RS3 evidence capture, then explicit authorization before default retriever change

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "decision": {
    "decision_id": "orpd1-opt-in-retriever-promotion-decision-gate",
    "decision": "defer",
    "promote_to_default": false,
    "target_retriever": "ifrs1109_classification_hybrid",
    "demo_validation_ok": true,
    "actual_accountant_evidence": false,
    "explicit_authorization": false,
    "blockers": [
      "actual accountant feedback evidence is required before default retriever promotion",
      "explicit user authorization is required before changing the default retriever"
    ],
    "next_leaf": "real-accountant-session RS2/RS3 evidence capture, then explicit authorization before default retriever change"
  },
  "demo_validation": {
    "ok": true,
    "target_retriever": "ifrs1109_classification_hybrid",
    "target_recall20": 1.0,
    "target_buckets": {
      "hit@5": 47,
      "hit@10": 18,
      "hit@20": 17,
      "beyond@20": 0,
      "absent": 0
    },
    "target_misses": [],
    "default_promotion": "deferred",
    "report_path": "docs\\reports\\2026-07-05-odv1-opt-in-retriever-demo-validation.md"
  },
  "real_accountant_session": {
    "session_mode": "ready_to_schedule",
    "outreach_counts": {
      "completed": 0,
      "declined": 0,
      "not_sent": 1,
      "responded": 0,
      "scheduled": 0,
      "sent": 0
    },
    "close_ready": false,
    "next_action": "Send reviewer invite and update outreach ledger to sent.",
    "blocked_by": [
      "reviewer invite has not been sent",
      "no completed reviewer session in outreach ledger",
      "session manifest is ready_to_schedule, not actual_feedback",
      "session_manifest: mode must be actual_feedback, got ready_to_schedule",
      "session_manifest: missing notes_file",
      "session_manifest: missing queue_jsonl",
      "outreach: at least one completed reviewer session is required"
    ]
  },
  "report_path": "docs\\reports\\2026-07-05-orpd1-opt-in-retriever-promotion-decision-gate.md",
  "next_leaf": "real-accountant-session RS2/RS3 evidence capture, then explicit authorization before default retriever change"
}
```
