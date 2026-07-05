# DRQ3 Rehearsal Evidence Capture

> Scope: public-safe local rehearsal evidence fixture.

## 한 줄 결론

Captured rehearsal run `drq3-local-public-safe-rehearsal-001` with 8 stage results; one timing warning is recorded for improvement backlog input.

## Stage Results

| Stage | Target | Elapsed | Status | Finding | Recovery |
|---|---:|---:|---|---|---|
| position | 60 | 45 | pass | none | rerun stage command and inspect the expected report path |
| storyboard | 90 | 70 | pass | none | rerun stage command and inspect the expected report path |
| scenario-contract | 90 | 80 | pass | none | rerun stage command and inspect the expected report path |
| local-parser-boundary | 90 | 85 | pass | none | rerun stage command and inspect the expected report path |
| source-lane-boundary | 90 | 88 | pass | none | rerun stage command and inspect the expected report path |
| workflow-depth | 90 | 86 | pass | none | rerun stage command and inspect the expected report path |
| retriever-decision | 90 | 104 | warning | timing variance recorded; recovery route remains available | rerun stage command and inspect the expected report path |
| operator-surface | 90 | 76 | pass | none | rerun stage command and inspect the expected report path |

## Timing Metadata

- total target seconds: 690
- total elapsed seconds: 634
- variance seconds: -56

## Checks

| Check | OK |
|---|---|
| stage_results_present | True |
| all_stages_have_status | True |
| timing_metadata_present | True |
| warnings_recorded | True |
| no_private_participant_data | True |
| next_milestone_named | True |

## Errors

- none

## Next Leaf

- `DRQ4_demo_improvement_backlog`

## Machine Result

```json
{
  "title": "DRQ3 Rehearsal Evidence Capture",
  "ok": true,
  "horizon": "demo-rehearsal-quality-loop",
  "completed_milestone": "DRQ3",
  "run_id": "drq3-local-public-safe-rehearsal-001",
  "stage_results": [
    {
      "stage_id": "position",
      "target_seconds": 60,
      "elapsed_seconds": 45,
      "status": "pass",
      "finding": "none",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "storyboard",
      "target_seconds": 90,
      "elapsed_seconds": 70,
      "status": "pass",
      "finding": "none",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "scenario-contract",
      "target_seconds": 90,
      "elapsed_seconds": 80,
      "status": "pass",
      "finding": "none",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "local-parser-boundary",
      "target_seconds": 90,
      "elapsed_seconds": 85,
      "status": "pass",
      "finding": "none",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "source-lane-boundary",
      "target_seconds": 90,
      "elapsed_seconds": 88,
      "status": "pass",
      "finding": "none",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "workflow-depth",
      "target_seconds": 90,
      "elapsed_seconds": 86,
      "status": "pass",
      "finding": "none",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "retriever-decision",
      "target_seconds": 90,
      "elapsed_seconds": 104,
      "status": "warning",
      "finding": "timing variance recorded; recovery route remains available",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "operator-surface",
      "target_seconds": 90,
      "elapsed_seconds": 76,
      "status": "pass",
      "finding": "none",
      "recovery_route": "rerun stage command and inspect the expected report path"
    }
  ],
  "timing": {
    "total_target_seconds": 690,
    "total_elapsed_seconds": 634,
    "variance_seconds": -56
  },
  "checks": {
    "stage_results_present": true,
    "all_stages_have_status": true,
    "timing_metadata_present": true,
    "warnings_recorded": true,
    "no_private_participant_data": true,
    "next_milestone_named": true
  },
  "errors": [],
  "next_leaf": "DRQ4_demo_improvement_backlog",
  "report_path": "docs/reports/2026-07-05-drq3-demo-rehearsal-evidence.md"
}
```
