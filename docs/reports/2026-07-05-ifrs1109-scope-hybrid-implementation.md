# IFRS 1109 Scope Hybrid Implementation

> Date: 2026-07-05
> Horizon: `docs/horizons/rag-optimization-resume.md`
> Previous: `docs/reports/2026-07-05-ifrs1115-subquery-hybrid-implementation.md`

## Summary

Implemented opt-in `ifrs1109_scope_hybrid`. The default `hybrid` retriever remains unchanged.

Q008 is a cross-standard scope question: the 1116 lease measurement citations are already recovered, but the 1109
scope-exclusion citation is absent. RRF fusion recovered 1109 but displaced a required 1116 citation, so this retriever
uses a narrower insertion strategy: keep the `ifrs1115_subquery_hybrid` baseline order, insert the top 1109 scope result
after the first three baseline results, then continue the baseline list.

## Commands

```powershell
python scripts\ifrs1109_scope_gate.py --format text
python -m kifrs.eval.retrieval --k 20 --retrievers ifrs1115_subquery_hybrid ifrs1109_scope_hybrid --only Q008 Q040 --no-save
python -m kifrs.eval.retrieval --k 20 --retrievers ifrs1115_subquery_hybrid ifrs1109_scope_hybrid --no-save
python scripts\retrieval_must_cite_report.py --retrievers ifrs1109_scope_hybrid --format markdown
```

## Result

Focused remaining cluster:

| Retriever | recall@1 | recall@3 | recall@5 | recall@10 | recall@20 | MRR | nDCG@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ifrs1115_subquery_hybrid | 0.000 | 0.167 | 0.167 | 0.167 | 0.333 | 0.167 | 0.117 |
| ifrs1109_scope_hybrid | 0.000 | 0.167 | 0.333 | 0.333 | 0.500 | 0.167 | 0.218 |

Full 50-item retrieval-only eval:

| Retriever | recall@1 | recall@3 | recall@5 | recall@10 | recall@20 | MRR | nDCG@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ifrs1115_subquery_hybrid | 0.233 | 0.397 | 0.557 | 0.767 | 0.973 | 0.517 | 0.524 |
| ifrs1109_scope_hybrid | 0.233 | 0.397 | 0.563 | 0.773 | 0.980 | 0.517 | 0.528 |

Citation bucket summary:

| Retriever | hit@5 | hit@10 | hit@20 | beyond@20 | absent |
|---|---:|---:|---:|---:|---:|
| ifrs1109_scope_hybrid | 47 | 18 | 16 | 0 | 1 |

Remaining miss:

- Q040 `1109-4.1.4`

## Gate Output

```text
ok: True
k: 20
baseline_recall@20: 0.867
ifrs1109_scope_recall@20: 0.900
preserved:
  Q001: baseline_miss=[] target_miss=[]
  Q004: baseline_miss=[] target_miss=[]
  Q006: baseline_miss=[] target_miss=[]
  Q013: baseline_miss=[] target_miss=[]
  Q025: baseline_miss=[] target_miss=[]
  Q026: baseline_miss=[] target_miss=[]
  Q029: baseline_miss=[] target_miss=[]
  Q041: baseline_miss=[] target_miss=[]
recovered_scope:
  Q008: baseline_miss=[('1109', '2.1')] target_miss=[]
rejected:
  Q040: baseline_miss=[('1109', '4.1.4')] target_miss=[('1109', '4.1.4')]
```

## Decision

Keep `ifrs1109_scope_hybrid` opt-in. It is still rule-triggered and optimized for a reviewed cross-standard scope
pattern. The next RAG leaf should focus on Q040: either a narrow 1109 classification rerank or a K-boundary/gold strictness
review.
