# RQF3 Opt-In Retriever Regression Matrix

> Scope: public-safe regression matrix for opt-in retriever promotion evidence.

## 한 줄 결론

Matrix result: `defer_until_fresh_comparison`. Rollback evidence exists, but quality and latency axes need fresh local reruns.

## Regression Matrix

| Axis | Baseline | Opt-In | Pass | Blocker |
|---|---|---|---|---|
| fresh_numeric_eval | missing_public_numeric_eval | previous_evidence_only | False | fresh baseline and opt-in rerun are missing |
| known_regressions | not_recomputed | not_recomputed | False | regression count cannot be trusted without a fresh comparison run |
| latency | not_recomputed | not_recomputed | False | latency budget cannot be trusted without a fresh local timing run |
| rollback | current_default_preserved | rollback_policy_documented | True | none |

## Evidence

| ID | Path | Exists |
|---|---|---|
| validation_contract | `docs/reports/2026-07-05-rqf1-validation-contract.md` | True |
| baseline_snapshot | `docs/reports/2026-07-05-rqf2-baseline-snapshot.md` | True |
| previous_promotion_gate | `docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md` | True |

## Checks

| Check | OK |
|---|---|
| all_evidence_exists | True |
| all_axes_present | True |
| rollback_axis_passes | True |
| quality_axes_do_not_pass_without_fresh_runs | True |

## Errors

- none

## Next Leaf

- `RQF4_promotion_decision_gate`

## Machine Result

```json
{
  "title": "RQF3 Opt-In Retriever Regression Matrix",
  "ok": true,
  "horizon": "rag-quality-fresh-validation",
  "completed_milestone": "RQF3",
  "matrix_result": "defer_until_fresh_comparison",
  "comparisons": [
    {
      "axis": "fresh_numeric_eval",
      "baseline_status": "missing_public_numeric_eval",
      "opt_in_status": "previous_evidence_only",
      "pass": false,
      "blocker": "fresh baseline and opt-in rerun are missing"
    },
    {
      "axis": "known_regressions",
      "baseline_status": "not_recomputed",
      "opt_in_status": "not_recomputed",
      "pass": false,
      "blocker": "regression count cannot be trusted without a fresh comparison run"
    },
    {
      "axis": "latency",
      "baseline_status": "not_recomputed",
      "opt_in_status": "not_recomputed",
      "pass": false,
      "blocker": "latency budget cannot be trusted without a fresh local timing run"
    },
    {
      "axis": "rollback",
      "baseline_status": "current_default_preserved",
      "opt_in_status": "rollback_policy_documented",
      "pass": true,
      "blocker": "none"
    }
  ],
  "evidence": [
    {
      "id": "validation_contract",
      "path": "docs/reports/2026-07-05-rqf1-validation-contract.md",
      "exists": true
    },
    {
      "id": "baseline_snapshot",
      "path": "docs/reports/2026-07-05-rqf2-baseline-snapshot.md",
      "exists": true
    },
    {
      "id": "previous_promotion_gate",
      "path": "docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md",
      "exists": true
    }
  ],
  "checks": {
    "all_evidence_exists": true,
    "all_axes_present": true,
    "rollback_axis_passes": true,
    "quality_axes_do_not_pass_without_fresh_runs": true
  },
  "errors": [],
  "next_leaf": "RQF4_promotion_decision_gate",
  "report_path": "docs/reports/2026-07-05-rqf3-regression-matrix.md"
}
```
