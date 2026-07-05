# DRQ2 Demo Run Quality Checklist

> Scope: pass/fail checklist for each timed demo rehearsal stage.

## 한 줄 결론

Every rehearsal stage has pass checks, a failure note, a recovery route, and a timing check.

## Stage Checks

| Stage | Target Seconds | Variance Threshold | Pass Checks | Failure Note | Recovery |
|---|---:|---:|---|---|---|
| position | 60 | 0 | command_exits_zero_or_existing_report_is_present, expected_output_path_exists, public_safe_boundary_still_visible, timing_within_stage_budget_or_within_variance_threshold | record missing report, timeout, unclear boundary, stale output, or timing variance above threshold before continuing | rerun stage command and inspect the expected report path |
| storyboard | 90 | 0 | command_exits_zero_or_existing_report_is_present, expected_output_path_exists, public_safe_boundary_still_visible, timing_within_stage_budget_or_within_variance_threshold | record missing report, timeout, unclear boundary, stale output, or timing variance above threshold before continuing | rerun stage command and inspect the expected report path |
| scenario-contract | 90 | 0 | command_exits_zero_or_existing_report_is_present, expected_output_path_exists, public_safe_boundary_still_visible, timing_within_stage_budget_or_within_variance_threshold | record missing report, timeout, unclear boundary, stale output, or timing variance above threshold before continuing | rerun stage command and inspect the expected report path |
| local-parser-boundary | 90 | 0 | command_exits_zero_or_existing_report_is_present, expected_output_path_exists, public_safe_boundary_still_visible, timing_within_stage_budget_or_within_variance_threshold | record missing report, timeout, unclear boundary, stale output, or timing variance above threshold before continuing | rerun stage command and inspect the expected report path |
| source-lane-boundary | 90 | 0 | command_exits_zero_or_existing_report_is_present, expected_output_path_exists, public_safe_boundary_still_visible, timing_within_stage_budget_or_within_variance_threshold | record missing report, timeout, unclear boundary, stale output, or timing variance above threshold before continuing | rerun stage command and inspect the expected report path |
| workflow-depth | 90 | 0 | command_exits_zero_or_existing_report_is_present, expected_output_path_exists, public_safe_boundary_still_visible, timing_within_stage_budget_or_within_variance_threshold | record missing report, timeout, unclear boundary, stale output, or timing variance above threshold before continuing | rerun stage command and inspect the expected report path |
| retriever-decision | 90 | 15 | command_exits_zero_or_existing_report_is_present, expected_output_path_exists, public_safe_boundary_still_visible, timing_within_stage_budget_or_within_variance_threshold | record missing report, timeout, unclear boundary, stale output, or timing variance above threshold before continuing | rerun stage command and inspect the expected report path |
| operator-surface | 90 | 0 | command_exits_zero_or_existing_report_is_present, expected_output_path_exists, public_safe_boundary_still_visible, timing_within_stage_budget_or_within_variance_threshold | record missing report, timeout, unclear boundary, stale output, or timing variance above threshold before continuing | rerun stage command and inspect the expected report path |

## Checks

| Check | OK |
|---|---|
| stage_checks_present | True |
| each_stage_has_pass_checks | True |
| each_stage_has_failure_note | True |
| each_stage_has_recovery_route | True |
| has_timing_check | True |
| next_milestone_named | True |

## Errors

- none

## Next Leaf

- `DRQ3_rehearsal_evidence_capture`

## Machine Result

```json
{
  "title": "DRQ2 Demo Run Quality Checklist",
  "ok": true,
  "horizon": "demo-rehearsal-quality-loop",
  "completed_milestone": "DRQ2",
  "source_stage_count": 8,
  "stage_checks": [
    {
      "stage_id": "position",
      "target_seconds": 60,
      "timing_variance_threshold_seconds": 0,
      "pass_checks": [
        "command_exits_zero_or_existing_report_is_present",
        "expected_output_path_exists",
        "public_safe_boundary_still_visible",
        "timing_within_stage_budget_or_within_variance_threshold"
      ],
      "failure_note": "record missing report, timeout, unclear boundary, stale output, or timing variance above threshold before continuing",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "storyboard",
      "target_seconds": 90,
      "timing_variance_threshold_seconds": 0,
      "pass_checks": [
        "command_exits_zero_or_existing_report_is_present",
        "expected_output_path_exists",
        "public_safe_boundary_still_visible",
        "timing_within_stage_budget_or_within_variance_threshold"
      ],
      "failure_note": "record missing report, timeout, unclear boundary, stale output, or timing variance above threshold before continuing",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "scenario-contract",
      "target_seconds": 90,
      "timing_variance_threshold_seconds": 0,
      "pass_checks": [
        "command_exits_zero_or_existing_report_is_present",
        "expected_output_path_exists",
        "public_safe_boundary_still_visible",
        "timing_within_stage_budget_or_within_variance_threshold"
      ],
      "failure_note": "record missing report, timeout, unclear boundary, stale output, or timing variance above threshold before continuing",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "local-parser-boundary",
      "target_seconds": 90,
      "timing_variance_threshold_seconds": 0,
      "pass_checks": [
        "command_exits_zero_or_existing_report_is_present",
        "expected_output_path_exists",
        "public_safe_boundary_still_visible",
        "timing_within_stage_budget_or_within_variance_threshold"
      ],
      "failure_note": "record missing report, timeout, unclear boundary, stale output, or timing variance above threshold before continuing",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "source-lane-boundary",
      "target_seconds": 90,
      "timing_variance_threshold_seconds": 0,
      "pass_checks": [
        "command_exits_zero_or_existing_report_is_present",
        "expected_output_path_exists",
        "public_safe_boundary_still_visible",
        "timing_within_stage_budget_or_within_variance_threshold"
      ],
      "failure_note": "record missing report, timeout, unclear boundary, stale output, or timing variance above threshold before continuing",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "workflow-depth",
      "target_seconds": 90,
      "timing_variance_threshold_seconds": 0,
      "pass_checks": [
        "command_exits_zero_or_existing_report_is_present",
        "expected_output_path_exists",
        "public_safe_boundary_still_visible",
        "timing_within_stage_budget_or_within_variance_threshold"
      ],
      "failure_note": "record missing report, timeout, unclear boundary, stale output, or timing variance above threshold before continuing",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "retriever-decision",
      "target_seconds": 90,
      "timing_variance_threshold_seconds": 15,
      "pass_checks": [
        "command_exits_zero_or_existing_report_is_present",
        "expected_output_path_exists",
        "public_safe_boundary_still_visible",
        "timing_within_stage_budget_or_within_variance_threshold"
      ],
      "failure_note": "record missing report, timeout, unclear boundary, stale output, or timing variance above threshold before continuing",
      "recovery_route": "rerun stage command and inspect the expected report path"
    },
    {
      "stage_id": "operator-surface",
      "target_seconds": 90,
      "timing_variance_threshold_seconds": 0,
      "pass_checks": [
        "command_exits_zero_or_existing_report_is_present",
        "expected_output_path_exists",
        "public_safe_boundary_still_visible",
        "timing_within_stage_budget_or_within_variance_threshold"
      ],
      "failure_note": "record missing report, timeout, unclear boundary, stale output, or timing variance above threshold before continuing",
      "recovery_route": "rerun stage command and inspect the expected report path"
    }
  ],
  "checks": {
    "stage_checks_present": true,
    "each_stage_has_pass_checks": true,
    "each_stage_has_failure_note": true,
    "each_stage_has_recovery_route": true,
    "has_timing_check": true,
    "next_milestone_named": true
  },
  "errors": [],
  "next_leaf": "DRQ3_rehearsal_evidence_capture",
  "report_path": "docs/reports/2026-07-05-drq2-demo-run-quality-checklist.md"
}
```
