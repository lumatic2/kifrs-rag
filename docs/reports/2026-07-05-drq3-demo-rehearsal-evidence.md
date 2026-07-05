# DRQ3 Rehearsal Evidence Capture

> Scope: public-safe local rehearsal evidence fixture.

## 한 줄 결론

Captured rehearsal run `drq3-local-public-safe-rehearsal-001` with 8 stage results, timing thresholds, and freshness metadata.

## Stage Results

| Stage | Target | Elapsed | Variance | Threshold | Status | Generated At | Finding | Recovery |
|---|---:|---:|---:|---:|---|---|---|---|
| position | 60 | 45 | -15 | 0 | pass | 2026-07-06T00:00:00+09:00 | none | rerun stage command and inspect the expected report path |
| storyboard | 90 | 70 | -20 | 0 | pass | 2026-07-06T00:00:00+09:00 | none | rerun stage command and inspect the expected report path |
| scenario-contract | 90 | 80 | -10 | 0 | pass | 2026-07-06T00:00:00+09:00 | none | rerun stage command and inspect the expected report path |
| local-parser-boundary | 90 | 85 | -5 | 0 | pass | 2026-07-06T00:00:00+09:00 | none | rerun stage command and inspect the expected report path |
| source-lane-boundary | 90 | 88 | -2 | 0 | pass | 2026-07-06T00:00:00+09:00 | none | rerun stage command and inspect the expected report path |
| workflow-depth | 90 | 86 | -4 | 0 | pass | 2026-07-06T00:00:00+09:00 | none | rerun stage command and inspect the expected report path |
| retriever-decision | 90 | 104 | 14 | 15 | pass | 2026-07-06T00:00:00+09:00 | none | rerun stage command and inspect the expected report path |
| operator-surface | 90 | 76 | -14 | 0 | pass | 2026-07-06T00:00:00+09:00 | none | rerun stage command and inspect the expected report path |

## Timing Metadata

- total target seconds: 690
- total elapsed seconds: 634
- variance seconds: -56

## Freshness Metadata

- generated at: 2026-07-06T00:00:00+09:00
- max age hours: 24
- all stage outputs have generated at: True
- all stage outputs within max age: True

## Checks

| Check | OK |
|---|---|
| stage_results_present | True |
| all_stages_have_status | True |
| timing_metadata_present | True |
| variance_metadata_present | True |
| threshold_metadata_present | True |
| variance_threshold_applied | True |
| freshness_metadata_present | True |
| stage_outputs_fresh | True |
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
      "variance_seconds": -15,
      "timing_variance_threshold_seconds": 0,
      "status": "pass",
      "finding": "none",
      "generated_at": "2026-07-06T00:00:00+09:00",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "storyboard",
      "target_seconds": 90,
      "elapsed_seconds": 70,
      "variance_seconds": -20,
      "timing_variance_threshold_seconds": 0,
      "status": "pass",
      "finding": "none",
      "generated_at": "2026-07-06T00:00:00+09:00",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "scenario-contract",
      "target_seconds": 90,
      "elapsed_seconds": 80,
      "variance_seconds": -10,
      "timing_variance_threshold_seconds": 0,
      "status": "pass",
      "finding": "none",
      "generated_at": "2026-07-06T00:00:00+09:00",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "local-parser-boundary",
      "target_seconds": 90,
      "elapsed_seconds": 85,
      "variance_seconds": -5,
      "timing_variance_threshold_seconds": 0,
      "status": "pass",
      "finding": "none",
      "generated_at": "2026-07-06T00:00:00+09:00",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "source-lane-boundary",
      "target_seconds": 90,
      "elapsed_seconds": 88,
      "variance_seconds": -2,
      "timing_variance_threshold_seconds": 0,
      "status": "pass",
      "finding": "none",
      "generated_at": "2026-07-06T00:00:00+09:00",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "workflow-depth",
      "target_seconds": 90,
      "elapsed_seconds": 86,
      "variance_seconds": -4,
      "timing_variance_threshold_seconds": 0,
      "status": "pass",
      "finding": "none",
      "generated_at": "2026-07-06T00:00:00+09:00",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "retriever-decision",
      "target_seconds": 90,
      "elapsed_seconds": 104,
      "variance_seconds": 14,
      "timing_variance_threshold_seconds": 15,
      "status": "pass",
      "finding": "none",
      "generated_at": "2026-07-06T00:00:00+09:00",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "operator-surface",
      "target_seconds": 90,
      "elapsed_seconds": 76,
      "variance_seconds": -14,
      "timing_variance_threshold_seconds": 0,
      "status": "pass",
      "finding": "none",
      "generated_at": "2026-07-06T00:00:00+09:00",
      "recovery_route": "rerun stage command and inspect the expected report path"
    }
  ],
  "timing": {
    "total_target_seconds": 690,
    "total_elapsed_seconds": 634,
    "variance_seconds": -56
  },
  "freshness": {
    "generated_at": "2026-07-06T00:00:00+09:00",
    "max_age_hours": 24,
    "all_stage_outputs_have_generated_at": true,
    "all_stage_outputs_within_max_age": true,
    "stale_outputs": []
  },
  "checks": {
    "stage_results_present": true,
    "all_stages_have_status": true,
    "timing_metadata_present": true,
    "variance_metadata_present": true,
    "threshold_metadata_present": true,
    "variance_threshold_applied": true,
    "freshness_metadata_present": true,
    "stage_outputs_fresh": true,
    "no_private_participant_data": true,
    "next_milestone_named": true
  },
  "errors": [],
  "next_leaf": "DRQ4_demo_improvement_backlog",
  "report_path": "docs/reports/2026-07-05-drq3-demo-rehearsal-evidence.md"
}
```
