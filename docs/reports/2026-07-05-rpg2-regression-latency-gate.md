# RPG2 Regression And Latency Gate

> Scope: RPG2 regression and runtime-cost precondition gate.

## 한 줄 결론

Recall and citation evidence are present, but promotion remains `defer` because latency/cost measurement and rollback policy are not yet present.

## Gate Result

- target retriever: `ifrs1109_classification_hybrid`
- current default: `hybrid`
- promotion gate result: `defer`
- next gate: `failure_and_rollback_policy`

## Minimum Requirements

- inventory is valid
- recall support exists
- citation miss support exists
- default guard blocks accidental promotion
- latency/cost measurement exists
- rollback policy exists

## Checks

| Check | OK |
|---|---|
| inventory_ok | True |
| recall_support_present | True |
| citation_miss_support_present | True |
| default_guard_blocks_accidental_promotion | True |
| latency_cost_measured | False |
| rollback_policy_present | False |

## Blocking Reasons

- latency_cost_measured
- rollback_policy_present

## Errors

- none

## Machine Result

```json
{
  "title": "RPG2 Regression And Latency Gate",
  "ok": true,
  "horizon": "runtime-retriever-promotion-gate",
  "completed_milestone": "RPG2",
  "target_retriever": "ifrs1109_classification_hybrid",
  "current_default": "hybrid",
  "promotion_gate_result": "defer",
  "checks": {
    "inventory_ok": true,
    "recall_support_present": true,
    "citation_miss_support_present": true,
    "default_guard_blocks_accidental_promotion": true,
    "latency_cost_measured": false,
    "rollback_policy_present": false
  },
  "blocking_reasons": [
    "latency_cost_measured",
    "rollback_policy_present"
  ],
  "errors": [],
  "minimum_requirements": [
    "inventory is valid",
    "recall support exists",
    "citation miss support exists",
    "default guard blocks accidental promotion",
    "latency/cost measurement exists",
    "rollback policy exists"
  ],
  "next_gate": "failure_and_rollback_policy",
  "report_path": "docs/reports/2026-07-05-rpg2-regression-latency-gate.md"
}
```
