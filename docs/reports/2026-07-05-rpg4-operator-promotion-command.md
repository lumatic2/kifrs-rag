# RPG4 Operator Promotion Command

> Scope: dry-run operator surface for retriever promotion status.

## 한 줄 결론

The operator command reports `defer`, shows required evidence, and does not mutate runtime defaults.

## Command Output

- command: `retriever-promotion status --dry-run`
- mutates runtime: False
- decision: `defer`
- target retriever: `ifrs1109_classification_hybrid`
- current default: `hybrid`
- safe fallback: `hybrid`
- next gate: `promotion_gate_close_report`

## Required Before Promote

- latency/cost measurement
- close-gate promote decision
- operator-reviewed rollback path
- explicit runtime implementation review

## Operator Actions

- keep current default hybrid
- run regression/latency gate after latency evidence exists
- use rollback policy if any promotion experiment fails
- do not expose target retriever in MCP modes before close gate

## Checks

| Check | OK |
|---|---|
| rollback_policy_ok | True |
| dry_run_only | True |
| decision_visible | True |
| required_evidence_visible | True |
| rollback_path_visible | True |
| target_retriever_visible | True |

## Errors

- none

## Machine Result

```json
{
  "title": "RPG4 Operator Promotion Command",
  "ok": true,
  "horizon": "runtime-retriever-promotion-gate",
  "completed_milestone": "RPG4",
  "command_output": {
    "command": "retriever-promotion status --dry-run",
    "mutates_runtime": false,
    "decision": "defer",
    "target_retriever": "ifrs1109_classification_hybrid",
    "current_default": "hybrid",
    "safe_fallback": "hybrid",
    "required_before_promote": [
      "latency/cost measurement",
      "close-gate promote decision",
      "operator-reviewed rollback path",
      "explicit runtime implementation review"
    ],
    "operator_actions": [
      "keep current default hybrid",
      "run regression/latency gate after latency evidence exists",
      "use rollback policy if any promotion experiment fails",
      "do not expose target retriever in MCP modes before close gate"
    ]
  },
  "checks": {
    "rollback_policy_ok": true,
    "dry_run_only": true,
    "decision_visible": true,
    "required_evidence_visible": true,
    "rollback_path_visible": true,
    "target_retriever_visible": true
  },
  "errors": [],
  "next_gate": "promotion_gate_close_report",
  "report_path": "docs/reports/2026-07-05-rpg4-operator-promotion-command.md"
}
```
