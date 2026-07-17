# Plan: Accountant Feedback Incorporation

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/accountant-feedback-incorporation.md`
> Status source: `phases/accountant-feedback-incorporation/index.json`

## 요약

이번 run은 실제 회계사 correction 후보가 queue에 들어온 뒤 제품 개선으로 이어지는 경로를 만든다.
첫 구현은 queue record를 action plan으로 바꾸고, demo/review question supplement를 생성하는 것이다.

## Step Tree

- [x] AF1 — horizon/phase/plan setup. (verify: `Test-Path docs\horizons\accountant-feedback-incorporation.md`)
- [x] AF2 — feedback incorporation planner. (verify: `python -m pytest tests\test_feedback_incorporation.py -q`)
- [x] AF3 — incorporation report command. (verify: `python scripts\feedback_incorporation_report.py --queue docs\reports\real-transaction-poc\feedback-queue.jsonl --out docs\reports\2026-07-05-af3-feedback-incorporation-report.md --questions-out docs\reports\field-feedback\2026-07-05-incorporated-review-questions.md`)
- [x] AF4 — close gate and status sync. (verify: focused tests + `python scripts\quality_preflight.py --format text`)

## 결정 로그

- 결정: 실제 회계사 피드백이 아직 없으므로, 직전 horizon의 public-safe sample queue를 첫 입력으로 사용한다.
- 결정: queue record를 원문 수정으로 바로 patch하지 않고, review question supplement와 incorporation report로 먼저 반영한다.
- 이유: 실제 회계사 피드백이 들어오기 전에는 demo 본문을 단정적으로 바꾸기보다, 반영 후보와 검증 규칙을 분리하는 편이 안전하다.
- 예상 사용자 소유 결정: 없음. 실제 회계사 피드백 수집은 병행 사용자 액션으로 유지한다.

## 중단점

- correction이 protected payload를 요구하면 close하지 않는다.
- generated report가 eval/backlog split을 흐리면 close하지 않는다.
