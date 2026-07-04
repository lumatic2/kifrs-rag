# IFRS 1109 Classification Hybrid Implementation

> Date: 2026-07-05
> Horizon: `docs/horizons/rag-optimization-resume.md`
> Previous: `docs/reports/2026-07-05-ifrs1109-scope-hybrid-implementation.md`

## Summary

Implemented opt-in `ifrs1109_classification_hybrid`. The default `hybrid` retriever remains unchanged.

Q040 is a 1109 classification boundary question. The baseline was close, but the residual FVTPL classification paragraph
stayed outside top-20. The new retriever keeps `ifrs1109_scope_hybrid` as baseline and fuses one narrow 1109
classification subquery. This recovers the final remaining citation in the 50-item goldset.

## Commands

```powershell
python scripts\ifrs1109_classification_gate.py --format text
python -m kifrs.eval.retrieval --k 20 --retrievers ifrs1109_scope_hybrid ifrs1109_classification_hybrid --only Q040 --no-save
python -m kifrs.eval.retrieval --k 20 --retrievers ifrs1109_scope_hybrid ifrs1109_classification_hybrid --no-save
python scripts\retrieval_must_cite_report.py --retrievers ifrs1109_classification_hybrid --format markdown
```

## Result

Focused Q040:

| Retriever | recall@1 | recall@3 | recall@5 | recall@10 | recall@20 | MRR | nDCG@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ifrs1109_scope_hybrid | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| ifrs1109_classification_hybrid | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.200 | 0.387 |

Full 50-item retrieval-only eval:

| Retriever | recall@1 | recall@3 | recall@5 | recall@10 | recall@20 | MRR | nDCG@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ifrs1109_scope_hybrid | 0.233 | 0.397 | 0.563 | 0.773 | 0.980 | 0.517 | 0.528 |
| ifrs1109_classification_hybrid | 0.233 | 0.397 | 0.563 | 0.773 | 1.000 | 0.518 | 0.528 |

Citation bucket summary:

| Retriever | hit@5 | hit@10 | hit@20 | beyond@20 | absent |
|---|---:|---:|---:|---:|---:|
| ifrs1109_classification_hybrid | 47 | 18 | 17 | 0 | 0 |

## Gate Output

```text
ok: True
k: 20
baseline_recall@20: 0.900
ifrs1109_classification_recall@20: 1.000
preserved:
  Q001: baseline_miss=[] target_miss=[]
  Q004: baseline_miss=[] target_miss=[]
  Q006: baseline_miss=[] target_miss=[]
  Q008: baseline_miss=[] target_miss=[]
  Q013: baseline_miss=[] target_miss=[]
  Q025: baseline_miss=[] target_miss=[]
  Q026: baseline_miss=[] target_miss=[]
  Q029: baseline_miss=[] target_miss=[]
  Q041: baseline_miss=[] target_miss=[]
recovered_classification:
  Q040: baseline_miss=[('1109', '4.1.4')] target_miss=[]
```

## Decision

Keep `ifrs1109_classification_hybrid` opt-in. It achieves retrieval recall@20 1.000 on the 50-item goldset, but it is a
stack of reviewed, rule-triggered repair layers. The next step is a consolidated RAG quality close report and then
real-use validation before considering default retriever promotion.
