# Accounting Intelligence Progress Map

> Scope: plain-language objective/horizon/milestone position for continuing Accounting Intelligence work.

## One-Line Position

The active horizon is non-IFRS source dataization: turn non-IFRS source lanes into public-safe RAG dataization units.

## Objective

Prove how far accountant work can be automated, then package that proof as a local toolkit for firm PoC.

## Current Horizon

- Horizon: `non-ifrs-source-dataization`
- Status: active
- Goal: Turn KASB/FSS, law, DART, and client-private source lanes into public-safe RAG dataization units.

| Milestone | Name | Status |
|---|---|---|
| NIS1 | existing source asset inventory | active_next |
| NIS2 | source record contract | pending |
| NIS3 | dataization fixtures and validators | pending |
| NIS4 | chunking and embedding policy | pending |
| NIS5 | dataization gate and runtime handoff | pending |

## Completed Capability Chain

| Horizon | Result | Evidence |
|---|---|---|
| firm-service-map | Mapped accounting firm teams and selected F-ACC/accounting advisory as the first product lane. | `docs/horizons/firm-service-map.md` |
| F-ACC sequence | Turned the firm-service map into review-pack workflow sequence candidates. | `BACKLOG.md` |
| rag-quality-refresh | Built an opt-in repair retriever stack that reaches 50-item recall@20 1.000 without default promotion. | `docs/reports/2026-07-05-rag-quality-refresh-close-report.md` |
| authority-source-map | Separated K-IFRS, regulator, disclosure, law, and private-client source lanes with storage boundaries. | `docs/reports/2026-07-05-authority-source-map-close-report.md` |
| client-private intake/local parser | Defined local-only private intake, redaction, parser dry-run, deletion attestation, and adapter plan boundaries. | `docs/reports/2026-07-05-local-parser-real-adapter-implementation-plan.md` |

## Automation Snapshot

- Review packs: 24
- Automated packs: 20
- Human-review packs: 4
- Automation rate: 83.33%

## Open Decisions

| Decision | Status | Blocker | Command |
|---|---|---|---|
| run_NIS1_source_asset_inventory | active | none | `python scripts\quality_preflight.py --format text` |
| approve_default_retriever_promotion | deferred_until_eval_evidence_and_authorization | stronger evaluation evidence and explicit authorization are missing | `python scripts\default_retriever_guard.py --format text` |

## Remaining Gaps

- RAG quality needs a fresh internal validation horizon before any default retriever promotion
- local parser real-adapter implementation plan is present, but actual evidence and explicit authorization are still required before real upload/OCR/parser/deletion automation
- external source connector metadata-only lane is closed and demo-noted; authorization record scaffold is present, but source-body connector is still not implemented
- opt-in retriever promotion decision gate and default retriever guard are present, but default retriever change remains deferred until stronger evaluation evidence and explicit authorization
- firm-facing brief and toolkit packaging docs exist, but the repo is still closer to an internal toolkit than a finished user-facing product

## Next Leaf

- decision: `NIS1_existing_source_asset_inventory`
- command: `python scripts\quality_preflight.py --format text`

## Machine Result

```json
{
  "title": "Accounting Intelligence Progress Map",
  "objective": "Prove how far accountant work can be automated, then package that proof as a local toolkit for firm PoC.",
  "current_horizon": {
    "id": "non-ifrs-source-dataization",
    "status": "active",
    "goal": "Turn KASB/FSS, law, DART, and client-private source lanes into public-safe RAG dataization units.",
    "milestones": [
      {
        "id": "NIS1",
        "name": "existing source asset inventory",
        "status": "active_next"
      },
      {
        "id": "NIS2",
        "name": "source record contract",
        "status": "pending"
      },
      {
        "id": "NIS3",
        "name": "dataization fixtures and validators",
        "status": "pending"
      },
      {
        "id": "NIS4",
        "name": "chunking and embedding policy",
        "status": "pending"
      },
      {
        "id": "NIS5",
        "name": "dataization gate and runtime handoff",
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
    }
  ],
  "open_decisions": [
    {
      "id": "run_NIS1_source_asset_inventory",
      "status": "active",
      "decide": "Build the first inventory report for non-IFRS source dataization.",
      "blocker": "none",
      "command": "python scripts\\quality_preflight.py --format text"
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
    "RAG quality needs a fresh internal validation horizon before any default retriever promotion",
    "local parser real-adapter implementation plan is present, but actual evidence and explicit authorization are still required before real upload/OCR/parser/deletion automation",
    "external source connector metadata-only lane is closed and demo-noted; authorization record scaffold is present, but source-body connector is still not implemented",
    "opt-in retriever promotion decision gate and default retriever guard are present, but default retriever change remains deferred until stronger evaluation evidence and explicit authorization",
    "firm-facing brief and toolkit packaging docs exist, but the repo is still closer to an internal toolkit than a finished user-facing product"
  ],
  "next_leaf": "NIS1_existing_source_asset_inventory",
  "next_command": "python scripts\\quality_preflight.py --format text",
  "report_path": "docs/reports/2026-07-05-accounting-intelligence-progress-map.md"
}
```
