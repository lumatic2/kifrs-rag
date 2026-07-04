# IFRS 1115 Subquery Hybrid Implementation

> Date: 2026-07-05
> Horizon: `docs/horizons/rag-optimization-resume.md`
> Previous: `docs/reports/2026-07-05-ifrs1115-subquery-candidate-eval.md`

## Summary

Implemented opt-in `ifrs1115_subquery_hybrid`. The default `hybrid` retriever remains unchanged.

The new retriever starts from `source_routed_hybrid` and, only for reviewed 1115 gap patterns, fuses a focused 1115
subquery with weight 2. This recovers Q001 and Q006 while preserving the existing accepted source routes and Q029 seed.

## Commands

```powershell
python scripts\ifrs1115_subquery_gate.py --format text
python -m kifrs.eval.retrieval --k 20 --retrievers source_routed_hybrid ifrs1115_subquery_hybrid --only Q001 Q006 Q008 Q040 --no-save
python -m kifrs.eval.retrieval --k 20 --retrievers source_routed_hybrid ifrs1115_subquery_hybrid --no-save
python scripts\retrieval_must_cite_report.py --retrievers ifrs1115_subquery_hybrid --format markdown
```

## Result

Focused remaining hard-miss cluster:

| Retriever | recall@1 | recall@3 | recall@5 | recall@10 | recall@20 | MRR | nDCG@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| source_routed_hybrid | 0.000 | 0.083 | 0.208 | 0.208 | 0.417 | 0.146 | 0.118 |
| ifrs1115_subquery_hybrid | 0.125 | 0.208 | 0.333 | 0.458 | 0.667 | 0.396 | 0.329 |

Full 50-item retrieval-only eval:

| Retriever | recall@1 | recall@3 | recall@5 | recall@10 | recall@20 | MRR | nDCG@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| source_routed_hybrid | 0.223 | 0.387 | 0.547 | 0.747 | 0.953 | 0.497 | 0.507 |
| ifrs1115_subquery_hybrid | 0.233 | 0.397 | 0.557 | 0.767 | 0.973 | 0.517 | 0.524 |

Citation bucket summary:

| Retriever | hit@5 | hit@10 | hit@20 | beyond@20 | absent |
|---|---:|---:|---:|---:|---:|
| ifrs1115_subquery_hybrid | 46 | 18 | 16 | 0 | 2 |

Remaining misses:

- Q008 `1109-2.1`
- Q040 `1109-4.1.4`

## Gate Output

```text
ok: True
k: 20
baseline_recall@20: 0.767
ifrs1115_subquery_recall@20: 0.867
accepted_source_route:
  Q004: baseline_miss=[] target_miss=[]
  Q013: baseline_miss=[] target_miss=[]
  Q025: baseline_miss=[] target_miss=[]
  Q026: baseline_miss=[] target_miss=[]
  Q041: baseline_miss=[] target_miss=[]
recovered_1115:
  Q001: baseline_miss=[('1115', '27')] target_miss=[]
  Q006: baseline_miss=[('1115', '51')] target_miss=[]
seeded:
  Q029: baseline_miss=[] target_miss=[]
rejected:
  Q008: baseline_miss=[('1109', '2.1')] target_miss=[('1109', '2.1')]
  Q040: baseline_miss=[('1109', '4.1.4')] target_miss=[('1109', '4.1.4')]
```

## Decision

Keep `ifrs1115_subquery_hybrid` opt-in. It is still rule-triggered and should not replace the default retriever until
real usage shows the same pattern. The next RAG leaf should focus on Q008 cross-standard 1109 scope exclusion or Q040
1109 classification boundary.
