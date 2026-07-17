# Plan: Field Feedback Runbook

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/field-feedback-runbook.md`
> Status source: `phases/field-feedback-runbook/index.json`

## 요약

이번 run은 지금까지 만든 산출물을 회계사 30분 피드백 세션에 바로 쓸 수 있게 묶는다. 목표는 새 기능을
만드는 것이 아니라, one-page brief -> demo bundle -> real transaction sample -> incorporation report
순서로 실제 피드백을 받는 운영 절차를 고정하는 것이다.

## Step Tree

- [x] FB1 — horizon/phase/plan setup. (verify: `Test-Path docs\horizons\field-feedback-runbook.md`)
- [x] FB2 — 30분 session runbook + operator checklist. (verify: `Test-Path docs\reports\field-feedback-runbook\2026-07-05-30min-session-runbook.md`)
- [x] FB3 — runbook manifest + checker. (verify: `python -m pytest tests\test_field_feedback_runbook.py -q`)
- [x] FB4 — close gate and status sync. (verify: checker + quality preflight)

## 결정 로그

- 결정: runbook은 실제 회계사 피드백을 받기 전 운영 문서이므로 "검증 완료"가 아니라 "세션 운영 준비"로 표현한다.
- 결정: 기존 field-feedback questionnaire는 덮지 않고, incorporated review questions supplement를 함께 보여준다.
- 결정: checker는 파일 존재와 required section만 확인한다. 세션 자체의 성공 여부는 사람이 기록한다.
- 예상 사용자 소유 결정: 없음. 실제 피드백 대상 회계사 선정과 일정 조율은 병행 사용자 액션이다.

## 중단점

- 필수 입력 산출물이 누락되면 close하지 않는다.
- runbook이 고객자료 업로드나 기준서 원문 공유를 요구하면 close하지 않는다.
