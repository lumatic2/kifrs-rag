# PTQ4 Promotion Decision Evidence Pack

> Scope: PTQ4 product-facing evidence for retriever promotion decision.

## One-Line Result

Default retriever promotion remains deferred; the repair retriever stays opt-in until explicit authorization and separate implementation.

## Decision

- decision: `defer`
- promote to default: False
- current default: `hybrid`
- target retriever: `ifrs1109_classification_hybrid`

## Evidence

| Evidence | Value |
|---|---|
| rag_quality_ok | `True` |
| target_recall20 | `1.0` |
| target_absent_citations | `0` |
| default_guard_ok | `True` |
| target_exposed_in_mcp | `False` |
| cached_promotion_decision | `defer` |
| failure_matrix_ok | `True` |
| failure_categories | `['retrieval_quality', 'citation_assembly', 'client_private_fact_gap', 'unsupported_workflow', 'authority_boundary', 'default_promotion']` |

## Blockers

- explicit promotion authorization is absent

## Operator Policy

- Keep runtime default retriever as hybrid.
- Use ifrs1109_classification_hybrid as opt-in evaluation/demo repair evidence only.
- A future default change requires explicit authorization and separate implementation.
- If RAG/citation failures appear, follow PTQ3 failure boundary actions before trusting output.

## Machine Result

```json
{
  "title": "PTQ4 Promotion Decision Evidence Pack",
  "ok": true,
  "horizon": "product-trust-and-quality-evidence",
  "milestone": "PTQ4",
  "decision": "defer",
  "promote_to_default": false,
  "current_default": "hybrid",
  "target_retriever": "ifrs1109_classification_hybrid",
  "evidence": {
    "rag_quality_ok": true,
    "target_recall20": 1.0,
    "target_absent_citations": 0,
    "default_guard_ok": true,
    "target_exposed_in_mcp": false,
    "cached_promotion_decision": "defer",
    "failure_matrix_ok": true,
    "failure_categories": [
      "retrieval_quality",
      "citation_assembly",
      "client_private_fact_gap",
      "unsupported_workflow",
      "authority_boundary",
      "default_promotion"
    ]
  },
  "blockers": [
    "explicit promotion authorization is absent"
  ],
  "operator_policy": [
    "Keep runtime default retriever as hybrid.",
    "Use ifrs1109_classification_hybrid as opt-in evaluation/demo repair evidence only.",
    "A future default change requires explicit authorization and separate implementation.",
    "If RAG/citation failures appear, follow PTQ3 failure boundary actions before trusting output."
  ],
  "report_path": "docs/reports/2026-07-05-ptq4-promotion-decision-evidence.md",
  "next_leaf": "PTQ5_trust_quality_close_gate"
}
```
