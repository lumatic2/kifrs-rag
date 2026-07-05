# ESB4 Connector Leak And Policy Gate

> Scope: public-safe leak and policy gate for ESB1 to ESB3 reports.

## 한 줄 결론

ESB connector reports pass the public-safe leak gate; blocked marker contents are counted but not rendered.

## Scanned Reports

- `docs/reports/2026-07-05-esb1-source-body-connector-selection.md`
- `docs/reports/2026-07-05-esb2-source-body-fixture-contract.md`
- `docs/reports/2026-07-05-esb3-chunking-retrieval-dry-run.md`

## Negative Cases

| Case | Marker Rendered | Real Payload |
|---|---|---|
| synthetic_blocked_marker_case | False | False |
| synthetic_private_payload_case | False | False |
| synthetic_cache_path_case | False | False |

## Policy Requirements

| Requirement | OK |
|---|---|
| live_fetching_blocked | True |
| copied_payload_rendering_blocked | True |
| public_report_marker_list_hidden | True |
| synthetic_negative_cases_only | True |
| scanned_reports_exist | True |

## Leak Scan

- blocked marker count: 7
- hit count: 0

## Checks

| Check | OK |
|---|---|
| live_fetching_blocked | True |
| copied_payload_rendering_blocked | True |
| public_report_marker_list_hidden | True |
| synthetic_negative_cases_only | True |
| scanned_reports_exist | True |
| no_blocked_markers_in_scanned_reports | True |
| next_milestone_named | True |

## Errors

- none

## Next Leaf

- `ESB5_horizon_close_and_workflow_coverage_handoff`

## Machine Result

```json
{
  "title": "ESB4 Connector Leak And Policy Gate",
  "ok": true,
  "horizon": "external-source-body-connector-expansion",
  "completed_milestone": "ESB4",
  "scanned_reports": [
    "docs/reports/2026-07-05-esb1-source-body-connector-selection.md",
    "docs/reports/2026-07-05-esb2-source-body-fixture-contract.md",
    "docs/reports/2026-07-05-esb3-chunking-retrieval-dry-run.md"
  ],
  "blocked_marker_count": 7,
  "hit_count": 0,
  "negative_cases": [
    {
      "case_id": "synthetic_blocked_marker_case",
      "marker_rendered": false,
      "real_payload": false
    },
    {
      "case_id": "synthetic_private_payload_case",
      "marker_rendered": false,
      "real_payload": false
    },
    {
      "case_id": "synthetic_cache_path_case",
      "marker_rendered": false,
      "real_payload": false
    }
  ],
  "policy_requirements": {
    "live_fetching_blocked": true,
    "copied_payload_rendering_blocked": true,
    "public_report_marker_list_hidden": true,
    "synthetic_negative_cases_only": true,
    "scanned_reports_exist": true
  },
  "checks": {
    "live_fetching_blocked": true,
    "copied_payload_rendering_blocked": true,
    "public_report_marker_list_hidden": true,
    "synthetic_negative_cases_only": true,
    "scanned_reports_exist": true,
    "no_blocked_markers_in_scanned_reports": true,
    "next_milestone_named": true
  },
  "errors": [],
  "next_leaf": "ESB5_horizon_close_and_workflow_coverage_handoff",
  "report_path": "docs/reports/2026-07-05-esb4-connector-leak-policy-gate.md"
}
```
