# Horizon: Real Case Feedback Loop

> Status: closed
> Created: 2026-07-05
> Sequence: `docs/horizons/accounting-intelligence-expansion.md`
> Previous: `docs/horizons/workflow-rebuild-on-richer-knowledge.md`

## Goal

익명화된 실제 업무 사례를 안전하게 intake하고, review pack routing 후보와 회계사 correction을
구조화해 eval seed/backlog로 전환할 수 있는 feedback loop를 만든다.

## Why next

Field feedback package는 회계사에게 보여줄 demo 자료를 만들었고, workflow rebuild는 1109/1115/1116
review pack의 source coverage를 계량했다. 다음 제품 리스크는 "실제 사례가 들어오면 무엇을 어떻게
받고, 무엇을 저장하지 않으며, 회계사 피드백을 어떻게 개선 항목으로 남기는가"이다.

## Milestones

### RC1. Anonymized Case Intake Schema

실제 사례를 보호자료 없이 구조화하기 위한 intake schema와 validator를 만든다.

Deliverable:

- `kifrs/feedback/case_intake.py`
- `tests/test_real_case_feedback.py`

Acceptance:

- raw contract/body/customer identifiers를 금지한다.
- 1109/1115/1116 후보 routing에 필요한 최소 사실만 받는다.
- public-safe sample intake가 validation을 통과한다.

### RC2. Reviewer Correction Capture

회계사 피드백을 점수/수정/누락자료/다음 액션으로 구조화한다.

Deliverable:

- correction dataclass and validator
- markdown summary renderer

Acceptance:

- reviewer correction은 원문 본문 없이 issue, severity, correction, evidence need를 저장한다.
- correction을 eval seed 후보 또는 backlog 후보로 분류할 수 있다.

### RC3. Case-to-Review-Pack Routing Stub

intake된 사례를 현재 지원 가능한 review pack domain으로 routing한다.

Deliverable:

- routing candidate function
- unsupported-domain reason

Acceptance:

- 1109/1115/1116 후보를 구분한다.
- 세무/Deal/내부자료 의존 사례는 out-of-scope로 남긴다.

### RC4. Feedback Loop Report and Close Gate

public-safe sample case와 reviewer correction을 report로 묶고 close gate를 통과한다.

Deliverable:

- `docs/reports/2026-07-05-rc4-real-case-feedback-loop-report.md`

Acceptance:

- tests pass.
- `quality_preflight.py` public-safe gate passes.
- ROADMAP/OBJECTIVE가 다음 후보를 가리킨다.
