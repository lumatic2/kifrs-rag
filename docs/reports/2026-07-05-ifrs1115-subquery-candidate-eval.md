# IFRS 1115 Subquery Candidate Evaluation

> Date: 2026-07-05
> Horizon: `docs/horizons/rag-optimization-resume.md`
> Previous: `docs/reports/2026-07-05-remaining-hard-miss-triage.md`
> Command: `python scripts\ifrs1115_subquery_candidate_eval.py --format markdown`

## Summary

Q001 and Q006 are both 1115 misses where the baseline already recovers one required citation but misses the paired
concept paragraph. This experiment keeps the baseline `source_routed_hybrid` results and fuses a focused 1115 subquery
with weight 2. It does not mutate the default retriever.

| Item | Candidate | Target | Before | After | Decision |
|---|---|---|---:|---:|---|
| Q001 | `q001-performance-obligation-criteria` | `1115-27` | absent | 15 | candidate |
| Q006 | `q006-variable-consideration-refund` | `1115-51` | absent | 7 | candidate |

## Detail

### q001-performance-obligation-criteria

- Subquery: `고객 효익 쉽게 구할 수 있는 다른 자원 별도 식별 계약 내 다른 약속 구별`
- Baseline ranks: `{"1115-22": 20, "1115-27": null}`
- Subquery-only ranks: `{"1115-22": 4, "1115-27": 1}`
- Fused ranks: `{"1115-22": 4, "1115-27": 15}`
- Preserves existing hits: `True`

### q006-variable-consideration-refund

- Subquery: `리베이트 환불 가격할인 변동대가 미래 사건 거래가격 환불부채`
- Baseline ranks: `{"1115-51": null, "1115-55": 5}`
- Subquery-only ranks: `{"1115-51": 1, "1115-55": 2}`
- Fused ranks: `{"1115-51": 7, "1115-55": 1}`
- Preserves existing hits: `True`

## Decision

Promote this only to the next implementation candidate, not to default runtime yet. The next leaf should be an opt-in
1115 subquery retriever or a source-aware query decomposition policy with a regression gate proving Q001/Q006 recover
without losing the current accepted route, Q029 seed, or rejected-hard-miss boundaries.
