# RO2 Term Bridge Candidate Evaluation

> Date: 2026-07-05
> Horizon: `docs/horizons/rag-optimization-resume.md`
> Previous: `docs/reports/2026-07-05-ro2-multi-query-experiment.md`

## Summary

After the generic multi-query experiment failed to improve Q039/Q048, this pass tested reviewed term bridge
candidates without mutating `user_note_v2`.

Result: two candidates are worth promoting to reviewed seed candidates; two should be rejected.

## Command

```powershell
python scripts\term_bridge_candidate_eval.py --format markdown
```

## Result

| Item | Candidate | Target | Before | After | Decision |
|---|---|---|---:|---:|---|
| Q039 | `q039-provision-recognition` | `1037-14` | absent | 16 | candidate |
| Q039 | `q039-restoration-provision` | `1037-14` | absent | 44 | reject |
| Q048 | `q048-recoverable-amount-definition` | `1036-18` | absent | 13 | reject |
| Q048 | `q048-impairment-recoverable` | `1036-18` | absent | 17 | candidate |

Candidate means:

- the missing target citation moves into top-20, and
- existing top-20 required citations are preserved.

## Seed Candidates

These are not applied to the DB yet. They are candidates for a later reviewed `user_note_v2` seed change.

| Standard | Paragraph | Type | Trigger | Expansion | Rationale |
|---|---|---|---|---|---|
| 1037 | 14 | term_bridge | 충당부채 | 현재의무 과거사건 자원 유출 가능성 신뢰성 있는 추정 | Q039 misses 1037-14 because the original lease-focused question does not include provision recognition criteria terms. |
| 1036 | 18 | term_bridge | 손상차손 | 회수가능액 순공정가치 사용가치 | Q048 misses 1036-18 while already finding 1036-59; this bridge recovers 1036-18 and keeps 1036-59 in top-20. |

## Rejected Candidates

| Candidate | Reason |
|---|---|
| `q039-restoration-provision` | target citation only reaches rank 44, outside the top-20 gate |
| `q048-recoverable-amount-definition` | recovers 1036-18 but loses existing 1036-59 hit |

## Next Step

Create a reviewed seed change only for the two seed candidates, then rerun:

```powershell
python scripts\seed_user_notes.py --apply
python -m kifrs.eval.retrieval --k 20 --retrievers hybrid --only Q039 Q048 --no-save
python scripts\quality_preflight.py --format text
```
