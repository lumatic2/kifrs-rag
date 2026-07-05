# WCE1 Coverage Gap Ranking

> Scope: rank the next accountant workflow candidate for workflow coverage expansion.

## 한 줄 결론

`1037_provisions` should be the next workflow contract: it is valuable to F-ACC/F-AUD, bounded enough for decision-prep output, and cheap to verify with existing evidence.

## Ranking Basis

| Criterion | Meaning |
|---|---|
| firm_service_value | clear accounting-firm team, workflow, and output fit |
| data_availability | can be exercised with public-safe or synthetic structured facts |
| determinism | can produce a bounded decision-prep draft without inventing facts |
| verification_cost_score | higher means cheaper to verify locally |

## Ranked Candidates

| Rank | Candidate | Service Line | Workflow | Output | Value | Data | Determinism | Verification | Total |
|---|---|---|---|---|---:|---:|---:|---:|---:|
| 1 | `1037_provisions` | F-ACC / F-AUD | provision recognition and measurement memo | decision-prep memo, journal-entry cue, human-review checklist | 5 | 4 | 5 | 5 | 19 |
| 2 | `disclosure_closing_support` | F-ACC / F-AUD | disclosure checklist and closing support pack | closing checklist, disclosure gap list, review questions | 5 | 5 | 4 | 4 | 18 |
| 3 | `1036_impairment` | F-ACC / F-AUD | impairment indicator and recoverable amount review memo | impairment trigger memo, missing-facts list, human-review checklist | 5 | 3 | 3 | 3 | 14 |
| 4 | `1113_fair_value` | F-ACC / F-DEAL | fair value hierarchy and input-level assessment memo | fair value classification memo and valuation input checklist | 5 | 3 | 3 | 2 | 13 |
| 5 | `1110_consolidation` | F-ACC | control assessment and consolidation scope memo | control indicators matrix, consolidation-scope memo, review checklist | 5 | 2 | 3 | 2 | 12 |

## Recommended Next Contract

- candidate: `1037_provisions`
- workflow: provision recognition and measurement memo
- output: decision-prep memo, journal-entry cue, human-review checklist
- reason: It is a high-value F-ACC/F-AUD workflow, has existing 1037 retrieval/eval evidence, is deterministic enough for a decision-prep memo, and can be verified without live private data.

## Candidate Limits

### 1037_provisions
- actual obligating event facts still need local structured input
- amount estimation remains human-reviewed unless provided as facts

### disclosure_closing_support
- partly overlaps existing review-pack surfaces
- full DART or company note parsing remains outside this milestone

### 1036_impairment
- valuation assumptions and cash-flow forecasts cannot be invented
- recoverable amount calculation needs external or client facts

### 1113_fair_value
- market data, model assumptions, and valuation technique selection need human review
- too much scope if DCF or option model validation is included now

### 1110_consolidation
- group structure, voting rights, contracts, and de facto control facts are fixture-heavy
- not enough current repo evidence for a fast first WCE implementation

## Boundaries Not Reopened

- external accountant outreach
- actual feedback capture
- real client document intake

## Machine Result

```json
{
  "title": "WCE1 Coverage Gap Ranking",
  "ok": true,
  "horizon": "workflow-coverage-expansion",
  "completed_milestone": "WCE1",
  "ranking_basis": {
    "firm_service_value": "clear accounting-firm team, workflow, and output fit",
    "data_availability": "can be exercised with public-safe or synthetic structured facts",
    "determinism": "can produce a bounded decision-prep draft without inventing facts",
    "verification_cost_score": "higher means cheaper to verify locally"
  },
  "ranked_candidates": [
    {
      "candidate_id": "1037_provisions",
      "service_line": "F-ACC / F-AUD",
      "workflow": "provision recognition and measurement memo",
      "output": "decision-prep memo, journal-entry cue, human-review checklist",
      "firm_service_value": 5,
      "data_availability": 4,
      "determinism": 5,
      "verification_cost_score": 5,
      "existing_evidence": [
        "docs/practice-map/team-workflows.md",
        "docs/reports/2026-07-05-rq2-eval-coverage-refresh.md",
        "docs/reports/2026-07-05-source-routed-hybrid-implementation.md"
      ],
      "limits": [
        "actual obligating event facts still need local structured input",
        "amount estimation remains human-reviewed unless provided as facts"
      ],
      "rank": 1,
      "total_score": 19
    },
    {
      "candidate_id": "disclosure_closing_support",
      "service_line": "F-ACC / F-AUD",
      "workflow": "disclosure checklist and closing support pack",
      "output": "closing checklist, disclosure gap list, review questions",
      "firm_service_value": 5,
      "data_availability": 5,
      "determinism": 4,
      "verification_cost_score": 4,
      "existing_evidence": [
        "docs/practice-map/service-line-candidates.md",
        "docs/reports/2026-07-04-ae2-disclosure-coverage.md",
        "docs/reports/demo-poc/statement-candidates.md"
      ],
      "limits": [
        "partly overlaps existing review-pack surfaces",
        "full DART or company note parsing remains outside this milestone"
      ],
      "rank": 2,
      "total_score": 18
    },
    {
      "candidate_id": "1036_impairment",
      "service_line": "F-ACC / F-AUD",
      "workflow": "impairment indicator and recoverable amount review memo",
      "output": "impairment trigger memo, missing-facts list, human-review checklist",
      "firm_service_value": 5,
      "data_availability": 3,
      "determinism": 3,
      "verification_cost_score": 3,
      "existing_evidence": [
        "docs/plans/2026-06-30-phase4-content-axis.md",
        "docs/reports/2026-07-05-rq2-eval-coverage-refresh.md",
        "docs/reports/2026-07-05-ro2-term-bridge-candidate-eval.md"
      ],
      "limits": [
        "valuation assumptions and cash-flow forecasts cannot be invented",
        "recoverable amount calculation needs external or client facts"
      ],
      "rank": 3,
      "total_score": 14
    },
    {
      "candidate_id": "1113_fair_value",
      "service_line": "F-ACC / F-DEAL",
      "workflow": "fair value hierarchy and input-level assessment memo",
      "output": "fair value classification memo and valuation input checklist",
      "firm_service_value": 5,
      "data_availability": 3,
      "determinism": 3,
      "verification_cost_score": 2,
      "existing_evidence": [
        "docs/plans/2026-06-30-p4c4-fair-value-entry.md",
        "docs/OBJECTIVE.md",
        "docs/practice-map/service-line-candidates.md"
      ],
      "limits": [
        "market data, model assumptions, and valuation technique selection need human review",
        "too much scope if DCF or option model validation is included now"
      ],
      "rank": 4,
      "total_score": 13
    },
    {
      "candidate_id": "1110_consolidation",
      "service_line": "F-ACC",
      "workflow": "control assessment and consolidation scope memo",
      "output": "control indicators matrix, consolidation-scope memo, review checklist",
      "firm_service_value": 5,
      "data_availability": 2,
      "determinism": 3,
      "verification_cost_score": 2,
      "existing_evidence": [
        "docs/practice-map/team-workflows.md",
        "docs/reports/2026-07-05-current-capability-map.md"
      ],
      "limits": [
        "group structure, voting rights, contracts, and de facto control facts are fixture-heavy",
        "not enough current repo evidence for a fast first WCE implementation"
      ],
      "rank": 5,
      "total_score": 12
    }
  ],
  "recommended_candidate": "1037_provisions",
  "recommended_next_contract": {
    "candidate_id": "1037_provisions",
    "workflow": "provision recognition and measurement memo",
    "output": "decision-prep memo, journal-entry cue, human-review checklist",
    "reason": "It is a high-value F-ACC/F-AUD workflow, has existing 1037 retrieval/eval evidence, is deterministic enough for a decision-prep memo, and can be verified without live private data."
  },
  "not_reopened": [
    "external accountant outreach",
    "actual feedback capture",
    "real client document intake"
  ],
  "report_path": "docs/reports/2026-07-05-wce1-coverage-gap-ranking.md"
}
```
