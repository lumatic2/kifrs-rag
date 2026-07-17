# Horizon: Field Feedback Runbook

> Status: closed
> Created: 2026-07-05
> Sequence: `docs/horizons/accounting-intelligence-expansion.md`
> Previous: `docs/horizons/accountant-feedback-incorporation.md`

## Goal

one-page brief, demo bundle, real-transaction sample, incorporation report를 묶어 회계사 30분 피드백
세션을 실제로 운영할 runbook을 만든다.

## Why next

`accountant-feedback-incorporation`까지 완료되면서 기술 루프는 생겼다. 이제 병목은 "무엇을 보여주고,
어떤 순서로 질문하고, 끝난 뒤 어떤 산출물로 반영할 것인가"이다. 이 horizon은 사용자가 세션에 바로
쓸 수 있는 운영 절차와 체크리스트를 만든다.

## Milestones

### FB1. Horizon and Plan Setup

Deliverable:

- `docs/horizons/field-feedback-runbook.md`
- `docs/plans/2026-07-05-field-feedback-runbook.md`
- `phases/field-feedback-runbook/*`

Acceptance:

- ROADMAP/OBJECTIVE가 active horizon을 가리킨다.
- FB1~FB4 phase가 정의된다.

Status: completed (2026-07-05)

### FB2. Session Runbook

Deliverable:

- `docs/reports/field-feedback-runbook/2026-07-05-30min-session-runbook.md`
- `docs/reports/field-feedback-runbook/2026-07-05-operator-checklist.md`

Acceptance:

- 30분 세션 타임라인, 사전 준비, 화면 순서, 질문 순서, 사후 처리 절차가 포함된다.

Status: completed (2026-07-05)

### FB3. Runbook Manifest and Checker

Deliverable:

- `docs/reports/field-feedback-runbook/runbook_manifest.json`
- `scripts/field_feedback_runbook_check.py`
- `tests/test_field_feedback_runbook.py`

Acceptance:

- manifest가 필수 입력 자료를 모두 가리킨다.
- checker가 missing artifact를 실패로 표시한다.

Status: completed (2026-07-05)

### FB4. Close Gate

Deliverable:

- `docs/reports/2026-07-05-fb4-field-feedback-runbook-close-report.md`

Acceptance:

- focused tests pass.
- runbook checker passes.
- quality preflight remains public-safe.
- ROADMAP/OBJECTIVE가 다음 horizon을 제안한다.

Status: completed (2026-07-05)
