# Horizon: Field Feedback Capture

> Status: closed
> Created: 2026-07-05
> Sequence: `docs/horizons/accounting-intelligence-expansion.md`
> Previous: `docs/horizons/field-feedback-runbook.md`

## Goal

회계사 피드백 세션에서 나온 notes를 public-safe 구조로 기록하고, safe correction만 feedback queue
record로 변환하는 capture pipeline을 만든다.

## Why next

`field-feedback-runbook`은 30분 세션 운영 절차를 만들었다. 다음 단계는 세션에서 나온 답변을 raw
메모로 흩어두지 않고, 보호자료 없이 검증 가능한 correction 후보로 전환하는 것이다.

## Milestones

### FC1. Horizon and Plan Setup

Deliverable:

- `docs/horizons/field-feedback-capture.md`
- `docs/plans/2026-07-05-field-feedback-capture.md`
- `phases/field-feedback-capture/*`

Acceptance:

- ROADMAP/OBJECTIVE가 active horizon을 가리킨다.
- FC1~FC4 phase가 정의된다.

Status: completed (2026-07-05)

### FC2. Feedback Notes Capture Contract

Deliverable:

- `kifrs/feedback/capture.py`
- `tests/test_field_feedback_capture.py`

Acceptance:

- notes schema가 reviewer context, scores, top risk, correction candidates를 표현한다.
- protected payload가 포함된 notes는 거부된다.
- safe corrections는 queue record로 변환된다.

Status: completed (2026-07-05)

### FC3. Capture Report Command

Deliverable:

- `scripts/field_feedback_capture.py`
- `docs/reports/field-feedback-capture/`

Acceptance:

- 명령 하나로 sample notes, capture report, queue JSONL, queue report가 생성된다.

Status: completed (2026-07-05)

### FC4. Close Gate

Deliverable:

- `docs/reports/2026-07-05-fc4-field-feedback-capture-close-report.md`

Acceptance:

- focused tests pass.
- sample capture package exists.
- quality preflight remains public-safe.
- ROADMAP/OBJECTIVE가 다음 horizon을 제안한다.

Status: completed (2026-07-05)
