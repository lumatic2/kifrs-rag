# Real Accountant Session Packet

> Date: 2026-07-05
> Status: ready to schedule, not completed feedback evidence

## Purpose

실제 회계사 1명에게 Accounting Intelligence toolkit을 30분 동안 보여주고, 제품이 실제 검토 시간을 줄일
수 있는지와 위험한 부분이 무엇인지 기록한다.

## Packet Files

| File | Role |
|---|---|
| `2026-07-05-session-invite.md` | reviewer에게 보낼 초대/설명 문구 |
| `2026-07-05-session-evidence-template.md` | 세션 후 public-safe notes 기록 템플릿 |
| `session_manifest.json` | 세션 준비 상태와 실제 evidence 여부 |

## Files to Open During Session

1. `docs/reports/firm-facing-poc/2026-07-05-one-page-brief.md`
2. `docs/reports/field-feedback-runbook/2026-07-05-30min-session-runbook.md`
3. `docs/reports/demo-poc/MANIFEST.md`
4. `docs/reports/real-transaction-poc/INDEX.md`
5. `docs/reports/field-feedback-capture/INDEX.md`
6. `docs/reports/field-feedback/2026-07-05-feedback-questionnaire.md`
7. `docs/reports/field-feedback/2026-07-05-incorporated-review-questions.md`

## Before Sending

- Reviewer에게 실제 고객자료나 계약 원문을 보내지 말라고 말한다.
- 세션 목적이 도입 결정이 아니라 제품 검증임을 말한다.
- 익명화 거래는 structured facts card로만 받을 수 있다고 말한다.
- 세션 후 notes는 public-safe correction 후보만 queue로 변환한다고 말한다.

## Completion Boundary

이 packet은 세션 준비 산출물이다. 아래가 생기기 전에는 `real-accountant-session` horizon을 close하지 않는다.

- actual reviewer metadata
- actual public-safe feedback notes
- actual capture manifest with `actual_feedback_evidence: true`
- safe feedback queue records generated from the actual notes
