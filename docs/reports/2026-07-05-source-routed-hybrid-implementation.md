# Source Routed Hybrid Implementation

> Date: 2026-07-05
> Horizon: `docs/horizons/rag-optimization-resume.md`
> Previous: `docs/reports/2026-07-05-source-routing-candidate-eval.md`

## Summary

Implemented an opt-in `source_routed_hybrid` retriever for the accepted source-routing clusters only. The default
`hybrid` retriever is unchanged.

Accepted routes:

| Route | Trigger scope | Recovered items |
|---|---|---|
| `1001` | borrowing/current-vs-non-current classification wording | Q004 `1001-69` |
| `1037` | provision plus onerous contract/disposal gain/present value/unwinding wording | Q013 `1037-68`, Q025 `1037-83`, Q026 `1037-60` |
| `1102` | equity-settled share-based payment/measurement-date wording | Q041 `1102-11` |

Rejected clusters from the prior experiment are intentionally not routed.

## Commands

Focused accepted-cluster check:

```powershell
python -m kifrs.eval.retrieval --k 20 --retrievers hybrid source_routed_hybrid --only Q004 Q013 Q025 Q026 Q041 --no-save
```

Rejected-cluster preservation check:

```powershell
python -m kifrs.eval.retrieval --k 20 --retrievers hybrid source_routed_hybrid --only Q008 Q001 Q006 Q029 Q040 --no-save
```

Regression gate:

```powershell
python scripts\source_routed_hybrid_gate.py --format text
```

## Result

Focused accepted cluster:

| Retriever | recall@1 | recall@3 | recall@5 | recall@10 | recall@20 | MRR | nDCG@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| hybrid | 0.000 | 0.267 | 0.267 | 0.267 | 0.333 | 0.300 | 0.214 |
| source_routed_hybrid | 0.267 | 0.267 | 0.267 | 0.600 | 1.000 | 0.633 | 0.460 |

Rejected cluster:

| Retriever | recall@1 | recall@3 | recall@5 | recall@10 | recall@20 | MRR | nDCG@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| hybrid | 0.000 | 0.167 | 0.267 | 0.267 | 0.433 | 0.217 | 0.172 |
| source_routed_hybrid | 0.000 | 0.167 | 0.267 | 0.267 | 0.433 | 0.217 | 0.172 |

Full 50-item retrieval-only eval:

| Retriever | recall@1 | recall@3 | recall@5 | recall@10 | recall@20 | MRR | nDCG@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| hybrid | 0.187 | 0.387 | 0.547 | 0.713 | 0.877 | 0.454 | 0.478 |
| source_routed_hybrid | 0.213 | 0.387 | 0.547 | 0.747 | 0.943 | 0.487 | 0.502 |

Citation bucket summary:

| Retriever | hit@5 | hit@10 | hit@20 | beyond@20 | absent |
|---|---:|---:|---:|---:|---:|
| source_routed_hybrid | 45 | 17 | 15 | 0 | 5 |

## Gate Output

```text
ok: True
k: 20
baseline_recall@20: 0.383
source_routed_recall@20: 0.717
accepted:
  Q004: baseline_miss=[('1001', '69')] routed_miss=[]
  Q013: baseline_miss=[('1037', '68')] routed_miss=[]
  Q025: baseline_miss=[('1037', '83')] routed_miss=[]
  Q026: baseline_miss=[('1037', '60')] routed_miss=[]
  Q041: baseline_miss=[('1102', '11')] routed_miss=[]
rejected:
  Q001: baseline_miss=[('1115', '27')] routed_miss=[('1115', '27')]
  Q006: baseline_miss=[('1115', '51')] routed_miss=[('1115', '51')]
  Q008: baseline_miss=[('1109', '2.1')] routed_miss=[('1109', '2.1')]
  Q029: baseline_miss=[('1116', '45')] routed_miss=[('1116', '45')]
  Q040: baseline_miss=[('1109', '4.1.4')] routed_miss=[('1109', '4.1.4')]
```

## Decision

Keep `source_routed_hybrid` opt-in for now. It improves the evaluation set, but it is still rule-triggered and needs
more real usage before becoming the default retriever. The remaining hard misses are Q001, Q006, Q008, Q029, and Q040.
