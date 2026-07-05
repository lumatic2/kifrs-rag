# RPG1 Promotion Evidence Inventory

> Scope: RPG1 inventory for runtime retriever promotion decisioning.

## 한 줄 결론

The opt-in repair retriever has strong recall-supporting evidence, but current product evidence still points to `defer` until regression/latency, rollback, and operator evidence are added.

## Runtime Boundary

- target retriever: `ifrs1109_classification_hybrid`
- current default: `hybrid`
- promotion decision now: `defer`
- next gate: `regression_and_latency_gate`

## Promotion-Supporting Evidence

- `target_recall_at_20_full_coverage` — final opt-in retriever reaches recall@20 1.000 on current 50-item retrieval-only eval (`docs/reports/2026-07-05-rag-quality-refresh-close-report.md`)
- `target_misses_zero` — final gate reports no target misses under opt-in repair stack (`scripts/rag_quality_final_gate.py`)
- `repair_retriever_available` — ifrs1109_classification_hybrid exists as an opt-in eval retriever (`scripts/default_retriever_guard.py`)

## Promotion-Blocking Evidence

- `default_guard_defers_promotion` — default guard decision is defer and promote_to_default is False (`docs/reports/2026-07-05-default-retriever-guard.md`)
- `target_not_exposed_in_mcp` — target repair retriever is not exposed as an MCP search mode (`scripts/default_retriever_guard.py`)
- `general_usage_not_proven` — current evidence is strong on the 50-item eval but not yet a broad default-runtime proof (`docs/reports/2026-07-05-rag-quality-refresh-close-report.md`)

## Advisory Evidence

- `product_trust_failure_boundaries` — product trust close gate carries retrieval_quality and default_promotion failure categories (`docs/reports/2026-07-05-product-trust-quality-close-report.md`)
- `workflow_coverage_closed` — workflow coverage expansion is closed, so promotion decision can focus on runtime retrieval quality (`docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md`)

## Missing Evidence Before Promotion

- broad runtime latency/cost measurement
- regression gate that compares recall/citation preservation and runtime cost together
- operator rollback policy and command surface
- explicit final promote/defer/block close result

## Checks

| Check | OK |
|---|---|
| final_gate_ok | True |
| default_guard_ok | True |
| product_trust_ok | True |
| supporting_evidence_present | True |
| blocking_evidence_present | True |
| advisory_evidence_present | True |
| missing_evidence_recorded | True |
| all_required_reports_present | True |

## Required Reports

| Report | Path | Exists |
|---|---|---|
| rag_quality_close | `docs/reports/2026-07-05-rag-quality-refresh-close-report.md` | True |
| default_retriever_guard | `docs/reports/2026-07-05-default-retriever-guard.md` | True |
| product_trust_close | `docs/reports/2026-07-05-product-trust-quality-close-report.md` | True |
| failure_boundary | `docs/reports/2026-07-05-ptq3-failure-boundary-matrix.md` | True |
| workflow_coverage_close | `docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md` | True |

## Errors

- none

## Machine Result

```json
{
  "title": "RPG1 Promotion Evidence Inventory",
  "ok": true,
  "horizon": "runtime-retriever-promotion-gate",
  "completed_milestone": "RPG1",
  "target_retriever": "ifrs1109_classification_hybrid",
  "current_default": "hybrid",
  "promotion_decision_now": "defer",
  "promotion_supporting": [
    {
      "id": "target_recall_at_20_full_coverage",
      "evidence": "final opt-in retriever reaches recall@20 1.000 on current 50-item retrieval-only eval",
      "source": "docs/reports/2026-07-05-rag-quality-refresh-close-report.md"
    },
    {
      "id": "target_misses_zero",
      "evidence": "final gate reports no target misses under opt-in repair stack",
      "source": "scripts/rag_quality_final_gate.py"
    },
    {
      "id": "repair_retriever_available",
      "evidence": "ifrs1109_classification_hybrid exists as an opt-in eval retriever",
      "source": "scripts/default_retriever_guard.py"
    }
  ],
  "promotion_blocking": [
    {
      "id": "default_guard_defers_promotion",
      "evidence": "default guard decision is defer and promote_to_default is False",
      "source": "docs/reports/2026-07-05-default-retriever-guard.md"
    },
    {
      "id": "target_not_exposed_in_mcp",
      "evidence": "target repair retriever is not exposed as an MCP search mode",
      "source": "scripts/default_retriever_guard.py"
    },
    {
      "id": "general_usage_not_proven",
      "evidence": "current evidence is strong on the 50-item eval but not yet a broad default-runtime proof",
      "source": "docs/reports/2026-07-05-rag-quality-refresh-close-report.md"
    }
  ],
  "advisory": [
    {
      "id": "product_trust_failure_boundaries",
      "evidence": "product trust close gate carries retrieval_quality and default_promotion failure categories",
      "source": "docs/reports/2026-07-05-product-trust-quality-close-report.md"
    },
    {
      "id": "workflow_coverage_closed",
      "evidence": "workflow coverage expansion is closed, so promotion decision can focus on runtime retrieval quality",
      "source": "docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md"
    }
  ],
  "missing_evidence": [
    "broad runtime latency/cost measurement",
    "regression gate that compares recall/citation preservation and runtime cost together",
    "operator rollback policy and command surface",
    "explicit final promote/defer/block close result"
  ],
  "checks": {
    "final_gate_ok": true,
    "default_guard_ok": true,
    "product_trust_ok": true,
    "supporting_evidence_present": true,
    "blocking_evidence_present": true,
    "advisory_evidence_present": true,
    "missing_evidence_recorded": true,
    "all_required_reports_present": true
  },
  "errors": [],
  "reports": {
    "rag_quality_close": {
      "path": "docs/reports/2026-07-05-rag-quality-refresh-close-report.md",
      "exists": true
    },
    "default_retriever_guard": {
      "path": "docs/reports/2026-07-05-default-retriever-guard.md",
      "exists": true
    },
    "product_trust_close": {
      "path": "docs/reports/2026-07-05-product-trust-quality-close-report.md",
      "exists": true
    },
    "failure_boundary": {
      "path": "docs/reports/2026-07-05-ptq3-failure-boundary-matrix.md",
      "exists": true
    },
    "workflow_coverage_close": {
      "path": "docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md",
      "exists": true
    }
  },
  "missing_reports": [],
  "next_gate": "regression_and_latency_gate",
  "report_path": "docs/reports/2026-07-05-rpg1-promotion-evidence-inventory.md"
}
```
