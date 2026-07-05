# Accounting Intelligence Progress Map

> Scope: plain-language objective/horizon/milestone position for continuing Accounting Intelligence work.

## One-Line Position

Objective gaps are grouped into horizons; ESB1 selected the first external source-body connector lane and ESB2 is now active.

## Objective

Prove how far accountant work can be automated, then turn that proof into firm-facing local toolkit evidence.

## Current Horizon

- Horizon: `external-source-body-connector-expansion`
- Status: active
- Goal: Expand non-IFRS source body connector evidence under policy-gated, public-safe source-body handling.

| Milestone | Name | Status |
|---|---|---|
| ESB1 | source-body connector selection and policy gate | completed |
| ESB2 | synthetic source-body fixture contract | active |
| ESB3 | chunking and retrieval dry run | pending |
| ESB4 | connector leak and policy gate | pending |
| ESB5 | close and workflow coverage handoff | pending |

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
| operator-experience-hardening | Closed operator UX with command inventory, run doctor, report manifest, recovery playbook, and close gate. | `docs/reports/2026-07-05-operator-experience-hardening-close-report.md` |

## Automation Snapshot

- Review packs: 24
- Automated packs: 20
- Human-review packs: 4
- Automation rate: 83.33%

## Open Decisions

| Decision | Status | Blocker | Command |
|---|---|---|---|
| select_next_post_demo_horizon | closed_by_objective_gap_queue | none | `python scripts\objective_gap_horizon_candidates.py --format text` |
| run_rag_quality_fresh_validation | closed_defer | none | `python scripts\rag_quality_fresh_validation_close_gate.py --format text` |
| run_private_parser_realism_hardening | closed_realism_contract_ready | none | `python scripts\private_parser_realism_close_gate.py --format text` |
| run_external_connector_body_expansion | active_horizon | none | `python scripts\external_source_connector_body_fixture_contract.py --format text --write` |
| approve_default_retriever_promotion | deferred_until_eval_evidence_and_authorization | stronger evaluation evidence and explicit authorization are missing | `python scripts\default_retriever_guard.py --format text` |

## Remaining Gaps

- RAG quality needs a fresh internal validation horizon before any default retriever promotion
- local parser real-adapter implementation plan is present, but actual evidence and explicit authorization are still required before real upload/OCR/parser/deletion automation
- external source connector metadata-only lane is closed and demo-noted; authorization record scaffold is present, but source-body connector is still not implemented
- opt-in retriever promotion decision gate and default retriever guard are present, but default retriever change remains deferred until stronger evaluation evidence and explicit authorization
- firm-facing brief and demo packet exist, but the repo is still closer to an internal toolkit than a field-proven product

## Next Leaf

- decision: `ESB2_synthetic_connector_body_fixture_contract`
- command: `python scripts\external_source_connector_body_fixture_contract.py --format text --write`

## Machine Result

```json
{
  "title": "Accounting Intelligence Progress Map",
  "objective": "Prove how far accountant work can be automated, then turn that proof into firm-facing local toolkit evidence.",
  "current_horizon": {
    "id": "external-source-body-connector-expansion",
    "status": "active",
    "goal": "Expand non-IFRS source body connector evidence under policy-gated, public-safe source-body handling.",
    "milestones": [
      {
        "id": "ESB1",
        "name": "source-body connector selection and policy gate",
        "status": "completed"
      },
      {
        "id": "ESB2",
        "name": "synthetic source-body fixture contract",
        "status": "active"
      },
      {
        "id": "ESB3",
        "name": "chunking and retrieval dry run",
        "status": "pending"
      },
      {
        "id": "ESB4",
        "name": "connector leak and policy gate",
        "status": "pending"
      },
      {
        "id": "ESB5",
        "name": "close and workflow coverage handoff",
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
    },
    {
      "id": "operator-experience-hardening",
      "result": "Closed operator UX with command inventory, run doctor, report manifest, recovery playbook, and close gate.",
      "evidence": "docs/reports/2026-07-05-operator-experience-hardening-close-report.md"
    }
  ],
  "open_decisions": [
    {
      "id": "select_next_post_demo_horizon",
      "status": "closed_by_objective_gap_queue",
      "decide": "Objective gaps are grouped into a new horizon queue; run RAG quality fresh validation first.",
      "blocker": "none",
      "command": "python scripts\\objective_gap_horizon_candidates.py --format text"
    },
    {
      "id": "run_rag_quality_fresh_validation",
      "status": "closed_defer",
      "decide": "RAG quality fresh validation closed as defer; default retriever remains unchanged.",
      "blocker": "none",
      "command": "python scripts\\rag_quality_fresh_validation_close_gate.py --format text"
    },
    {
      "id": "run_private_parser_realism_hardening",
      "status": "closed_realism_contract_ready",
      "decide": "Private parser realism closed with authorization-safe adapter proof, fixture adapter contract, deletion rehearsal, leak gate, and source connector handoff.",
      "blocker": "none",
      "command": "python scripts\\private_parser_realism_close_gate.py --format text"
    },
    {
      "id": "run_external_connector_body_expansion",
      "status": "active_horizon",
      "decide": "ESB1 selected the first connector lane; continue with a synthetic fixture contract before chunking/retrieval work.",
      "blocker": "none",
      "command": "python scripts\\external_source_connector_body_fixture_contract.py --format text --write"
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
    "firm-facing brief and demo packet exist, but the repo is still closer to an internal toolkit than a field-proven product"
  ],
  "next_leaf": "ESB2_synthetic_connector_body_fixture_contract",
  "next_command": "python scripts\\external_source_connector_body_fixture_contract.py --format text --write",
  "report_path": "docs/reports/2026-07-05-accounting-intelligence-progress-map.md"
}
```
