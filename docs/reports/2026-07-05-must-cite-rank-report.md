# Must-Cite Retrieval Rank Report

> Date: 2026-07-05
> Horizon: `docs/horizons/rag-optimization-resume.md`
> Command: `python scripts\retrieval_must_cite_report.py --retrievers hybrid --format markdown`

## Summary

This report changes the retrieval view from item-level pass/fail to citation-level rank buckets. A multi-citation
question can partly pass while one required paragraph is still missing; this view shows that gap directly.

| Retriever | Items | Required citations | hit@5 | hit@10 | hit@20 | beyond@20 | absent from returned K |
|---|---:|---:|---:|---:|---:|---:|---:|
| hybrid | 50 | 82 | 45 | 14 | 13 | 0 | 10 |

Interpretation:

- 72/82 required citations are now inside hybrid top-20.
- 10/82 required citations remain outside the returned top-20 list.
- `absent` here means "not returned within the requested K=20", not absent from the underlying standards DB.
- RO2 term bridge repair moved Q039 `1037-14` and Q048 `1036-18` into top-20, but both remain low-rank hits.

## Remaining Outside Top-20 Citations

| Item | Citation |
|---|---|
| Q001 | `1115-27` |
| Q004 | `1001-69` |
| Q006 | `1115-51` |
| Q008 | `1109-2.1` |
| Q013 | `1037-68` |
| Q025 | `1037-83` |
| Q026 | `1037-60` |
| Q029 | `1116-45` |
| Q040 | `1109-4.1.4` |
| Q041 | `1102-11` |

## Low-Rank But Recovered Citations

These citations are inside top-20 but not top-10, so answer-time retrieval can still be fragile when context budget is
tight or reranking changes.

| Item | Citation | Rank |
|---|---|---:|
| Q001 | `1115-22` | 20 |
| Q004 | `1001-73` | 15 |
| Q015 | `1109-5.5.17` | 12 |
| Q019 | `1019-109` | 11 |
| Q028 | `1116-44` | 13 |
| Q033 | `1109-4.1.1` | 12 |
| Q036 | `1109-4.1.5` | 12 |
| Q039 | `1037-14` | 16 |
| Q045 | `1115-38` | 14 |
| Q047 | `1116-62` | 18 |
| Q048 | `1036-18` | 17 |
| Q048 | `1036-59` | 14 |

## Next Use

Use this report to choose the next RAG improvement leaf:

- **source routing**: Q001/Q006/Q045 cluster around K-IFRS 1115 revenue recognition.
- **standard-specific routing**: Q008/Q040 cluster around K-IFRS 1109 classification/scope.
- **provision disclosure bridge**: Q013/Q025/Q026 cluster around K-IFRS 1037 disclosure/contingent items.
- **lease modification routing**: Q029 still misses K-IFRS 1116-45.
- **share-based payment routing**: Q041 still misses K-IFRS 1102-11.

The next implementation should not claim a full RAG quality upgrade from this report alone. It is a diagnostic layer
that makes future source routing or term bridge work measurable per citation.
