# Accounting Intelligence Progress Map

> Scope: plain-language objective/horizon/milestone position for continuing Accounting Intelligence work.

## One-Line Position

The active horizon is multi-authority runtime hardening: make workflow outputs keep primary, supporting, legal, fact, and private evidence separate.

## Objective

Prove how far accountant work can be automated, then package that proof as a local toolkit for firm PoC.

## Current Horizon

- Horizon: `multi-authority-runtime-hardening`
- Status: active
- Goal: Use K-IFRS, supporting interpretation, legal boundary, fact evidence, and client-private facts as separated runtime evidence.

| Milestone | Name | Status |
|---|---|---|
| MAH1 | runtime evidence boundary audit | completed |
| MAH2 | runtime evidence contract hardening | active_next |
| MAH3 | review pack authority panel | pending |
| MAH4 | statement draft and analytics fact hook | pending |
| MAH5 | authority composer gate and runtime demo | pending |

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
| run_MAH2_runtime_evidence_contract_hardening | active | none | `python -m pytest tests\test_runtime_authority_boundary.py -q` |
| approve_default_retriever_promotion | deferred_until_eval_evidence_and_authorization | stronger evaluation evidence and explicit authorization are missing | `python scripts\default_retriever_guard.py --format text` |

## Remaining Gaps

- RAG quality needs a fresh internal validation horizon before any default retriever promotion
- local parser real-adapter implementation plan is present, but actual evidence and explicit authorization are still required before real upload/OCR/parser/deletion automation
- external source connector metadata-only lane is closed and demo-noted; authorization record scaffold is present, but source-body connector is still not implemented
- opt-in retriever promotion decision gate and default retriever guard are present, but default retriever change remains deferred until stronger evaluation evidence and explicit authorization
- firm-facing brief and toolkit packaging docs exist, but the repo is still closer to an internal toolkit than a finished user-facing product

## Next Leaf

- decision: `MAH2_runtime_evidence_contract_hardening`
- command: `python -m pytest tests\test_runtime_authority_boundary.py -q`

## Machine Result

```json
{
  "title": "Accounting Intelligence Progress Map",
  "objective": "Prove how far accountant work can be automated, then package that proof as a local toolkit for firm PoC.",
  "current_horizon": {
    "id": "multi-authority-runtime-hardening",
    "status": "active",
    "goal": "Use K-IFRS, supporting interpretation, legal boundary, fact evidence, and client-private facts as separated runtime evidence.",
    "milestones": [
      {
        "id": "MAH1",
        "name": "runtime evidence boundary audit",
        "status": "completed"
      },
      {
        "id": "MAH2",
        "name": "runtime evidence contract hardening",
        "status": "active_next"
      },
      {
        "id": "MAH3",
        "name": "review pack authority panel",
        "status": "pending"
      },
      {
        "id": "MAH4",
        "name": "statement draft and analytics fact hook",
        "status": "pending"
      },
      {
        "id": "MAH5",
        "name": "authority composer gate and runtime demo",
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
      "id": "run_MAH2_runtime_evidence_contract_hardening",
      "status": "active",
      "decide": "Add a shared runtime authority object that converts NIS source records without mixing primary, supporting, legal, fact, and private roles.",
      "blocker": "none",
      "command": "python -m pytest tests\\test_runtime_authority_boundary.py -q"
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
  "next_leaf": "MAH2_runtime_evidence_contract_hardening",
  "next_command": "python -m pytest tests\\test_runtime_authority_boundary.py -q",
  "report_path": "docs/reports/2026-07-05-accounting-intelligence-progress-map.md"
}
```
