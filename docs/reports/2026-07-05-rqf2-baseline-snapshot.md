# RQF2 Current Retriever Baseline Snapshot

> Scope: public-safe baseline snapshot for the current default retriever.

## 한 줄 결론

The baseline contract is ready, but fresh numeric local eval evidence is not present in public reports; default retriever changes remain forbidden.

## Baseline

- Default retriever: `current_default_hybrid`
- Default change allowed: False
- Public fresh numeric eval available: False
- Status: `baseline_contract_ready_numeric_eval_missing`

## Missing Local Evidence

- fresh eval run against local K-IFRS DB
- fresh latency run on local retriever
- fresh regression comparison against opt-in retriever

## Evidence

| ID | Path | Exists |
|---|---|---|
| validation_contract | `docs/reports/2026-07-05-rqf1-validation-contract.md` | True |
| gap_audit | `docs/reports/2026-07-05-accounting-intelligence-gap-audit.md` | True |
| default_guard | `docs/reports/2026-07-05-default-retriever-guard.md` | True |
| previous_promotion_gate | `docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md` | True |

## Checks

| Check | OK |
|---|---|
| all_required_evidence_exists | True |
| default_change_forbidden | True |
| missing_local_evidence_recorded | True |
| public_numeric_eval_not_faked | True |

## Errors

- none

## Next Leaf

- `RQF3_opt_in_retriever_regression_matrix`

## Machine Result

```json
{
  "title": "RQF2 Current Retriever Baseline Snapshot",
  "ok": true,
  "horizon": "rag-quality-fresh-validation",
  "completed_milestone": "RQF2",
  "baseline": {
    "default_retriever": "current_default_hybrid",
    "default_change_allowed": false,
    "fresh_numeric_eval_available_in_public_report": false,
    "public_safe_status": "baseline_contract_ready_numeric_eval_missing",
    "missing_local_evidence": [
      "fresh eval run against local K-IFRS DB",
      "fresh latency run on local retriever",
      "fresh regression comparison against opt-in retriever"
    ]
  },
  "evidence": [
    {
      "id": "validation_contract",
      "path": "docs/reports/2026-07-05-rqf1-validation-contract.md",
      "exists": true
    },
    {
      "id": "gap_audit",
      "path": "docs/reports/2026-07-05-accounting-intelligence-gap-audit.md",
      "exists": true
    },
    {
      "id": "default_guard",
      "path": "docs/reports/2026-07-05-default-retriever-guard.md",
      "exists": true
    },
    {
      "id": "previous_promotion_gate",
      "path": "docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md",
      "exists": true
    }
  ],
  "checks": {
    "all_required_evidence_exists": true,
    "default_change_forbidden": true,
    "missing_local_evidence_recorded": true,
    "public_numeric_eval_not_faked": true
  },
  "errors": [],
  "next_leaf": "RQF3_opt_in_retriever_regression_matrix",
  "report_path": "docs/reports/2026-07-05-rqf2-baseline-snapshot.md"
}
```
