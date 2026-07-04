# RO2 Multi-Query Retrieval Experiment

> Date: 2026-07-05
> Horizon: `docs/horizons/rag-optimization-resume.md`
> Scope: category C deep miss cases from RO1, Q039/Q048 only

## Summary

RO2 tested whether cross-concept questions improve when one question is split into multiple hybrid-search
subqueries and the results are fused with RRF.

Result: **not promoted**. The experimental retriever did not recover the remaining missed citations and lowered
ranking quality on the focused Q039/Q048 check.

## What Changed

`kifrs.eval.retrieval` now exposes an experimental retriever:

```powershell
python -m kifrs.eval.retrieval --k 20 --retrievers multi_query_hybrid --only Q039 Q048 --no-save
```

It is intentionally opt-in. Existing retrievers are unchanged.

The experiment does four things:

1. keeps the original query,
2. adds literal cross-concept phrases from the question,
3. adds small concept expansions for terms such as `충당부채`, `회수가능액`, and `손상차손`,
4. fuses hybrid results with reciprocal rank fusion while preserving original-query weight.

## Focused Result

Command:

```powershell
python -m kifrs.eval.retrieval --k 20 --retrievers hybrid multi_query_hybrid --only Q039 Q048 --no-save
```

Observed result:

| Retriever | recall@1 | recall@3 | recall@5 | recall@10 | recall@20 | MRR | nDCG@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| hybrid | 0.000 | 0.250 | 0.500 | 0.500 | 0.500 | 0.350 | 0.312 |
| multi_query_hybrid | 0.000 | 0.000 | 0.250 | 0.500 | 0.500 | 0.175 | 0.221 |

Misses remained:

| Item | hybrid miss | multi_query_hybrid miss |
|---|---|---|
| Q039 | `1037-14` | `1037-14` |
| Q048 | `1036-18` | `1036-18` |

## Interpretation

The simple multi-query approach did not fix the category C miss. It can dilute ranking quality because subqueries
add plausible but competing candidates. This suggests that the next useful improvement is not a generic
split-and-fuse retriever.

Better next candidates:

1. move concept expansions into reviewed `user_note_v2` term bridges rather than hardcoded eval variants,
2. add structured source routing for cross-standard questions,
3. evaluate per-must-cite retrieval, not only item-level query text,
4. keep `multi_query_hybrid` opt-in for experiments only.

## Verification

```powershell
python -m pytest tests\test_eval_retrieval.py -q
python -m kifrs.eval.retrieval --k 20 --retrievers hybrid multi_query_hybrid --only Q039 Q048 --no-save
```
