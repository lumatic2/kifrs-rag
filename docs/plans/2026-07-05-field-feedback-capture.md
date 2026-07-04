# Plan: Field Feedback Capture

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/field-feedback-capture.md`
> Status source: `phases/field-feedback-capture/index.json`

## 요약

이번 run은 회계사 세션 notes를 public-safe 구조로 기록하고, raw contract/customer data 없이 correction
후보만 feedback queue record로 변환하는 capture pipeline을 만든다. 실제 피드백을 받은 것으로
표현하지 않고, sample notes로 구조와 검증을 먼저 만든다.

## Step Tree

- [x] FC1 — horizon/phase/plan setup. (verify: `Test-Path docs\horizons\field-feedback-capture.md`)
- [x] FC2 — feedback notes capture contract. (verify: `python -m pytest tests\test_field_feedback_capture.py -q`)
- [x] FC3 — capture report command and sample package. (verify: `python scripts\field_feedback_capture.py --out docs\reports\field-feedback-capture`)
- [x] FC4 — close gate and status sync. (verify: focused tests + quality preflight)

## 결정 로그

- 결정: 실제 피드백이 아직 없으므로 sample notes는 "sample"로 명시한다.
- 결정: notes 전체를 queue로 넣지 않고, safe correction candidate만 queue record로 변환한다.
- 결정: raw contract, customer identifier, copied source body, private filing은 validation error로 막는다.
- 예상 사용자 소유 결정: 실제 reviewer 섭외와 세션 일정.

## 중단점

- notes schema가 protected payload 저장을 요구하면 close하지 않는다.
- sample capture를 실제 회계사 검증으로 오해하게 만드는 문구가 있으면 close하지 않는다.
