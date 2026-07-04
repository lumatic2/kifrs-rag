# Hard Miss Candidate Evaluation

> Date: 2026-07-05
> Horizon: `docs/horizons/rag-optimization-resume.md`
> Previous: `docs/reports/2026-07-05-source-routed-hybrid-implementation.md`
> Command: `python scripts\hard_miss_candidate_eval.py --format markdown`

## Summary

After `source_routed_hybrid`, five required citations still remain outside top-20:

- Q001 `1115-27`
- Q006 `1115-51`
- Q008 `1109-2.1`
- Q029 `1116-45`
- Q040 `1109-4.1.4`

This pass tested one narrow expansion candidate for each remaining hard miss without mutating `user_note_v2`.

Result: only Q029 is a seed candidate. The other four should not be promoted from this experiment.

## Result

| Item | Candidate | Target | Before | After | Decision |
|---|---|---|---:|---:|---|
| Q001 | `q001-distinct-performance-obligation` | `1115-27` | absent | 28 | reject |
| Q006 | `q006-variable-consideration-constraint` | `1115-51` | absent | absent | reject |
| Q008 | `q008-lease-liability-ifrs9-scope` | `1109-2.1` | absent | absent | reject |
| Q029 | `q029-lease-modification-decrease-scope` | `1116-45` | absent | 13 | candidate |
| Q040 | `q040-sppi-fail-fvtpl-classification` | `1109-4.1.4` | absent | 22 | reject |

Candidate means:

- the missing target citation moves into top-20, and
- existing top-20 required citations are preserved.

## Seed Candidate

| Standard | Paragraph | Type | Trigger | Expansion | Rationale |
|---|---|---|---|---|---|
| 1116 | 45 | term_bridge | 리스 범위 감소 | 리스변경 별도 리스 아님 리스 범위 감소 사용권자산 장부금액 감소 손익 인식 | Q029 misses the scope-decrease lease modification paragraph while already finding 1116-46. |

## Rejected Candidates

| Item | Reason |
|---|---|
| Q001 `1115-27` | Expansion improves nearby 1115-22 but target remains rank 28, outside top-20. |
| Q006 `1115-51` | Expansion still does not retrieve the target within the candidate pool. |
| Q008 `1109-2.1` | Expansion does not recover the target and loses existing 1116 citations. |
| Q040 `1109-4.1.4` | Expansion moves target to rank 22 only, outside top-20. |

## Decision

The next implementation leaf can safely promote only the Q029 bridge to reviewed `user_note_v2` seed, then re-run
focused retrieval. Q001/Q006/Q008/Q040 need a different approach: deeper query design, chunk/routing changes, or manual
review of whether the gold citation is overly strict for the question wording.
