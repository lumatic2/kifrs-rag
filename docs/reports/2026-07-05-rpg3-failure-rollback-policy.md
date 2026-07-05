# RPG3 Failure And Rollback Policy

> Scope: RPG3 rollback policy for runtime retriever promotion decisions.

## 한 줄 결론

Promotion remains reversible: if evidence is missing or runtime checks fail, the operator keeps current default or must restore `hybrid` as the default.

## Policy

- current default: `hybrid`
- target retriever: `ifrs1109_classification_hybrid`
- safe fallback: `hybrid`
- promotion gate result carried from RPG2: `defer`
- next gate: `operator_promotion_command`

## States

| State | Trigger | Action |
|---|---|---|
| defer | missing latency/cost, rollback, authorization, or broad runtime evidence | keep current default and continue opt-in evaluation |
| block | recall/citation regression, default guard failure, or missing critical reports | do not expose target retriever as runtime default |
| rollback | post-promotion runtime regression or operator-reported failure | restore hybrid as default and rerun guard/report gates |

## Operator Remediation

- run default retriever guard
- run regression/latency gate
- restore current default mode to hybrid if any promotion check fails
- record defer/block reason in promotion command output

## Forbidden Actions

- manual runtime default edit without close gate
- exposing target retriever in MCP modes before promotion
- treating recall@20 success as sufficient for promotion

## Checks

| Check | OK |
|---|---|
| regression_gate_ok | True |
| safe_fallback_is_current_default | True |
| defer_state_present | True |
| block_state_present | True |
| rollback_state_present | True |
| operator_remediation_present | True |
| forbidden_manual_promotion_present | True |

## Errors

- none

## Machine Result

```json
{
  "title": "RPG3 Failure And Rollback Policy",
  "ok": true,
  "horizon": "runtime-retriever-promotion-gate",
  "completed_milestone": "RPG3",
  "promotion_gate_result": "defer",
  "policy": {
    "current_default": "hybrid",
    "target_retriever": "ifrs1109_classification_hybrid",
    "safe_fallback": "hybrid",
    "states": [
      {
        "state": "defer",
        "trigger": "missing latency/cost, rollback, authorization, or broad runtime evidence",
        "action": "keep current default and continue opt-in evaluation"
      },
      {
        "state": "block",
        "trigger": "recall/citation regression, default guard failure, or missing critical reports",
        "action": "do not expose target retriever as runtime default"
      },
      {
        "state": "rollback",
        "trigger": "post-promotion runtime regression or operator-reported failure",
        "action": "restore hybrid as default and rerun guard/report gates"
      }
    ],
    "operator_remediation": [
      "run default retriever guard",
      "run regression/latency gate",
      "restore current default mode to hybrid if any promotion check fails",
      "record defer/block reason in promotion command output"
    ],
    "forbidden_actions": [
      "manual runtime default edit without close gate",
      "exposing target retriever in MCP modes before promotion",
      "treating recall@20 success as sufficient for promotion"
    ]
  },
  "checks": {
    "regression_gate_ok": true,
    "safe_fallback_is_current_default": true,
    "defer_state_present": true,
    "block_state_present": true,
    "rollback_state_present": true,
    "operator_remediation_present": true,
    "forbidden_manual_promotion_present": true
  },
  "errors": [],
  "next_gate": "operator_promotion_command",
  "report_path": "docs/reports/2026-07-05-rpg3-failure-rollback-policy.md"
}
```
