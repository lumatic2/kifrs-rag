# DRQ1 Demo Rehearsal Script And Timing Gate

> Scope: timed local rehearsal script for the public-safe demo packet.

## 한 줄 결론

The demo rehearsal now has 8 stages and a 11.5-minute target budget with explicit expected outputs.

## Rehearsal Stages

| Order | Stage | Command | Expected Output | Target Seconds | Recovery |
|---:|---|---|---|---:|---|
| 0 | `position` | `python scripts\accounting_intelligence_progress_map.py --format text --write` | `docs/reports/2026-07-05-accounting-intelligence-progress-map.md` | 60 | rerun stage command and inspect the expected report path |
| 1 | `storyboard` | `python scripts\e2e_demo_asset_inventory.py --format text --write` | `docs/reports/2026-07-05-e2e1-demo-asset-inventory.md` | 90 | rerun stage command and inspect the expected report path |
| 2 | `scenario-contract` | `python scripts\e2e_scenario_contract.py --format text --write` | `docs/reports/2026-07-05-e2e2-scenario-contract.md` | 90 | rerun stage command and inspect the expected report path |
| 3 | `local-parser-boundary` | `python scripts\real_local_parser_prototype_close_gate.py --format text` | `docs/reports/2026-07-05-real-local-parser-prototype-close-report.md` | 90 | rerun stage command and inspect the expected report path |
| 4 | `source-lane-boundary` | `python scripts\external_source_connector_body_close_gate.py --format text` | `docs/reports/2026-07-05-external-source-body-connector-expansion-close-report.md` | 90 | rerun stage command and inspect the expected report path |
| 5 | `workflow-depth` | `python scripts\workflow_coverage_depth_close_gate.py --format text` | `docs/reports/2026-07-05-workflow-coverage-depth-expansion-close-report.md` | 90 | rerun stage command and inspect the expected report path |
| 6 | `retriever-decision` | `python scripts\runtime_retriever_promotion_close_gate.py --format text` | `docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md` | 90 | rerun stage command and inspect the expected report path |
| 7 | `operator-surface` | `python scripts\operator_experience_close_gate.py --format text` | `docs/reports/2026-07-05-operator-experience-hardening-close-report.md` | 90 | rerun stage command and inspect the expected report path |

## Timing Gate

- total budget seconds: 690
- total budget minutes: 11.5

## Checks

| Check | OK |
|---|---|
| stages_present | True |
| all_stages_have_command | True |
| all_stages_have_expected_output | True |
| timing_budget_present | True |
| public_safe_outputs_only | True |
| next_milestone_named | True |

## Errors

- none

## Next Leaf

- `DRQ2_demo_run_quality_checklist`

## Machine Result

```json
{
  "title": "DRQ1 Demo Rehearsal Script And Timing Gate",
  "ok": true,
  "horizon": "demo-rehearsal-quality-loop",
  "completed_milestone": "DRQ1",
  "total_budget_seconds": 690,
  "total_budget_minutes": 11.5,
  "stages": [
    {
      "order": 0,
      "stage_id": "position",
      "operator_command": "python scripts\\accounting_intelligence_progress_map.py --format text --write",
      "expected_output": "docs/reports/2026-07-05-accounting-intelligence-progress-map.md",
      "target_seconds": 60,
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "order": 1,
      "stage_id": "storyboard",
      "operator_command": "python scripts\\e2e_demo_asset_inventory.py --format text --write",
      "expected_output": "docs/reports/2026-07-05-e2e1-demo-asset-inventory.md",
      "target_seconds": 90,
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "order": 2,
      "stage_id": "scenario-contract",
      "operator_command": "python scripts\\e2e_scenario_contract.py --format text --write",
      "expected_output": "docs/reports/2026-07-05-e2e2-scenario-contract.md",
      "target_seconds": 90,
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "order": 3,
      "stage_id": "local-parser-boundary",
      "operator_command": "python scripts\\real_local_parser_prototype_close_gate.py --format text",
      "expected_output": "docs/reports/2026-07-05-real-local-parser-prototype-close-report.md",
      "target_seconds": 90,
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "order": 4,
      "stage_id": "source-lane-boundary",
      "operator_command": "python scripts\\external_source_connector_body_close_gate.py --format text",
      "expected_output": "docs/reports/2026-07-05-external-source-body-connector-expansion-close-report.md",
      "target_seconds": 90,
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "order": 5,
      "stage_id": "workflow-depth",
      "operator_command": "python scripts\\workflow_coverage_depth_close_gate.py --format text",
      "expected_output": "docs/reports/2026-07-05-workflow-coverage-depth-expansion-close-report.md",
      "target_seconds": 90,
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "order": 6,
      "stage_id": "retriever-decision",
      "operator_command": "python scripts\\runtime_retriever_promotion_close_gate.py --format text",
      "expected_output": "docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md",
      "target_seconds": 90,
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "order": 7,
      "stage_id": "operator-surface",
      "operator_command": "python scripts\\operator_experience_close_gate.py --format text",
      "expected_output": "docs/reports/2026-07-05-operator-experience-hardening-close-report.md",
      "target_seconds": 90,
      "recovery_route": "rerun stage command and inspect the expected report path"
    }
  ],
  "checks": {
    "stages_present": true,
    "all_stages_have_command": true,
    "all_stages_have_expected_output": true,
    "timing_budget_present": true,
    "public_safe_outputs_only": true,
    "next_milestone_named": true
  },
  "errors": [],
  "next_leaf": "DRQ2_demo_run_quality_checklist",
  "report_path": "docs/reports/2026-07-05-drq1-demo-rehearsal-script.md"
}
```
