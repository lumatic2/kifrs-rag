# Accounting Intelligence Progress Map

> Scope: plain-language objective/horizon/milestone position for continuing Accounting Intelligence work.

## One-Line Position

The next active horizon is RAG reliability revalidation: prove the K-IFRS retrieval and citation baseline before source expansion or product hardening.

## Objective

Prove how far accountant work can be automated, then package that proof as a local toolkit for firm PoC.

## Current Horizon

- Horizon: `rag-reliability-revalidation`
- Status: active
- Goal: Re-validate K-IFRS RAG quality and define retriever promotion criteria before expanding sources or product UX.

| Milestone | Name | Status |
|---|---|---|
| RR1 | baseline inventory | completed |
| RR2 | eval matrix and seed coverage | completed |
| RR3 | retrieval and citation diagnostics | active_next |
| RR4 | repair policy candidate | pending |
| RR5 | promotion gate and handoff | pending |

## Completed Capability Chain

| Horizon | Result | Evidence |
|---|---|---|
| firm-service-map | Mapped accounting firm teams and selected F-ACC/accounting advisory as the first product lane. | `docs/horizons/firm-service-map.md` |
| F-ACC sequence | Turned the firm-service map into review-pack workflow sequence candidates. | `BACKLOG.md` |
| rag-quality-refresh | Built an opt-in repair retriever stack that reaches 50-item recall@20 1.000 without default promotion. | `docs/reports/2026-07-05-rag-quality-refresh-close-report.md` |
| authority-source-map | Separated K-IFRS, regulator, disclosure, law, and private-client source lanes with storage boundaries. | `docs/reports/2026-07-05-authority-source-map-close-report.md` |
| client-private intake/local parser | Defined local-only private intake, redaction, parser dry-run, deletion attestation, and adapter plan boundaries. | `docs/reports/2026-07-05-local-parser-real-adapter-implementation-plan.md` |
| field-feedback runbook/capture | Prepared a 30-minute feedback session flow and safe feedback capture/queue conversion pipeline. | `docs/reports/2026-07-05-fc4-field-feedback-capture-close-report.md` |

## Automation Snapshot

- Review packs: 24
- Automated packs: 20
- Human-review packs: 4
- Automation rate: 83.33%

## Open Decisions

| Decision | Status | Blocker | Command |
|---|---|---|---|
| None | none | none | `none` |
| approve_default_retriever_promotion | deferred_until_eval_evidence_and_authorization | stronger evaluation evidence and explicit authorization are missing | `python scripts\default_retriever_guard.py --format text` |

## Remaining Gaps

- external accountant feedback is parked by user request and excluded from the active plan until explicitly reintroduced
- RAG quality needs a fresh internal validation horizon before any default retriever promotion
- local parser real-adapter implementation plan is present, but actual evidence and explicit authorization are still required before real upload/OCR/parser/deletion automation
- external source connector metadata-only lane is closed and demo-noted; authorization record scaffold is present, but source-body connector is still not implemented
- opt-in retriever promotion decision gate and default retriever guard are present, but default retriever change remains deferred until stronger evaluation evidence and explicit authorization
- firm-facing brief and toolkit packaging docs exist, but the repo is still closer to an internal toolkit than a finished user-facing product

## Next Leaf

- decision: `RR3_retrieval_and_citation_diagnostics`
- command: `python scripts\quality_preflight.py --format text`

## Machine Result

```json
{
  "title": "Accounting Intelligence Progress Map",
  "objective": "Prove how far accountant work can be automated, then package that proof as a local toolkit for firm PoC.",
  "current_horizon": {
    "id": "rag-reliability-revalidation",
    "status": "active",
    "goal": "Re-validate K-IFRS RAG quality and define retriever promotion criteria before expanding sources or product UX.",
    "milestones": [
      {
        "id": "RR1",
        "name": "baseline inventory",
        "status": "completed"
      },
      {
        "id": "RR2",
        "name": "eval matrix and seed coverage",
        "status": "completed"
      },
      {
        "id": "RR3",
        "name": "retrieval and citation diagnostics",
        "status": "active_next"
      },
      {
        "id": "RR4",
        "name": "repair policy candidate",
        "status": "pending"
      },
      {
        "id": "RR5",
        "name": "promotion gate and handoff",
        "status": "pending"
      }
    ]
  },
  "completed_horizons": [
    {
      "id": "firm-service-map",
      "result": "Mapped accounting firm teams and selected F-ACC/accounting advisory as the first product lane.",
      "evidence": "docs/horizons/firm-service-map.md"
    },
    {
      "id": "F-ACC sequence",
      "result": "Turned the firm-service map into review-pack workflow sequence candidates.",
      "evidence": "BACKLOG.md"
    },
    {
      "id": "rag-quality-refresh",
      "result": "Built an opt-in repair retriever stack that reaches 50-item recall@20 1.000 without default promotion.",
      "evidence": "docs/reports/2026-07-05-rag-quality-refresh-close-report.md"
    },
    {
      "id": "authority-source-map",
      "result": "Separated K-IFRS, regulator, disclosure, law, and private-client source lanes with storage boundaries.",
      "evidence": "docs/reports/2026-07-05-authority-source-map-close-report.md"
    },
    {
      "id": "client-private intake/local parser",
      "result": "Defined local-only private intake, redaction, parser dry-run, deletion attestation, and adapter plan boundaries.",
      "evidence": "docs/reports/2026-07-05-local-parser-real-adapter-implementation-plan.md"
    },
    {
      "id": "field-feedback runbook/capture",
      "result": "Prepared a 30-minute feedback session flow and safe feedback capture/queue conversion pipeline.",
      "evidence": "docs/reports/2026-07-05-fc4-field-feedback-capture-close-report.md"
    }
  ],
  "open_decisions": [
    {
      "id": null,
      "status": "none",
      "decide": "No user-owned decision is currently required.",
      "blocker": "none",
      "command": "none"
    },
    {
      "id": "approve_default_retriever_promotion",
      "status": "deferred_until_eval_evidence_and_authorization",
      "decide": "Promote the opt-in repair retriever to default only after stronger evaluation evidence and explicit authorization.",
      "blocker": "stronger evaluation evidence and explicit authorization are missing",
      "command": "python scripts\\default_retriever_guard.py --format text"
    }
  ],
  "automation_snapshot": {
    "review_packs": 24,
    "automated_packs": 20,
    "human_review_packs": 4,
    "automation_rate": 0.8333
  },
  "remaining_gaps": [
    "external accountant feedback is parked by user request and excluded from the active plan until explicitly reintroduced",
    "RAG quality needs a fresh internal validation horizon before any default retriever promotion",
    "local parser real-adapter implementation plan is present, but actual evidence and explicit authorization are still required before real upload/OCR/parser/deletion automation",
    "external source connector metadata-only lane is closed and demo-noted; authorization record scaffold is present, but source-body connector is still not implemented",
    "opt-in retriever promotion decision gate and default retriever guard are present, but default retriever change remains deferred until stronger evaluation evidence and explicit authorization",
    "firm-facing brief and toolkit packaging docs exist, but the repo is still closer to an internal toolkit than a finished user-facing product"
  ],
  "next_leaf": "RR3_retrieval_and_citation_diagnostics",
  "next_command": "python scripts\\quality_preflight.py --format text",
  "report_path": "docs/reports/2026-07-05-accounting-intelligence-progress-map.md"
}
```
