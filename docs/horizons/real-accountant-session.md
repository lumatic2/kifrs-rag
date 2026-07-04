# Horizon: Real Accountant Session

> Status: active
> Created: 2026-07-05
> Sequence: `docs/horizons/accounting-intelligence-expansion.md`
> Previous: `docs/horizons/field-feedback-capture.md`

## Goal

실제 회계사 1명과 `field-feedback-runbook`으로 세션을 운영하고, public-safe notes를 capture pipeline에
넣어 queue record로 변환한다.

## Why next

`field-feedback-capture`까지는 sample notes였다. 제품 objective의 중간 관문은 "현업 회계사 1명 이상이
실제 업무 사례를 이 도구로 처리해보고 피드백을 남겼다"이므로, 이제 외부 reviewer와 실제 세션 증거가
필요하다.

## Milestones

### RS1. Session Packet Prep

Deliverable:

- `docs/reports/real-accountant-session/SESSION_PACKET.md`
- `docs/reports/real-accountant-session/2026-07-05-session-invite.md`
- `docs/reports/real-accountant-session/2026-07-05-session-evidence-template.md`
- `docs/reports/real-accountant-session/session_manifest.json`

Acceptance:

- invite, session prep, evidence template가 실제 reviewer에게 보낼 수 있는 형태다.
- packet은 actual feedback evidence가 아직 없음을 명시한다.

Status: completed (2026-07-05)

### RS2. Run Actual Session

Deliverable:

- 실제 회계사 세션 notes
- reviewer role/service-line metadata
- public-safe correction 후보

Acceptance:

- raw contract/customer identifier 없이 notes가 남는다.
- reviewer가 실제 회계사 또는 회계 실무 검토 가능한 사람임이 metadata로 표시된다.

Status: pending external reviewer

### RS3. Capture and Queue Conversion

Deliverable:

- `field_feedback_capture.py` 또는 직접 API로 생성한 actual capture package
- queue record candidate

Acceptance:

- `actual_feedback_evidence`가 true인 manifest는 실제 세션 notes가 있을 때만 생성한다.
- safe correction만 queue로 변환된다.

Status: pending

### RS4. Close Gate

Deliverable:

- close report

Acceptance:

- actual session evidence exists.
- quality preflight remains public-safe.
- ROADMAP/OBJECTIVE가 실제 feedback 관문 달성 여부를 반영한다.

Status: pending
