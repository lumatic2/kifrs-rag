# ORPD1 Opt-In Retriever Promotion Decision Gate

> Scope: stop/go gate before changing the default retriever from `hybrid` to the final opt-in repair stack.

## 한 줄 결론

`ifrs1109_classification_hybrid` remains opt-in. Retrieval metrics pass, but stronger internal evaluation evidence and explicit authorization are still required before changing the default retriever.

## Decision

- Decision: defer
- Promote to default: False
- Target retriever: `ifrs1109_classification_hybrid`
- Demo validation ok: True
- Stronger internal eval evidence: True
- Explicit authorization: False

## Blockers

- explicit user authorization is required before changing the default retriever

## Retrieval Evidence

- Demo validation report: `docs\reports\2026-07-05-odv1-opt-in-retriever-demo-validation.md`
- Target recall@20: 1.000
- Required-citation absent count: 0
- Target misses: 0
- Current default promotion state: deferred

## Boundary

- This gate does not change runtime defaults.
- The current default retriever remains unchanged unless this gate returns `promote` and a separate implementation changes the default.
- Retrieval-only quality is not answer-quality proof and does not replace broader eval coverage.

## Next Leaf

RAG reliability revalidation RR2/RR3/RR5, then explicit authorization before default retriever change

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "decision": {
    "decision_id": "orpd1-opt-in-retriever-promotion-decision-gate",
    "decision": "defer",
    "promote_to_default": false,
    "target_retriever": "ifrs1109_classification_hybrid",
    "demo_validation_ok": true,
    "stronger_internal_eval_evidence": true,
    "explicit_authorization": false,
    "blockers": [
      "explicit user authorization is required before changing the default retriever"
    ],
    "next_leaf": "RAG reliability revalidation RR2/RR3/RR5, then explicit authorization before default retriever change"
  },
  "demo_validation": {
    "ok": true,
    "target_retriever": "ifrs1109_classification_hybrid",
    "target_recall20": 1.0,
    "target_buckets": {
      "hit@5": 47,
      "hit@10": 18,
      "hit@20": 17,
      "beyond@20": 0,
      "absent": 0
    },
    "target_misses": [],
    "default_promotion": "deferred",
    "report_path": "docs\\reports\\2026-07-05-odv1-opt-in-retriever-demo-validation.md"
  },
  "report_path": "docs\\reports\\2026-07-05-orpd1-opt-in-retriever-promotion-decision-gate.md",
  "next_leaf": "RAG reliability revalidation RR2/RR3/RR5, then explicit authorization before default retriever change"
}
```
