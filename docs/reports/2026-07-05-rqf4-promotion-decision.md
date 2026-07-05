# RQF4 Promotion Decision Gate

> Scope: promote/defer/rollback decision for RAG default retriever status.

## 한 줄 결론

Decision: `defer`. Promotion is not allowed because fresh numeric evidence and explicit authorization are missing.

## Decision

- Result: `defer`
- Default change allowed: False
- Rollback required if later promoted: True

## Blockers

- fresh numeric baseline eval missing
- fresh opt-in regression comparison missing
- fresh latency comparison missing
- explicit authorization missing

## Evidence

| ID | Path | Exists |
|---|---|---|
| validation_contract | `docs/reports/2026-07-05-rqf1-validation-contract.md` | True |
| baseline_snapshot | `docs/reports/2026-07-05-rqf2-baseline-snapshot.md` | True |
| regression_matrix | `docs/reports/2026-07-05-rqf3-regression-matrix.md` | True |
| default_guard | `docs/reports/2026-07-05-default-retriever-guard.md` | True |

## Checks

| Check | OK |
|---|---|
| all_evidence_exists | True |
| decision_is_valid | True |
| default_change_forbidden | True |
| blockers_present | True |
| rollback_requirement_present | True |

## Errors

- none

## Next Leaf

- `RQF5_horizon_close_and_next_gap_handoff`

## Machine Result

```json
{
  "title": "RQF4 Promotion Decision Gate",
  "ok": true,
  "horizon": "rag-quality-fresh-validation",
  "completed_milestone": "RQF4",
  "decision": {
    "result": "defer",
    "default_change_allowed": false,
    "rollback_required_if_later_promoted": true,
    "reason": "Promotion is not allowed because fresh numeric evidence and explicit authorization are missing."
  },
  "blockers": [
    "fresh numeric baseline eval missing",
    "fresh opt-in regression comparison missing",
    "fresh latency comparison missing",
    "explicit authorization missing"
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
      "id": "regression_matrix",
      "path": "docs/reports/2026-07-05-rqf3-regression-matrix.md",
      "exists": true
    },
    {
      "id": "default_guard",
      "path": "docs/reports/2026-07-05-default-retriever-guard.md",
      "exists": true
    }
  ],
  "checks": {
    "all_evidence_exists": true,
    "decision_is_valid": true,
    "default_change_forbidden": true,
    "blockers_present": true,
    "rollback_requirement_present": true
  },
  "errors": [],
  "next_leaf": "RQF5_horizon_close_and_next_gap_handoff",
  "report_path": "docs/reports/2026-07-05-rqf4-promotion-decision.md"
}
```
