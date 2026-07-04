# Remaining Hard Miss Triage

> Date: 2026-07-05
> Horizon: `docs/horizons/rag-optimization-resume.md`
> Previous: `docs/reports/2026-07-05-hard-miss-candidate-eval.md`
> Command: `python scripts\remaining_hard_miss_triage.py --format markdown`

## Summary

After the Q029 reviewed seed, `source_routed_hybrid` still misses four required citations at K=20.

| Item | Miss | Existing hit | Candidate after | Decision | Classification |
|---|---|---|---:|---|---|
| Q001 | `1115-27` | `1115-22` | 28 | reject | `near_miss_candidate_pool` |
| Q006 | `1115-51` | `1115-55` | absent | reject | `concept_gap` |
| Q008 | `1109-2.1` | `1116-22`, `1116-26` | absent | reject | `cross_standard_scope_gap` |
| Q040 | `1109-4.1.4` | - | 22 | reject | `k_boundary_near_miss` |

## Triage

### Q001

- Gold ranks: `{"1115-22": 20, "1115-27": null}`
- Candidate: `q001-distinct-performance-obligation` -> `reject`
- Finding: 1115-22 is recovered but 1115-27 stays just outside the gate after expansion.
- Next action: Do not add a one-off seed yet; test a 1115 performance-obligation subquery or rerank rule.

### Q006

- Gold ranks: `{"1115-51": null, "1115-55": 5}`
- Candidate: `q006-variable-consideration-constraint` -> `reject`
- Finding: 1115-55 is recovered but 1115-51 remains absent even with the variable-consideration expansion.
- Next action: Rework query design around variable consideration and refund liability rather than adding the rejected seed.

### Q008

- Gold ranks: `{"1109-2.1": null, "1116-22": 3, "1116-26": 17}`
- Candidate: `q008-lease-liability-ifrs9-scope` -> `reject`
- Finding: 1116 lease measurement citations are recovered but the 1109 scope exclusion remains absent.
- Next action: Handle as cross-standard decomposition: ask a separate 1109 scope-exclusion subquery while preserving 1116 hits.

### Q040

- Gold ranks: `{"1109-4.1.4": null}`
- Candidate: `q040-sppi-fail-fvtpl-classification` -> `reject`
- Finding: 1109-4.1.4 moves near top-20 but does not enter the gate.
- Next action: Review whether K=20 is the right gate for this citation or test a narrow 1109 classification reranker.

## Decision

Do not add more reviewed `user_note_v2` seeds from this pass. The next useful implementation candidates are:

1. a 1115-focused performance-obligation/variable-consideration subquery experiment for Q001/Q006,
2. a cross-standard scope-exclusion decomposition experiment for Q008,
3. a narrow 1109 classification rerank/K-boundary experiment for Q040.
