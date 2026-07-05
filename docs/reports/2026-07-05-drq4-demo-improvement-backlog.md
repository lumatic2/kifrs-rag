# DRQ4 Demo Improvement Backlog

> Scope: internal product improvement backlog from demo rehearsal findings.

## 한 줄 결론

Rehearsal findings are converted into prioritized internal fixes; no external dependency is introduced.

## Findings

| Finding | Stage | Severity | Summary |
|---|---|---|---|
| retriever-decision-timing-warning | retriever-decision | medium | timing variance recorded during rehearsal |
| stage-output-freshness-check | all | medium | stage reports can be stale if commands are skipped |
| operator-summary-density | position | low | operator needs a compact current-state summary before demo start |

## Prioritized Backlog

| Item | Finding | Action | Impact | Cost | Score | Dependency |
|---|---|---|---:|---:|---:|---|
| DRQ4-1 | retriever-decision-timing-warning | Add retriever-decision timing note and expected variance threshold to the next checklist. | 4 | 1 | 3 | internal |
| DRQ4-2 | stage-output-freshness-check | Add generated-at freshness metadata check to rehearsal evidence capture. | 5 | 2 | 3 | internal |
| DRQ4-3 | operator-summary-density | Add one-screen operator summary to the progress map report. | 3 | 2 | 1 | internal |

## Checks

| Check | OK |
|---|---|
| findings_present | True |
| backlog_items_present | True |
| all_items_internal | True |
| all_items_prioritized | True |
| next_milestone_named | True |

## Errors

- none

## Next Leaf

- `DRQ5_horizon_close_and_objective_gap_audit`

## Machine Result

```json
{
  "title": "DRQ4 Demo Improvement Backlog",
  "ok": true,
  "horizon": "demo-rehearsal-quality-loop",
  "completed_milestone": "DRQ4",
  "findings": [
    {
      "finding_id": "retriever-decision-timing-warning",
      "source_stage": "retriever-decision",
      "finding": "timing variance recorded during rehearsal",
      "severity": "medium"
    },
    {
      "finding_id": "stage-output-freshness-check",
      "source_stage": "all",
      "finding": "stage reports can be stale if commands are skipped",
      "severity": "medium"
    },
    {
      "finding_id": "operator-summary-density",
      "source_stage": "position",
      "finding": "operator needs a compact current-state summary before demo start",
      "severity": "low"
    }
  ],
  "backlog": [
    {
      "item_id": "DRQ4-1",
      "finding_id": "retriever-decision-timing-warning",
      "source_stage": "retriever-decision",
      "action": "Add retriever-decision timing note and expected variance threshold to the next checklist.",
      "product_impact": 4,
      "implementation_cost": 1,
      "priority_score": 3,
      "dependency": "internal"
    },
    {
      "item_id": "DRQ4-2",
      "finding_id": "stage-output-freshness-check",
      "source_stage": "all",
      "action": "Add generated-at freshness metadata check to rehearsal evidence capture.",
      "product_impact": 5,
      "implementation_cost": 2,
      "priority_score": 3,
      "dependency": "internal"
    },
    {
      "item_id": "DRQ4-3",
      "finding_id": "operator-summary-density",
      "source_stage": "position",
      "action": "Add one-screen operator summary to the progress map report.",
      "product_impact": 3,
      "implementation_cost": 2,
      "priority_score": 1,
      "dependency": "internal"
    }
  ],
  "checks": {
    "findings_present": true,
    "backlog_items_present": true,
    "all_items_internal": true,
    "all_items_prioritized": true,
    "next_milestone_named": true
  },
  "errors": [],
  "next_leaf": "DRQ5_horizon_close_and_objective_gap_audit",
  "report_path": "docs/reports/2026-07-05-drq4-demo-improvement-backlog.md"
}
```
