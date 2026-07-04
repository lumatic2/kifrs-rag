# RAG Quality Refresh Close Report

> Date: 2026-07-05
> Horizon sequence: `docs/horizons/accounting-intelligence-expansion.md` Horizon 1
> Working horizon: `docs/horizons/rag-optimization-resume.md`
> Final gate: `python scripts\rag_quality_final_gate.py --format text`

## What Changed

This pass did not replace the default `hybrid` retriever. Instead, it built a measured opt-in repair stack for known
goldset miss patterns:

1. `source_routed_hybrid` — accepted standard routing for 1001/1037/1102 clusters.
2. reviewed `user_note_v2` seeds — Q039/Q048 and Q029 targeted term bridges.
3. `ifrs1115_subquery_hybrid` — Q001/Q006 focused 1115 subqueries.
4. `ifrs1109_scope_hybrid` — Q008 1109 scope-exclusion insertion without displacing 1116 hits.
5. `ifrs1109_classification_hybrid` — Q040 1109 residual classification subquery.

## Result

Full 50-item retrieval-only eval:

| Retriever | recall@1 | recall@3 | recall@5 | recall@10 | recall@20 | MRR | nDCG@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| hybrid | 0.197 | 0.387 | 0.547 | 0.713 | 0.887 | 0.464 | 0.482 |
| source_routed_hybrid | 0.223 | 0.387 | 0.547 | 0.747 | 0.953 | 0.497 | 0.507 |
| ifrs1115_subquery_hybrid | 0.233 | 0.397 | 0.557 | 0.767 | 0.973 | 0.517 | 0.524 |
| ifrs1109_scope_hybrid | 0.233 | 0.397 | 0.563 | 0.773 | 0.980 | 0.517 | 0.528 |
| ifrs1109_classification_hybrid | 0.233 | 0.397 | 0.563 | 0.773 | 1.000 | 0.518 | 0.528 |

Citation-level bucket summary:

| Retriever | hit@5 | hit@10 | hit@20 | beyond@20 | absent |
|---|---:|---:|---:|---:|---:|
| hybrid | 45 | 14 | 14 | 0 | 9 |
| ifrs1109_classification_hybrid | 47 | 18 | 17 | 0 | 0 |

## Gate Output

```text
ok: True
items: 50
k: 20
baseline_recall@20: 0.887
target_recall@20: 1.000
baseline_buckets: {'hit@5': 45, 'hit@10': 14, 'hit@20': 14, 'beyond@20': 0, 'absent': 9}
target_buckets: {'hit@5': 47, 'hit@10': 18, 'hit@20': 17, 'beyond@20': 0, 'absent': 0}
target_misses: []
```

## Interpretation

This is a retrieval quality win, not a default-runtime decision.

What is now true:

- The current 50-item goldset has no top-20 required-citation misses under the final opt-in retriever.
- Each repair layer has a focused gate that checks recovery and preservation boundaries.
- The reports explain which pattern each layer handles.

What is not yet true:

- The final repair stack is not proven as a general-purpose default retriever.
- The layer triggers were reviewed against the current goldset, not against broad real-world usage.
- MRR/nDCG improved only modestly; the main win is recall coverage.

## Next Decision

Keep the final retriever opt-in until real usage or accountant feedback confirms these patterns. The next product step is
not more goldset repair; it is to connect this stronger retrieval layer to real-accountant-session demos and, after that,
move to Accounting Intelligence Expansion Horizon 2: authority source map.
