# Runtime Retriever Promotion Gate Close Report

> Scope: RPG5 close gate for runtime retriever promotion.

## 한 줄 결론

Runtime retriever promotion closes as `defer`: the opt-in repair retriever stays available for evaluation, while runtime default remains `hybrid` until latency/cost evidence exists.

## Close Result

- close status: `closed`
- close result: `defer`
- reason: promotion remains deferred because latency/cost evidence is missing and current default guard keeps the repair retriever opt-in
- target retriever: `ifrs1109_classification_hybrid`
- current default: `hybrid`
- next horizon: `operator-experience-hardening`

## Checks

| Check | OK |
|---|---|
| rpg1_inventory_ok | True |
| rpg2_gate_ok | True |
| rpg3_policy_ok | True |
| rpg4_command_ok | True |
| close_result_explicit | True |
| rollback_evidence_present | True |
| operator_command_dry_run | True |
| default_not_changed | True |
| reports_parseable | True |
| all_required_reports_present | True |

## Required Reports

| Report | Path | Exists |
|---|---|---|
| rpg1_evidence_inventory | `docs/reports/2026-07-05-rpg1-promotion-evidence-inventory.md` | True |
| rpg2_regression_latency | `docs/reports/2026-07-05-rpg2-regression-latency-gate.md` | True |
| rpg3_rollback_policy | `docs/reports/2026-07-05-rpg3-failure-rollback-policy.md` | True |
| rpg4_operator_command | `docs/reports/2026-07-05-rpg4-operator-promotion-command.md` | True |

## Rollback Summary

- safe fallback: `hybrid`
- target retriever: `ifrs1109_classification_hybrid`
- current default: `hybrid`

## Errors

- none

## Machine Result

```json
{
  "title": "Runtime Retriever Promotion Gate Close Report",
  "ok": true,
  "horizon": "runtime-retriever-promotion-gate",
  "completed_milestone": "RPG5",
  "close_status": "closed",
  "close_result": "defer",
  "reason": "promotion remains deferred because latency/cost evidence is missing and current default guard keeps the repair retriever opt-in",
  "target_retriever": "ifrs1109_classification_hybrid",
  "current_default": "hybrid",
  "checks": {
    "rpg1_inventory_ok": true,
    "rpg2_gate_ok": true,
    "rpg3_policy_ok": true,
    "rpg4_command_ok": true,
    "close_result_explicit": true,
    "rollback_evidence_present": true,
    "operator_command_dry_run": true,
    "default_not_changed": true,
    "reports_parseable": true,
    "all_required_reports_present": true
  },
  "errors": [],
  "reports": {
    "rpg1_evidence_inventory": {
      "path": "docs/reports/2026-07-05-rpg1-promotion-evidence-inventory.md",
      "exists": true
    },
    "rpg2_regression_latency": {
      "path": "docs/reports/2026-07-05-rpg2-regression-latency-gate.md",
      "exists": true
    },
    "rpg3_rollback_policy": {
      "path": "docs/reports/2026-07-05-rpg3-failure-rollback-policy.md",
      "exists": true
    },
    "rpg4_operator_command": {
      "path": "docs/reports/2026-07-05-rpg4-operator-promotion-command.md",
      "exists": true
    }
  },
  "missing_reports": [],
  "rollback": {
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
  "next_horizon": "operator-experience-hardening",
  "report_path": "docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md"
}
```
