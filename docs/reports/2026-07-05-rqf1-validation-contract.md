# RQF1 Validation Corpus And Acceptance Contract

> Scope: public-safe RAG quality validation contract for the active objective-gap horizon.

## 한 줄 결론

RAG quality validation must produce fresh baseline, regression, rollback, and authorization evidence before any default retriever change.

## Contract

- Scope: fresh RAG quality validation before default retriever promotion
- Dataset boundary: public-safe eval metadata and local private eval assets by reference only
- Default change allowed in RQF1: False
- Result space: promote, defer, rollback, blocked

## Commands

| ID | Command | Evidence | Exists | Purpose |
|---|---|---|---|---|
| gap_audit | `python scripts\accounting_intelligence_gap_audit.py --format text --write` | `docs/reports/2026-07-05-accounting-intelligence-gap-audit.md` | True | Confirm current Objective gaps and automation snapshot before RAG work. |
| default_guard | `python scripts\default_retriever_guard.py --format text` | `docs/reports/2026-07-05-default-retriever-guard.md` | True | Confirm default retriever cannot change without stronger evidence and authorization. |
| promotion_close | `python scripts\runtime_retriever_promotion_close_gate.py --format text` | `docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md` | True | Carry forward previous promote/defer/rollback evidence. |

## Metrics

| Metric | Threshold | Reason |
|---|---|---|
| recall_at_20 | 0.95 | RAG answer quality must retrieve likely source paragraphs before answer composition. |
| regression_count | 0 | A stronger retriever cannot regress known cases before default promotion. |
| latency_budget_seconds | 2.0 | Interactive accounting use cannot require slow default retrieval. |
| rollback_available | True | Default retriever changes must be reversible. |

## Promotion Blockers

- missing fresh baseline snapshot
- missing opt-in regression matrix
- any known regression
- rollback evidence missing
- explicit authorization missing

## Boundaries

- Public reports may include commands, metrics, pass/fail status, and report paths.
- Public reports may not include K-IFRS source text, parsed DB rows, embeddings, dogfood prompts, private payloads, or secrets.
- Local private eval assets may be referenced as missing-local-evidence but not printed.
- Default retriever remains unchanged until promotion gate and explicit authorization both pass.

## Checks

| Check | OK |
|---|---|
| all_commands_have_evidence | True |
| all_commands_are_local_scripts | True |
| metrics_defined | True |
| promotion_blockers_defined | True |
| public_safety_boundaries_defined | True |
| default_change_forbidden_in_rqf1 | True |

## Errors

- none

## Next Leaf

- `RQF2_current_retriever_baseline_snapshot`

## Machine Result

```json
{
  "title": "RQF1 Validation Corpus And Acceptance Contract",
  "ok": true,
  "horizon": "rag-quality-fresh-validation",
  "completed_milestone": "RQF1",
  "contract": {
    "scope": "fresh RAG quality validation before default retriever promotion",
    "dataset_boundary": "public-safe eval metadata and local private eval assets by reference only",
    "promotion_result_space": [
      "promote",
      "defer",
      "rollback",
      "blocked"
    ],
    "default_change_allowed": false
  },
  "commands": [
    {
      "command_id": "gap_audit",
      "command": "python scripts\\accounting_intelligence_gap_audit.py --format text --write",
      "evidence": "docs/reports/2026-07-05-accounting-intelligence-gap-audit.md",
      "evidence_exists": true,
      "purpose": "Confirm current Objective gaps and automation snapshot before RAG work."
    },
    {
      "command_id": "default_guard",
      "command": "python scripts\\default_retriever_guard.py --format text",
      "evidence": "docs/reports/2026-07-05-default-retriever-guard.md",
      "evidence_exists": true,
      "purpose": "Confirm default retriever cannot change without stronger evidence and authorization."
    },
    {
      "command_id": "promotion_close",
      "command": "python scripts\\runtime_retriever_promotion_close_gate.py --format text",
      "evidence": "docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md",
      "evidence_exists": true,
      "purpose": "Carry forward previous promote/defer/rollback evidence."
    }
  ],
  "metrics": [
    {
      "name": "recall_at_20",
      "minimum": 0.95,
      "reason": "RAG answer quality must retrieve likely source paragraphs before answer composition."
    },
    {
      "name": "regression_count",
      "maximum": 0,
      "reason": "A stronger retriever cannot regress known cases before default promotion."
    },
    {
      "name": "latency_budget_seconds",
      "maximum": 2.0,
      "reason": "Interactive accounting use cannot require slow default retrieval."
    },
    {
      "name": "rollback_available",
      "required": true,
      "reason": "Default retriever changes must be reversible."
    }
  ],
  "promotion_blockers": [
    "missing fresh baseline snapshot",
    "missing opt-in regression matrix",
    "any known regression",
    "rollback evidence missing",
    "explicit authorization missing"
  ],
  "boundaries": [
    "Public reports may include commands, metrics, pass/fail status, and report paths.",
    "Public reports may not include K-IFRS source text, parsed DB rows, embeddings, dogfood prompts, private payloads, or secrets.",
    "Local private eval assets may be referenced as missing-local-evidence but not printed.",
    "Default retriever remains unchanged until promotion gate and explicit authorization both pass."
  ],
  "checks": {
    "all_commands_have_evidence": true,
    "all_commands_are_local_scripts": true,
    "metrics_defined": true,
    "promotion_blockers_defined": true,
    "public_safety_boundaries_defined": true,
    "default_change_forbidden_in_rqf1": true
  },
  "errors": [],
  "next_leaf": "RQF2_current_retriever_baseline_snapshot",
  "report_path": "docs/reports/2026-07-05-rqf1-validation-contract.md"
}
```
