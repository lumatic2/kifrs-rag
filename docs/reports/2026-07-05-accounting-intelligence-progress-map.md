# Accounting Intelligence Progress Map

> Scope: plain-language objective/horizon/milestone position for continuing Accounting Intelligence work.

## One-Line Position

The technical toolkit is broad enough for a demo, but the current proof is still waiting on one real accountant invite/session before RS2-RS4 can close.

## Objective

Prove how far accountant work can be automated, then package that proof as a local toolkit for firm PoC.

## Current Horizon

- Horizon: `real-accountant-session`
- Status: active
- Goal: Run one real accountant review session and convert public-safe notes into capture/queue evidence.

| Milestone | Name | Status |
|---|---|---|
| RS1 | session packet prep | completed |
| RS2 | run actual accountant session | waiting_on_reviewer_invite |
| RS3 | capture and queue conversion | pending_actual_notes |
| RS4 | close gate | pending_actual_evidence |

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
| send_reviewer_invite | needs_user_action | reviewer invite has not been sent | `python scripts\real_accountant_invite_packet.py --format text --write` |
| approve_default_retriever_promotion | deferred_until_actual_evidence_and_authorization | actual accountant evidence and explicit authorization are missing | `python scripts\default_retriever_guard.py --format text` |

## Remaining Gaps

- actual accountant session evidence is still external/user-owned; progress map, decision queue, next-action summary, next-action sequence gate, reviewer invite action packet, invite send receipt, filled receipt guide, invite receipt apply, post-send rehearsal, readiness index, external-action boundary, invite, response handling, after-send action matrix, outreach transition verifier, scheduled-session, RS3 notes-quality/capture-readiness/post-session final gate, operator execution brief, pre-send final gate, and close-state matrix are ready but the reviewer invite has not been sent
- local parser real-adapter implementation plan is present, but actual evidence and explicit authorization are still required before real upload/OCR/parser/deletion automation
- external source connector metadata-only lane is closed and demo-noted; authorization record scaffold is present, but source-body connector is still not implemented
- opt-in retriever promotion decision gate and default retriever guard are present, but default retriever change remains deferred until actual accountant evidence and explicit authorization

## Next Leaf

- decision: `send_reviewer_invite`
- command: `python scripts\real_accountant_invite_packet.py --format text --write`

## Machine Result

```json
{
  "title": "Accounting Intelligence Progress Map",
  "objective": "Prove how far accountant work can be automated, then package that proof as a local toolkit for firm PoC.",
  "current_horizon": {
    "id": "real-accountant-session",
    "status": "active",
    "goal": "Run one real accountant review session and convert public-safe notes into capture/queue evidence.",
    "milestones": [
      {
        "id": "RS1",
        "name": "session packet prep",
        "status": "completed"
      },
      {
        "id": "RS2",
        "name": "run actual accountant session",
        "status": "waiting_on_reviewer_invite"
      },
      {
        "id": "RS3",
        "name": "capture and queue conversion",
        "status": "pending_actual_notes"
      },
      {
        "id": "RS4",
        "name": "close gate",
        "status": "pending_actual_evidence"
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
      "id": "send_reviewer_invite",
      "status": "needs_user_action",
      "decide": "Which reviewer should receive the invite, and should the invite be sent now?",
      "blocker": "reviewer invite has not been sent",
      "command": "python scripts\\real_accountant_invite_packet.py --format text --write"
    },
    {
      "id": "approve_default_retriever_promotion",
      "status": "deferred_until_actual_evidence_and_authorization",
      "decide": "Promote the opt-in repair retriever to default only after actual accountant evidence and explicit authorization.",
      "blocker": "actual accountant evidence and explicit authorization are missing",
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
    "actual accountant session evidence is still external/user-owned; progress map, decision queue, next-action summary, next-action sequence gate, reviewer invite action packet, invite send receipt, filled receipt guide, invite receipt apply, post-send rehearsal, readiness index, external-action boundary, invite, response handling, after-send action matrix, outreach transition verifier, scheduled-session, RS3 notes-quality/capture-readiness/post-session final gate, operator execution brief, pre-send final gate, and close-state matrix are ready but the reviewer invite has not been sent",
    "local parser real-adapter implementation plan is present, but actual evidence and explicit authorization are still required before real upload/OCR/parser/deletion automation",
    "external source connector metadata-only lane is closed and demo-noted; authorization record scaffold is present, but source-body connector is still not implemented",
    "opt-in retriever promotion decision gate and default retriever guard are present, but default retriever change remains deferred until actual accountant evidence and explicit authorization"
  ],
  "next_leaf": "send_reviewer_invite",
  "next_command": "python scripts\\real_accountant_invite_packet.py --format text --write",
  "report_path": "docs/reports/2026-07-05-accounting-intelligence-progress-map.md"
}
```
