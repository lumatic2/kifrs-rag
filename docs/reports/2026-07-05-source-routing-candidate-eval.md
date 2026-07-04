# Source Routing Candidate Evaluation

> Date: 2026-07-05
> Horizon: `docs/horizons/rag-optimization-resume.md`
> Input: `docs/reports/2026-07-05-must-cite-rank-report.md`
> Command: `python scripts\source_routing_candidate_eval.py --format markdown`

## Summary

This experiment tested whether supplemental standard routing can recover the 10 required citations that were outside
hybrid top-20. It does **not** change runtime retrieval. It tests a candidate strategy:

1. run current hybrid retrieval,
2. run an additional hybrid query restricted to the target standard,
3. fuse both result sets with RRF,
4. accept only if the missing target enters top-20 and existing top-20 required citations are preserved.

Result: 5/10 are candidates for a future supplemental source-routing retriever. The rest need term bridges, better
query expansion, chunking, or a different routing strategy.

## Result

| Item | Route | Target | Before | Routed | Fused | Decision |
|---|---|---|---:|---:|---:|---|
| Q001 | `1115` | `1115-27` | absent | absent | absent | reject |
| Q004 | `1001` | `1001-69` | 31 | 6 | 10 | candidate |
| Q006 | `1115` | `1115-51` | absent | absent | absent | reject |
| Q008 | `1109` | `1109-2.1` | absent | absent | absent | reject |
| Q013 | `1037` | `1037-68` | 28 | 16 | 14 | candidate |
| Q025 | `1037` | `1037-83` | 35 | 16 | 18 | candidate |
| Q026 | `1037` | `1037-60` | 25 | 5 | 9 | candidate |
| Q029 | `1116` | `1116-45` | absent | 28 | absent | reject |
| Q040 | `1109` | `1109-4.1.4` | absent | absent | absent | reject |
| Q041 | `1102` | `1102-11` | 22 | 13 | 13 | candidate |

## Candidate Group

These are plausible for a future supplemental routing implementation:

| Cluster | Items | Why |
|---|---|---|
| Current liability classification | Q004 `1001-69` | Standard routing lifts the target to fused rank 10 while preserving `1001-72` and `1001-73`. |
| Provision disclosure/measurement | Q013 `1037-68`, Q025 `1037-83`, Q026 `1037-60` | K-IFRS 1037 routing recovers all three missed provision citations into top-20. |
| Share-based payment vesting | Q041 `1102-11` | K-IFRS 1102 routing moves the target from rank 22 to fused rank 13 while preserving `1102-10`. |

## Rejected Group

These should not be treated as source-routing wins:

| Cluster | Items | Reason |
|---|---|---|
| Revenue recognition | Q001 `1115-27`, Q006 `1115-51` | Restricting to K-IFRS 1115 still does not retrieve the target within the candidate pool. |
| Financial instruments scope/classification | Q008 `1109-2.1`, Q040 `1109-4.1.4` | K-IFRS 1109 routing still misses the target. Q008 also loses a lease citation under fused top-20. |
| Lease modification | Q029 `1116-45` | K-IFRS 1116 routing finds the target only at rank 28; fusion still leaves it outside top-20. |

## Decision

Do not promote source routing into the default retriever yet. The experiment is useful but partial:

- source routing looks promising for K-IFRS 1001, 1037, and 1102 misses;
- it does not solve the hard 1115/1109/1116 misses;
- implementation should be supplemental and evidence-gated, not a blanket standard filter.

The next implementation candidate is a narrow supplemental routing retriever or gate limited to accepted candidate
clusters, with Q008-style cross-standard preservation as a required failure-mode test.
