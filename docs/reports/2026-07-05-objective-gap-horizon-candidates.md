# Objective Gap Horizon Candidates

> Scope: post-demo horizon queue derived from the current Objective gap audit.

## Objective

Group the remaining objective gaps into implementation horizons and run them with the product harness.

## Excluded From This Plan

- external accountant feedback remains parked until explicitly reintroduced

## Recommended Horizon Queue

| # | Horizon | Objective Gap | Why Now | Status | First Milestone | Evidence Target |
|---:|---|---|---|---|---|---|
| 1 | `rag-quality-fresh-validation` | Default retrieval quality is still deferred; the strongest retriever is not yet trusted as a product default. | Every accountant-facing workflow depends on retrieval trust, so this should run before deeper source/parser expansion. | closed | RQF1 validation corpus and acceptance contract | `docs/reports/2026-07-05-rqf1-validation-contract.md` |
| 2 | `private-parser-realism-hardening` | Local parser evidence is still fixture-heavy; actual local-file adapter evidence remains gated by explicit authorization. | The objective needs realistic client-input handling, but protected payloads must stay local and authorization-gated. | closed | PPR1 authorization-safe adapter proof plan | `docs/reports/2026-07-05-ppr1-authorization-safe-adapter-proof.md` |
| 3 | `external-source-body-connector-expansion` | External sources have metadata/demo evidence, but broader source-body connector implementation is still missing. | Accounting work needs regulator, interpretive, legal, filing, and policy evidence beyond K-IFRS paragraphs. | active | ESB1 source-body connector selection and policy gate | `docs/reports/2026-07-05-esb1-source-body-connector-selection.md` |
| 4 | `workflow-coverage-depth-expansion` | Automation coverage is strong in selected workflows but still shallow against the full firm-service map. | The north-star question asks how far accountant work can be automated, which requires broader workflow sampling. | pending | WCD1 service-line coverage rerank | `docs/reports/2026-07-05-wcd1-service-line-coverage-rerank.md` |
| 5 | `demo-rehearsal-quality-loop` | The demo packet is ready, but it has not been rehearsed into repeatable operator evidence and quality notes. | Before any external step, the local demo needs timed, repeatable, failure-aware rehearsal evidence. | pending | DRQ1 demo rehearsal script and timing gate | `docs/reports/2026-07-05-drq1-demo-rehearsal-script.md` |

## Decision

- Active horizon: `external-source-body-connector-expansion`
- Run horizons in order unless a later gap becomes objectively blocking.
- Do not add external feedback work to this queue without explicit user instruction.

## Machine Result

```json
{
  "title": "Objective Gap Horizon Candidates",
  "objective": "Group the remaining objective gaps into implementation horizons and run them with the product harness.",
  "excluded_from_plan": [
    "external accountant feedback remains parked until explicitly reintroduced"
  ],
  "active_horizon": "external-source-body-connector-expansion",
  "candidates": [
    {
      "order": 1,
      "horizon_id": "rag-quality-fresh-validation",
      "objective_gap": "Default retrieval quality is still deferred; the strongest retriever is not yet trusted as a product default.",
      "why_now": "Every accountant-facing workflow depends on retrieval trust, so this should run before deeper source/parser expansion.",
      "status": "closed",
      "first_milestone": "RQF1 validation corpus and acceptance contract",
      "evidence_target": "docs/reports/2026-07-05-rqf1-validation-contract.md"
    },
    {
      "order": 2,
      "horizon_id": "private-parser-realism-hardening",
      "objective_gap": "Local parser evidence is still fixture-heavy; actual local-file adapter evidence remains gated by explicit authorization.",
      "why_now": "The objective needs realistic client-input handling, but protected payloads must stay local and authorization-gated.",
      "status": "closed",
      "first_milestone": "PPR1 authorization-safe adapter proof plan",
      "evidence_target": "docs/reports/2026-07-05-ppr1-authorization-safe-adapter-proof.md"
    },
    {
      "order": 3,
      "horizon_id": "external-source-body-connector-expansion",
      "objective_gap": "External sources have metadata/demo evidence, but broader source-body connector implementation is still missing.",
      "why_now": "Accounting work needs regulator, interpretive, legal, filing, and policy evidence beyond K-IFRS paragraphs.",
      "status": "active",
      "first_milestone": "ESB1 source-body connector selection and policy gate",
      "evidence_target": "docs/reports/2026-07-05-esb1-source-body-connector-selection.md"
    },
    {
      "order": 4,
      "horizon_id": "workflow-coverage-depth-expansion",
      "objective_gap": "Automation coverage is strong in selected workflows but still shallow against the full firm-service map.",
      "why_now": "The north-star question asks how far accountant work can be automated, which requires broader workflow sampling.",
      "status": "pending",
      "first_milestone": "WCD1 service-line coverage rerank",
      "evidence_target": "docs/reports/2026-07-05-wcd1-service-line-coverage-rerank.md"
    },
    {
      "order": 5,
      "horizon_id": "demo-rehearsal-quality-loop",
      "objective_gap": "The demo packet is ready, but it has not been rehearsed into repeatable operator evidence and quality notes.",
      "why_now": "Before any external step, the local demo needs timed, repeatable, failure-aware rehearsal evidence.",
      "status": "pending",
      "first_milestone": "DRQ1 demo rehearsal script and timing gate",
      "evidence_target": "docs/reports/2026-07-05-drq1-demo-rehearsal-script.md"
    }
  ],
  "report_path": "docs/reports/2026-07-05-objective-gap-horizon-candidates.md"
}
```
