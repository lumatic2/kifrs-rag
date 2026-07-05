# Accounting Intelligence Progress Map

> Scope: plain-language objective/horizon/milestone position for continuing Accounting Intelligence work.

## One-Line Position

DRQ4 internal fixes are implemented: timing threshold, freshness metadata, and operator summary are closed.

## Operator Summary

- status: demo_rehearsal_improvements_hardened
- current horizon: `demo-rehearsal-improvement-hardening`
- next operator action: open a new objective audit horizon when the next product weakness is selected
- automation rate: 83.33%
- main residual risk: default retriever promotion remains deferred by guard
- primary evidence: `docs/reports/2026-07-06-demo-rehearsal-improvement-hardening-close-report.md`

## Objective

Prove how far accountant work can be automated, then turn that proof into firm-facing local toolkit evidence.

## Current Horizon

- Horizon: `demo-rehearsal-improvement-hardening`
- Status: closed
- Goal: The three DRQ4 internal rehearsal improvements have been implemented and verified.

| Milestone | Name | Status |
|---|---|---|
| DRI1 | retriever timing threshold | completed |
| DRI2 | rehearsal freshness metadata | completed |
| DRI3 | operator summary surface | completed |
| DRI4 | close gate | completed |

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
| demo-rehearsal-improvement-hardening | Implemented DRQ4 internal fixes: timing threshold, freshness metadata, and operator summary surface. | `docs/reports/2026-07-06-demo-rehearsal-improvement-hardening-close-report.md` |

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
| run_external_connector_body_expansion | closed_connector_body_lane_ready | none | `python scripts\external_source_connector_body_close_gate.py --format text` |
| run_workflow_coverage_depth_expansion | closed_coverage_depth_expanded | none | `python scripts\workflow_coverage_depth_close_gate.py --format text` |
| run_demo_rehearsal_quality_loop | closed_demo_rehearsal_quality_loop | none | `python scripts\demo_rehearsal_quality_close_gate.py --format text --write` |
| approve_default_retriever_promotion | deferred_until_eval_evidence_and_authorization | stronger evaluation evidence and explicit authorization are missing | `python scripts\default_retriever_guard.py --format text` |

## Remaining Gaps

- No active rehearsal-improvement horizon remains.
- Residual risks should become a new horizon only after an explicit next objective decision.

## Next Leaf

- decision: `demo_rehearsal_improvement_hardening_complete`
- command: `python scripts\demo_rehearsal_improvement_close_gate.py --format text`

## Machine Result

```json
{
  "title": "Accounting Intelligence Progress Map",
  "objective": "Prove how far accountant work can be automated, then turn that proof into firm-facing local toolkit evidence.",
  "operator_summary": {
    "status": "demo_rehearsal_improvements_hardened",
    "current_horizon": "demo-rehearsal-improvement-hardening",
    "next_operator_action": "open a new objective audit horizon when the next product weakness is selected",
    "automation_rate": 0.8333,
    "main_residual_risk": "default retriever promotion remains deferred by guard",
    "primary_evidence": "docs/reports/2026-07-06-demo-rehearsal-improvement-hardening-close-report.md"
  },
  "current_horizon": {
    "id": "demo-rehearsal-improvement-hardening",
    "status": "closed",
    "goal": "The three DRQ4 internal rehearsal improvements have been implemented and verified.",
    "milestones": [
      {
        "id": "DRI1",
        "name": "retriever timing threshold",
        "status": "completed"
      },
      {
        "id": "DRI2",
        "name": "rehearsal freshness metadata",
        "status": "completed"
      },
      {
        "id": "DRI3",
        "name": "operator summary surface",
        "status": "completed"
      },
      {
        "id": "DRI4",
        "name": "close gate",
        "status": "completed"
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
    },
    {
      "id": "demo-rehearsal-improvement-hardening",
      "result": "Implemented DRQ4 internal fixes: timing threshold, freshness metadata, and operator summary surface.",
      "evidence": "docs/reports/2026-07-06-demo-rehearsal-improvement-hardening-close-report.md"
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
      "status": "closed_connector_body_lane_ready",
      "decide": "External source-body connector expansion closed with selected lane, fixture contract, retrieval dry run, leak gate, and workflow coverage handoff.",
      "blocker": "none",
      "command": "python scripts\\external_source_connector_body_close_gate.py --format text"
    },
    {
      "id": "run_workflow_coverage_depth_expansion",
      "status": "closed_coverage_depth_expanded",
      "decide": "Workflow coverage depth closed with audit_disclosure_tie_out rerank, contract, adapter, metric, and demo rehearsal handoff.",
      "blocker": "none",
      "command": "python scripts\\workflow_coverage_depth_close_gate.py --format text"
    },
    {
      "id": "run_demo_rehearsal_quality_loop",
      "status": "closed_demo_rehearsal_quality_loop",
      "decide": "DRQ1 to DRQ5 are complete; the demo rehearsal quality loop and objective-gap queue are closed.",
      "blocker": "none",
      "command": "python scripts\\demo_rehearsal_quality_close_gate.py --format text --write"
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
    "No active rehearsal-improvement horizon remains.",
    "Residual risks should become a new horizon only after an explicit next objective decision."
  ],
  "next_leaf": "demo_rehearsal_improvement_hardening_complete",
  "next_command": "python scripts\\demo_rehearsal_improvement_close_gate.py --format text",
  "report_path": "docs/reports/2026-07-05-accounting-intelligence-progress-map.md"
}
```
