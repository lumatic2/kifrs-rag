# RR4 Repair Policy Candidate

> Scope: decide which RAG repair behavior can be used now, and which runtime changes stay deferred.

## 한 줄 결론

Use the repair retriever as an opt-in eval/demo path, keep runtime default unchanged, and carry promotion to RR5.

## Methodology Source

- `rag-evaluation-metrics`
- `rag-retrieval-strategy`
- `rag-retrieval-rank-debugging-playbook`
- `rag-reranking-strategy`

## Accepted Policies

| ID | Policy | Why | Evidence |
|---|---|---|---|
| keep_default_hybrid | Keep MCP runtime default at `hybrid`. | Default remains stable while RR evidence is retrieval/citation-focused rather than full answer-quality proof. | default retriever guard |
| keep_target_opt_in_eval_path | Keep `ifrs1109_classification_hybrid` available as an opt-in eval/demo retriever. | RR3 shows target recall@20 is 1.000 with zero required-citation top-20 misses. | RR3 retrieval/citation diagnostics |
| use_bucket_diagnostics_for_rr5 | Use RR2 buckets and RR3 rank transitions as the promotion evidence shape. | Bucket-level evidence exposes disclosure, workflow, judgment, and exam-convention behavior without protected question text. | RR2 eval matrix + RR3 diagnostics |

## Deferred Policies

| ID | Policy | Blocker |
|---|---|---|
| default_promotion | Do not promote `ifrs1109_classification_hybrid` to default in this milestone. | Requires RR5 promotion gate and explicit authorization. |
| mcp_mode_exposure | Do not expose `ifrs1109_classification_hybrid` as an MCP search mode yet. | Would change user-facing runtime behavior before answer-quality regression policy is finalized. |
| heavy_reranker_default | Do not make reranked or heavy reranker paths default. | RR3's current issue is coverage/promotion policy, not a measured need for heavier latency/cost. |
| new_external_source_ingestion | Do not add non-IFRS source ingestion inside this RAG reliability horizon. | That belongs to the next horizon after RR5 handoff. |

## Guard Snapshot

- Default mode: `hybrid`
- Target retriever: `ifrs1109_classification_hybrid`
- Target exposed in MCP: False
- Promotion decision: defer
- Promote to default: False

## RR3 Snapshot

- Target misses: 0
- Recovered item ids: Q001, Q004, Q006, Q008, Q013, Q025, Q026, Q040, Q041
- Failure taxonomy: {'rank_improved': 6, 'rank_worse': 2, 'recovered_from_absent': 9, 'target_items_with_misses': 0, 'unchanged': 65}

## Verification Commands

- `python scripts\default_retriever_guard.py --format text`
- `python scripts\rag_reliability_retrieval_citation_diagnostics.py --format text`
- `python scripts\quality_preflight.py --format text`

## Next Leaf

RR5 promotion gate and next-horizon handoff

## Machine Result

```json
{
  "ok": true,
  "title": "RR4 Repair Policy Candidate",
  "milestone": "RR4",
  "methodology_nodes": [
    "rag-evaluation-metrics",
    "rag-retrieval-strategy",
    "rag-retrieval-rank-debugging-playbook",
    "rag-reranking-strategy"
  ],
  "accepted_policies": [
    {
      "id": "keep_default_hybrid",
      "decision": "accept",
      "policy": "Keep MCP runtime default at `hybrid`.",
      "why": "Default remains stable while RR evidence is retrieval/citation-focused rather than full answer-quality proof.",
      "evidence": "default retriever guard"
    },
    {
      "id": "keep_target_opt_in_eval_path",
      "decision": "accept",
      "policy": "Keep `ifrs1109_classification_hybrid` available as an opt-in eval/demo retriever.",
      "why": "RR3 shows target recall@20 is 1.000 with zero required-citation top-20 misses.",
      "evidence": "RR3 retrieval/citation diagnostics"
    },
    {
      "id": "use_bucket_diagnostics_for_rr5",
      "decision": "accept",
      "policy": "Use RR2 buckets and RR3 rank transitions as the promotion evidence shape.",
      "why": "Bucket-level evidence exposes disclosure, workflow, judgment, and exam-convention behavior without protected question text.",
      "evidence": "RR2 eval matrix + RR3 diagnostics"
    }
  ],
  "deferred_policies": [
    {
      "id": "default_promotion",
      "decision": "defer",
      "policy": "Do not promote `ifrs1109_classification_hybrid` to default in this milestone.",
      "blocker": "Requires RR5 promotion gate and explicit authorization."
    },
    {
      "id": "mcp_mode_exposure",
      "decision": "defer",
      "policy": "Do not expose `ifrs1109_classification_hybrid` as an MCP search mode yet.",
      "blocker": "Would change user-facing runtime behavior before answer-quality regression policy is finalized."
    },
    {
      "id": "heavy_reranker_default",
      "decision": "defer",
      "policy": "Do not make reranked or heavy reranker paths default.",
      "blocker": "RR3's current issue is coverage/promotion policy, not a measured need for heavier latency/cost."
    },
    {
      "id": "new_external_source_ingestion",
      "decision": "defer",
      "policy": "Do not add non-IFRS source ingestion inside this RAG reliability horizon.",
      "blocker": "That belongs to the next horizon after RR5 handoff."
    }
  ],
  "verification_commands": [
    "python scripts\\default_retriever_guard.py --format text",
    "python scripts\\rag_reliability_retrieval_citation_diagnostics.py --format text",
    "python scripts\\quality_preflight.py --format text"
  ],
  "guard_snapshot": {
    "default_mode": "hybrid",
    "target_retriever": "ifrs1109_classification_hybrid",
    "target_retriever_exposed_in_mcp": false,
    "promotion_decision": "defer",
    "promote_to_default": false
  },
  "rr3_snapshot": {
    "target_misses": 0,
    "recovered_item_ids": [
      "Q001",
      "Q004",
      "Q006",
      "Q008",
      "Q013",
      "Q025",
      "Q026",
      "Q040",
      "Q041"
    ],
    "failure_taxonomy": {
      "rank_improved": 6,
      "rank_worse": 2,
      "recovered_from_absent": 9,
      "target_items_with_misses": 0,
      "unchanged": 65
    }
  },
  "next_leaf": "RR5 promotion gate and next-horizon handoff",
  "errors": [],
  "report_path": "docs/reports/2026-07-05-rr4-repair-policy-candidate.md"
}
```
