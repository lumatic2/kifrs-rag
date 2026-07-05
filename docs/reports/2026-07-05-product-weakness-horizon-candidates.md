# Product Weakness Horizon Candidates

> Scope: product weakness based horizon queue for the next Accounting Intelligence work.

## Objective

Use the next five horizons to close the remaining product weaknesses before packaging or external PoC.

## Recommended Queue

| # | Horizon | Weakness Closed | Product Value | Status | First Milestone |
|---|---|---|---|---|---|
| 1 | `real-local-parser-prototype` | Local private inputs are still mostly represented by contracts and synthetic parser dry-runs. | Moves the toolkit toward realistic local-file handling while preserving structured-facts-only public output. | closed | RLP1 parser prototype asset inventory |
| 2 | `source-body-ingestion-controlled-lane` | K-IFRS-only evidence is insufficient for real accounting work that also needs interpretive, regulatory, legal, filing, and private facts. | Proves one non-IFRS source lane can be policy-bound, parsed, chunked, retrieved, and reported safely. | closed | SBI1 source class selection and authorization boundary |
| 3 | `workflow-coverage-expansion` | Automation proof is concentrated in a narrow set of standards and review-pack surfaces. | Expands the firm-service map into another testable accountant workflow and updates coverage evidence. | active | WCE1 coverage gap ranking |
| 4 | `runtime-retriever-promotion-gate` | The strongest retriever remains opt-in and has not been converted into a reversible product-default decision. | Creates a promote/defer/rollback gate for runtime retrieval quality. | planned | RPG1 promotion evidence inventory |
| 5 | `operator-experience-hardening` | The toolkit has many scripts and reports, but the operator path is difficult to discover and recover. | Turns the local toolkit into a run, diagnose, navigate, and recover experience. | planned | OEH1 operator command inventory |

## Parked

- `end-to-end-demo-scenario` — Should integrate the five horizons above instead of preceding them.
- `real-accountant-session` — User-owned external outreach remains parked until explicitly reopened.

## Decision

- `real-local-parser-prototype` is closed.
- `source-body-ingestion-controlled-lane` is closed.
- Keep `workflow-coverage-expansion` as the active horizon.
- Treat horizons 4 and 5 as the remaining product weakness queue after workflow coverage.
- Do not reopen actual outreach or feedback capture unless the user explicitly asks.

## Machine Result

```json
{
  "title": "Product Weakness Horizon Candidates",
  "objective": "Use the next five horizons to close the remaining product weaknesses before packaging or external PoC.",
  "active_horizon": "workflow-coverage-expansion",
  "candidates": [
    {
      "order": 1,
      "horizon_id": "real-local-parser-prototype",
      "weakness": "Local private inputs are still mostly represented by contracts and synthetic parser dry-runs.",
      "product_value": "Moves the toolkit toward realistic local-file handling while preserving structured-facts-only public output.",
      "status": "closed",
      "plan": "docs/plans/2026-07-05-real-local-parser-prototype.md",
      "first_milestone": "RLP1 parser prototype asset inventory"
    },
    {
      "order": 2,
      "horizon_id": "source-body-ingestion-controlled-lane",
      "weakness": "K-IFRS-only evidence is insufficient for real accounting work that also needs interpretive, regulatory, legal, filing, and private facts.",
      "product_value": "Proves one non-IFRS source lane can be policy-bound, parsed, chunked, retrieved, and reported safely.",
      "status": "closed",
      "plan": "docs/plans/2026-07-05-source-body-ingestion-controlled-lane.md",
      "first_milestone": "SBI1 source class selection and authorization boundary"
    },
    {
      "order": 3,
      "horizon_id": "workflow-coverage-expansion",
      "weakness": "Automation proof is concentrated in a narrow set of standards and review-pack surfaces.",
      "product_value": "Expands the firm-service map into another testable accountant workflow and updates coverage evidence.",
      "status": "active",
      "plan": "docs/plans/2026-07-05-workflow-coverage-expansion.md",
      "first_milestone": "WCE1 coverage gap ranking"
    },
    {
      "order": 4,
      "horizon_id": "runtime-retriever-promotion-gate",
      "weakness": "The strongest retriever remains opt-in and has not been converted into a reversible product-default decision.",
      "product_value": "Creates a promote/defer/rollback gate for runtime retrieval quality.",
      "status": "planned",
      "plan": "docs/plans/2026-07-05-runtime-retriever-promotion-gate.md",
      "first_milestone": "RPG1 promotion evidence inventory"
    },
    {
      "order": 5,
      "horizon_id": "operator-experience-hardening",
      "weakness": "The toolkit has many scripts and reports, but the operator path is difficult to discover and recover.",
      "product_value": "Turns the local toolkit into a run, diagnose, navigate, and recover experience.",
      "status": "planned",
      "plan": "docs/plans/2026-07-05-operator-experience-hardening.md",
      "first_milestone": "OEH1 operator command inventory"
    }
  ],
  "parked": [
    {
      "horizon_id": "end-to-end-demo-scenario",
      "reason": "Should integrate the five horizons above instead of preceding them."
    },
    {
      "horizon_id": "real-accountant-session",
      "reason": "User-owned external outreach remains parked until explicitly reopened."
    }
  ],
  "report_path": "docs/reports/2026-07-05-product-weakness-horizon-candidates.md"
}
```
