# WCD4 Coverage Depth Metric Update

> Scope: update internal workflow coverage depth after WCD3 adapter evidence.

## 한 줄 결론

`audit_disclosure_tie_out` adds one public-safe minimal adapter surface. This is repo evidence coverage, not field validation or final judgment automation.

## Workflow Records

| Workflow | Service Lines | Status | Evidence Depth |
|---|---|---|---:|
| 1109_financial_instrument_review | F-ACC, F-AUD | decision_engine_evidence | 4 |
| 1116_lease_review_pack | F-ACC, F-AUD | review_pack_and_disclosure_evidence | 4 |
| 1037_provisions | F-ACC, F-AUD | conditional_decision_prep_adapter | 3 |
| audit_disclosure_tie_out | F-AUD, F-ACC | minimal_decision_prep_adapter | 3 |

## Metric

- service lines total: 8
- service lines with adapter evidence: 2
- service-line touch rate: 25.00%
- workflow surfaces with adapter evidence: 4
- conditional or better workflows: 4
- new workflow added: `audit_disclosure_tie_out`
- not a field validation rate: True

## Limits

- metric counts repo evidence, not actual firm adoption
- metric does not claim external accountant validation
- metric does not claim final audit or accounting conclusion automation
- metric does not include tax-agent workflows

## Checks

| Check | OK |
|---|---|
| new_workflow_recorded | True |
| service_line_count_bounded | True |
| workflow_count_increased | True |
| not_field_validation_rate | True |
| limits_recorded | True |
| next_milestone_named | True |

## Errors

- none

## Next Leaf

- `WCD5_horizon_close_and_demo_rehearsal_handoff`

## Machine Result

```json
{
  "title": "WCD4 Coverage Depth Metric Update",
  "ok": true,
  "horizon": "workflow-coverage-depth-expansion",
  "completed_milestone": "WCD4",
  "workflow_records": [
    {
      "workflow_id": "1109_financial_instrument_review",
      "service_lines": [
        "F-ACC",
        "F-AUD"
      ],
      "coverage_status": "decision_engine_evidence",
      "evidence_depth": 4
    },
    {
      "workflow_id": "1116_lease_review_pack",
      "service_lines": [
        "F-ACC",
        "F-AUD"
      ],
      "coverage_status": "review_pack_and_disclosure_evidence",
      "evidence_depth": 4
    },
    {
      "workflow_id": "1037_provisions",
      "service_lines": [
        "F-ACC",
        "F-AUD"
      ],
      "coverage_status": "conditional_decision_prep_adapter",
      "evidence_depth": 3
    },
    {
      "workflow_id": "audit_disclosure_tie_out",
      "service_lines": [
        "F-AUD",
        "F-ACC"
      ],
      "coverage_status": "minimal_decision_prep_adapter",
      "evidence_depth": 3
    }
  ],
  "touched_service_lines": [
    "F-ACC",
    "F-AUD"
  ],
  "metric": {
    "service_lines_total": 8,
    "service_lines_with_adapter_evidence": 2,
    "service_line_touch_rate": 0.25,
    "workflow_surfaces_with_adapter_evidence": 4,
    "conditional_or_better_workflows": 4,
    "new_workflow_added": "audit_disclosure_tie_out",
    "not_a_field_validation_rate": true
  },
  "limits": [
    "metric counts repo evidence, not actual firm adoption",
    "metric does not claim external accountant validation",
    "metric does not claim final audit or accounting conclusion automation",
    "metric does not include tax-agent workflows"
  ],
  "checks": {
    "new_workflow_recorded": true,
    "service_line_count_bounded": true,
    "workflow_count_increased": true,
    "not_field_validation_rate": true,
    "limits_recorded": true,
    "next_milestone_named": true
  },
  "errors": [],
  "next_leaf": "WCD5_horizon_close_and_demo_rehearsal_handoff",
  "report_path": "docs/reports/2026-07-05-wcd4-coverage-depth-metric.md"
}
```
