# Accounting Intelligence Progress Map

> Scope: plain-language objective/horizon/milestone position for continuing Accounting Intelligence work.

## One-Line Position

The active horizon is operator-experience-hardening: add report navigation after run diagnostics.

## Objective

Prove how far accountant work can be automated, then package that proof as a local toolkit for firm PoC.

## Current Horizon

- Horizon: `operator-experience-hardening`
- Status: active
- Goal: Turn the CLI/report collection into a smoother local operator experience with command discovery, diagnostics, manifests, and recovery.

| Milestone | Name | Status |
|---|---|---|
| OEH1 | operator command inventory | completed |
| OEH2 | run doctor and environment checks | completed |
| OEH3 | report manifest and navigation surface | active_next |
| OEH4 | error recovery playbook | pending |
| OEH5 | operator experience close gate | pending |

## Completed Capability Chain

| Horizon | Result | Evidence |
|---|---|---|
| firm-service-map | Mapped accounting firm teams and selected F-ACC/accounting advisory as the first product lane. | `docs/horizons/firm-service-map.md` |
| F-ACC sequence | Turned the firm-service map into review-pack workflow sequence candidates. | `BACKLOG.md` |
| rag-quality-refresh | Built an opt-in repair retriever stack that reaches 50-item recall@20 1.000 without default promotion. | `docs/reports/2026-07-05-rag-quality-refresh-close-report.md` |
| authority-source-map | Separated K-IFRS, regulator, disclosure, law, and private-client source lanes with storage boundaries. | `docs/reports/2026-07-05-authority-source-map-close-report.md` |
| client-private intake/local parser | Defined local-only private intake, redaction, parser dry-run, deletion attestation, and adapter plan boundaries. | `docs/reports/2026-07-05-local-parser-real-adapter-implementation-plan.md` |
| multi-authority-runtime-hardening | Connected K-IFRS primary, supporting, legal, fact, and client-private placeholder evidence across runtime, review packs, statement draft, analytics, and close gate. | `docs/reports/2026-07-05-multi-authority-runtime-hardening-close-report.md` |
| client-private-parser-runtime | Added structured-facts-only private parser runtime contract, client_private_fact adapter, deletion close gate, and close demo without public private payload. | `docs/reports/2026-07-05-client-private-parser-runtime-close-report.md` |
| real-local-parser-prototype | Closed a local-safe fixture parser path with asset inventory, fixture adapter, deletion simulation, leak tests, and close gate. | `docs/reports/2026-07-05-real-local-parser-prototype-close-report.md` |
| source-body-ingestion-controlled-lane | Closed one synthetic-only controlled non-IFRS interpretive lane with source selection, policy, chunking, retrieval, and public-safe close gate. | `docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md` |
| workflow-coverage-expansion | Expanded firm-service coverage with a 1037 provisions decision-prep workflow ranking, contract, adapter, metric update, and close gate. | `docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md` |
| runtime-retriever-promotion-gate | Closed retriever default promotion as defer with evidence inventory, regression/latency gate, rollback policy, operator dry-run, and close report. | `docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md` |

## Automation Snapshot

- Review packs: 24
- Automated packs: 20
- Human-review packs: 4
- Automation rate: 83.33%

## Open Decisions

| Decision | Status | Blocker | Command |
|---|---|---|---|
| run_OEH3_report_manifest | active | none | `python -m pytest tests\test_operator_report_manifest.py -q` |
| approve_default_retriever_promotion | deferred_until_eval_evidence_and_authorization | stronger evaluation evidence and explicit authorization are missing | `python scripts\default_retriever_guard.py --format text` |

## Remaining Gaps

- RAG quality needs a fresh internal validation horizon before any default retriever promotion
- local parser real-adapter implementation plan is present, but actual evidence and explicit authorization are still required before real upload/OCR/parser/deletion automation
- external source connector metadata-only lane is closed and demo-noted; authorization record scaffold is present, but source-body connector is still not implemented
- opt-in retriever promotion decision gate and default retriever guard are present, but default retriever change remains deferred until stronger evaluation evidence and explicit authorization
- firm-facing brief and toolkit packaging docs exist, but the repo is still closer to an internal toolkit than a finished user-facing product

## Next Leaf

- decision: `OEH3_report_manifest`
- command: `python -m pytest tests\test_operator_report_manifest.py -q`

## Machine Result

```json
{
  "title": "Accounting Intelligence Progress Map",
  "objective": "Prove how far accountant work can be automated, then package that proof as a local toolkit for firm PoC.",
  "current_horizon": {
    "id": "operator-experience-hardening",
    "status": "active",
    "goal": "Turn the CLI/report collection into a smoother local operator experience with command discovery, diagnostics, manifests, and recovery.",
    "milestones": [
      {
        "id": "OEH1",
        "name": "operator command inventory",
        "status": "completed"
      },
      {
        "id": "OEH2",
        "name": "run doctor and environment checks",
        "status": "completed"
      },
      {
        "id": "OEH3",
        "name": "report manifest and navigation surface",
        "status": "active_next"
      },
      {
        "id": "OEH4",
        "name": "error recovery playbook",
        "status": "pending"
      },
      {
        "id": "OEH5",
        "name": "operator experience close gate",
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
      "id": "multi-authority-runtime-hardening",
      "result": "Connected K-IFRS primary, supporting, legal, fact, and client-private placeholder evidence across runtime, review packs, statement draft, analytics, and close gate.",
      "evidence": "docs/reports/2026-07-05-multi-authority-runtime-hardening-close-report.md"
    },
    {
      "id": "client-private-parser-runtime",
      "result": "Added structured-facts-only private parser runtime contract, client_private_fact adapter, deletion close gate, and close demo without public private payload.",
      "evidence": "docs/reports/2026-07-05-client-private-parser-runtime-close-report.md"
    },
    {
      "id": "real-local-parser-prototype",
      "result": "Closed a local-safe fixture parser path with asset inventory, fixture adapter, deletion simulation, leak tests, and close gate.",
      "evidence": "docs/reports/2026-07-05-real-local-parser-prototype-close-report.md"
    },
    {
      "id": "source-body-ingestion-controlled-lane",
      "result": "Closed one synthetic-only controlled non-IFRS interpretive lane with source selection, policy, chunking, retrieval, and public-safe close gate.",
      "evidence": "docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md"
    },
    {
      "id": "workflow-coverage-expansion",
      "result": "Expanded firm-service coverage with a 1037 provisions decision-prep workflow ranking, contract, adapter, metric update, and close gate.",
      "evidence": "docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md"
    },
    {
      "id": "runtime-retriever-promotion-gate",
      "result": "Closed retriever default promotion as defer with evidence inventory, regression/latency gate, rollback policy, operator dry-run, and close report.",
      "evidence": "docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md"
    }
  ],
  "open_decisions": [
    {
      "id": "run_OEH3_report_manifest",
      "status": "active",
      "decide": "Create an ordered report manifest so the operator can navigate evidence without reading ROADMAP internals.",
      "blocker": "none",
      "command": "python -m pytest tests\\test_operator_report_manifest.py -q"
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
  "next_leaf": "OEH3_report_manifest",
  "next_command": "python -m pytest tests\\test_operator_report_manifest.py -q",
  "report_path": "docs/reports/2026-07-05-accounting-intelligence-progress-map.md"
}
```
