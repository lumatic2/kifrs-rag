# Accounting Intelligence Progress Map

> Scope: plain-language objective/horizon/milestone position for continuing Accounting Intelligence work.

## One-Line Position

The active horizon is client-private parser runtime: connect local private files to runtime through structured facts, client-private evidence, and deletion gates.

## Objective

Prove how far accountant work can be automated, then package that proof as a local toolkit for firm PoC.

## Current Horizon

- Horizon: `client-private-parser-runtime`
- Status: active
- Goal: Connect local private files to runtime through structured-facts-only parser, client-private evidence adapter, and deletion gate.

| Milestone | Name | Status |
|---|---|---|
| CP1 | private parser boundary audit | active_next |
| CP2 | local parser runtime contract | pending |
| CP3 | client-private evidence adapter | pending |
| CP4 | deletion and retention gate | pending |
| CP5 | private runtime close demo | pending |

## Completed Capability Chain

| Horizon | Result | Evidence |
|---|---|---|
| firm-service-map | Mapped accounting firm teams and selected F-ACC/accounting advisory as the first product lane. | `docs/horizons/firm-service-map.md` |
| F-ACC sequence | Turned the firm-service map into review-pack workflow sequence candidates. | `BACKLOG.md` |
| rag-quality-refresh | Built an opt-in repair retriever stack that reaches 50-item recall@20 1.000 without default promotion. | `docs/reports/2026-07-05-rag-quality-refresh-close-report.md` |
| authority-source-map | Separated K-IFRS, regulator, disclosure, law, and private-client source lanes with storage boundaries. | `docs/reports/2026-07-05-authority-source-map-close-report.md` |
| client-private intake/local parser | Defined local-only private intake, redaction, parser dry-run, deletion attestation, and adapter plan boundaries. | `docs/reports/2026-07-05-local-parser-real-adapter-implementation-plan.md` |
| multi-authority-runtime-hardening | Connected K-IFRS primary, supporting, legal, fact, and client-private placeholder evidence across runtime, review packs, statement draft, analytics, and close gate. | `docs/reports/2026-07-05-multi-authority-runtime-hardening-close-report.md` |

## Automation Snapshot

- Review packs: 24
- Automated packs: 20
- Human-review packs: 4
- Automation rate: 83.33%

## Open Decisions

| Decision | Status | Blocker | Command |
|---|---|---|---|
| run_CP1_private_parser_boundary_audit | active | none | `python -m pytest tests\test_client_private_parser_dry_run_fixture.py tests\test_client_private_local_parser_adapter_contract.py -q` |
| approve_default_retriever_promotion | deferred_until_eval_evidence_and_authorization | stronger evaluation evidence and explicit authorization are missing | `python scripts\default_retriever_guard.py --format text` |

## Remaining Gaps

- RAG quality needs a fresh internal validation horizon before any default retriever promotion
- local parser real-adapter implementation plan is present, but actual evidence and explicit authorization are still required before real upload/OCR/parser/deletion automation
- external source connector metadata-only lane is closed and demo-noted; authorization record scaffold is present, but source-body connector is still not implemented
- opt-in retriever promotion decision gate and default retriever guard are present, but default retriever change remains deferred until stronger evaluation evidence and explicit authorization
- firm-facing brief and toolkit packaging docs exist, but the repo is still closer to an internal toolkit than a finished user-facing product

## Next Leaf

- decision: `CP1_private_parser_boundary_audit`
- command: `python -m pytest tests\test_client_private_parser_dry_run_fixture.py tests\test_client_private_local_parser_adapter_contract.py -q`

## Machine Result

```json
{
  "title": "Accounting Intelligence Progress Map",
  "objective": "Prove how far accountant work can be automated, then package that proof as a local toolkit for firm PoC.",
  "current_horizon": {
    "id": "client-private-parser-runtime",
    "status": "active",
    "goal": "Connect local private files to runtime through structured-facts-only parser, client-private evidence adapter, and deletion gate.",
    "milestones": [
      {
        "id": "CP1",
        "name": "private parser boundary audit",
        "status": "active_next"
      },
      {
        "id": "CP2",
        "name": "local parser runtime contract",
        "status": "pending"
      },
      {
        "id": "CP3",
        "name": "client-private evidence adapter",
        "status": "pending"
      },
      {
        "id": "CP4",
        "name": "deletion and retention gate",
        "status": "pending"
      },
      {
        "id": "CP5",
        "name": "private runtime close demo",
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
    }
  ],
  "open_decisions": [
    {
      "id": "run_CP1_private_parser_boundary_audit",
      "status": "active",
      "decide": "Audit existing local parser, redaction, storage, adapter, and deletion scaffolds before implementing the private runtime path.",
      "blocker": "none",
      "command": "python -m pytest tests\\test_client_private_parser_dry_run_fixture.py tests\\test_client_private_local_parser_adapter_contract.py -q"
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
  "next_leaf": "CP1_private_parser_boundary_audit",
  "next_command": "python -m pytest tests\\test_client_private_parser_dry_run_fixture.py tests\\test_client_private_local_parser_adapter_contract.py -q",
  "report_path": "docs/reports/2026-07-05-accounting-intelligence-progress-map.md"
}
```
