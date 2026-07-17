# Horizon: Accountant Feedback Incorporation

> Status: closed
> Created: 2026-07-05
> Sequence: `docs/horizons/accounting-intelligence-expansion.md`
> Previous: `docs/horizons/real-anonymized-transaction-poc.md`

## Goal

feedback queue에 들어온 회계사 correction 후보를 demo brief, review questions, eval/backlog rules에
반영할 수 있는 action plan으로 변환한다.

## Why next

`real-anonymized-transaction-poc`은 익명화 거래 카드가 F-ACC review pack과 feedback queue record로
이어지는 것을 보여줬다. 다음 병목은 queue에 쌓인 correction이 실제 제품 개선으로 어떻게 반영되는지다.

## Milestones

### AF1. Horizon and Plan Setup

Deliverable:

- `docs/horizons/accountant-feedback-incorporation.md`
- `docs/plans/2026-07-05-accountant-feedback-incorporation.md`
- `phases/accountant-feedback-incorporation/*`

Acceptance:

- ROADMAP/OBJECTIVE가 active horizon을 가리킨다.
- AF1~AF4 phase가 정의된다.

Status: completed (2026-07-05)

### AF2. Feedback Incorporation Planner

Deliverable:

- `kifrs/feedback/incorporation.py`
- `tests/test_feedback_incorporation.py`

Acceptance:

- feedback queue record를 review question, review pack checklist, eval seed, backlog action으로 분류한다.
- high/blocker severity는 priority action으로 표시한다.

Status: completed (2026-07-05)

### AF3. Incorporation Report Command

Deliverable:

- `scripts/feedback_incorporation_report.py`
- `docs/reports/2026-07-05-af3-feedback-incorporation-report.md`
- `docs/reports/field-feedback/2026-07-05-incorporated-review-questions.md`

Acceptance:

- 명령 하나로 queue 기반 incorporation report와 review question supplement를 생성한다.

Status: completed (2026-07-05)

### AF4. Close Gate

Deliverable:

- `docs/reports/2026-07-05-af4-accountant-feedback-incorporation-close-report.md`

Acceptance:

- focused tests pass.
- generated reports exist.
- quality preflight remains public-safe.
- ROADMAP/OBJECTIVE가 다음 horizon을 제안한다.

Status: completed (2026-07-05)
