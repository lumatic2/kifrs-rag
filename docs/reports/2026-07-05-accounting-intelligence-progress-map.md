# Accounting Intelligence Progress Map

> Scope: plain-language objective/horizon/milestone position for continuing Accounting Intelligence work.

## One-Line Position

The research and workflow toolkit is broad enough for an internal demo; the active plan now continues through internal RAG, source, parser, and product hardening.

## Objective

Prove how far accountant work can be automated, then package that proof as a local toolkit for firm PoC.

## Current Horizon

- Horizon: `internal-capability-hardening`
- Status: active
- Goal: Harden the local accounting-intelligence toolkit without requiring external accountant outreach.

| Milestone | Name | Status |
|---|---|---|
| IH1 | plain progress map and decision queue | completed |
| IH2 | RAG quality re-validation and promotion criteria | candidate_next |
| IH3 | non-IFRS source data lanes and metadata connectors | candidate_next |
| IH4 | client-private parser/runtime hardening | candidate_next |
| IH5 | product demo surface and operator UX | candidate_next |

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

- decision: `select_internal_capability_horizon`
- command: `python scripts\accounting_intelligence_gap_audit.py --format text`

## Machine Result

```json
{
  "title": "Accounting Intelligence Progress Map",
  "objective": "Prove how far accountant work can be automated, then package that proof as a local toolkit for firm PoC.",
  "current_horizon": {
    "id": "internal-capability-hardening",
    "status": "active",
    "goal": "Harden the local accounting-intelligence toolkit without requiring external accountant outreach.",
    "milestones": [
      {
        "id": "IH1",
        "name": "plain progress map and decision queue",
        "status": "completed"
      },
      {
        "id": "IH2",
        "name": "RAG quality re-validation and promotion criteria",
        "status": "candidate_next"
      },
      {
        "id": "IH3",
        "name": "non-IFRS source data lanes and metadata connectors",
        "status": "candidate_next"
      },
      {
        "id": "IH4",
        "name": "client-private parser/runtime hardening",
        "status": "candidate_next"
      },
      {
        "id": "IH5",
        "name": "product demo surface and operator UX",
        "status": "candidate_next"
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
  "next_leaf": "select_internal_capability_horizon",
  "next_command": "python scripts\\accounting_intelligence_gap_audit.py --format text",
  "report_path": "docs/reports/2026-07-05-accounting-intelligence-progress-map.md"
}
```
