# RR5 RAG Promotion Gate

> Scope: final gate for closing the RAG reliability revalidation horizon.

## One-Line Conclusion

Close this horizon without default promotion. `ifrs1109_classification_hybrid` stays opt-in, and `non-ifrs-source-dataization` may use the regression commands below.

## Decision

- Default promotion: False
- Promotion decision: defer
- Target retriever: `ifrs1109_classification_hybrid`
- Reason: explicit user authorization is required before changing the default retriever
- Next horizon: `non-ifrs-source-dataization`
- Handoff ready: True

## Evidence Chain

| Report | Exists |
|---|---|
| `docs/reports/2026-07-05-rr1-rag-baseline-inventory.md` | True |
| `docs/reports/2026-07-05-rr2-eval-matrix.md` | True |
| `docs/reports/2026-07-05-rr3-retrieval-citation-diagnostics.md` | True |
| `docs/reports/2026-07-05-rr4-repair-policy-candidate.md` | True |

## Quality Snapshot

- Items: 50
- Baseline recall@20: 0.887
- Target recall@20: 1.000
- Target misses: 0
- Target absent citations: 0

## Runtime Guard

- Guard ok: True
- Default mode: `hybrid`
- Target exposed in MCP: False
- Guard promote_to_default: False

## Regression Commands For Next Horizon

- `python scripts\quality_preflight.py --format text`
- `python scripts\rag_quality_final_gate.py --format text`
- `python scripts\default_retriever_guard.py --format text`
- `python scripts\rag_reliability_retrieval_citation_diagnostics.py --format text`

## Machine Result

```json
{
  "ok": true,
  "title": "RR5 RAG Promotion Gate",
  "milestone": "RR5",
  "default_promotion": false,
  "promotion_decision": "defer",
  "target_retriever": "ifrs1109_classification_hybrid",
  "decision_reason": "explicit user authorization is required before changing the default retriever",
  "required_reports": [
    {
      "path": "docs/reports/2026-07-05-rr1-rag-baseline-inventory.md",
      "exists": true
    },
    {
      "path": "docs/reports/2026-07-05-rr2-eval-matrix.md",
      "exists": true
    },
    {
      "path": "docs/reports/2026-07-05-rr3-retrieval-citation-diagnostics.md",
      "exists": true
    },
    {
      "path": "docs/reports/2026-07-05-rr4-repair-policy-candidate.md",
      "exists": true
    }
  ],
  "final_gate_snapshot": {
    "ok": true,
    "n_items": 50,
    "baseline_recall20": 0.8867,
    "target_recall20": 1.0,
    "target_misses": 0,
    "target_absent_citations": 0
  },
  "default_guard_snapshot": {
    "ok": true,
    "default_mode": "hybrid",
    "target_retriever_exposed_in_mcp": false,
    "promote_to_default": false
  },
  "policy_snapshot": {
    "accepted": [
      "keep_default_hybrid",
      "keep_target_opt_in_eval_path",
      "use_bucket_diagnostics_for_rr5"
    ],
    "deferred": [
      "default_promotion",
      "mcp_mode_exposure",
      "heavy_reranker_default",
      "new_external_source_ingestion"
    ]
  },
  "regression_commands": [
    "python scripts\\quality_preflight.py --format text",
    "python scripts\\rag_quality_final_gate.py --format text",
    "python scripts\\default_retriever_guard.py --format text",
    "python scripts\\rag_reliability_retrieval_citation_diagnostics.py --format text"
  ],
  "next_horizon": "non-ifrs-source-dataization",
  "handoff_ready": true,
  "errors": [],
  "report_path": "docs/reports/2026-07-05-rr5-rag-promotion-gate.md"
}
```
