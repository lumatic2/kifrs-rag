# Horizon: Feedback Eval Backlog Integration

> Status: closed
> Created: 2026-07-05
> Sequence: `docs/horizons/accounting-intelligence-expansion.md`
> Previous: `docs/horizons/real-case-feedback-loop.md`

## Goal

회계사 correction candidate를 public-safe JSONL 큐로 누적하고, eval seed 후보와 product backlog 후보를
분리해 리포트로 볼 수 있게 만든다.

## Why next

`real-case-feedback-loop`는 익명 사례 intake와 correction candidate 변환을 만들었다. 하지만 candidate가
파일/리포트 단위로 누적되지 않으면 현업 피드백이 다음 품질 개선 작업으로 이어지지 않는다. 이번
horizon은 "피드백을 받았다"를 "평가셋 후보와 제품 backlog 후보가 생겼다"로 바꾸는 연결부다.

## Milestones

### FI1. Feedback Queue Store

validated case/correction/seed candidate를 JSONL queue record로 저장하고 다시 읽는다.

Deliverable:

- `kifrs/feedback/queue.py`
- `tests/test_feedback_queue.py`

Acceptance:

- public-safe record만 저장한다.
- duplicate record id를 감지한다.
- eval/backlog/no_action disposition을 유지한다.

### FI2. Queue Report and Split

queue를 읽어 eval seed 후보와 backlog 후보를 분리하고 markdown summary를 만든다.

Deliverable:

- report renderer
- `scripts/feedback_queue_report.py`

Acceptance:

- eval_seed_candidate와 backlog_candidate count를 분리한다.
- blocker/high severity를 surfacing한다.
- raw source body/customer identifier를 출력하지 않는다.

### FI3. Public-Safe Sample Queue

sample case/correction을 queue에 쓰고 report를 재생성한다.

Deliverable:

- `docs/feedback/feedback_queue.sample.jsonl`
- `docs/reports/2026-07-05-fi3-feedback-queue-report.md`

Acceptance:

- sample queue는 actual client case가 아님을 명시한다.
- command로 동일 report를 재생성한다.

### FI4. Close Gate

tests, public-safe preflight, ROADMAP/OBJECTIVE sync를 끝낸다.

Deliverable:

- `docs/reports/2026-07-05-fi4-feedback-eval-backlog-close-report.md`

Acceptance:

- feedback queue tests pass.
- existing feedback tests pass.
- `quality_preflight.py` public-safe gate passes.
