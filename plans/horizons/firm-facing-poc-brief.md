# Horizon: Firm-Facing PoC Brief

> Status: closed
> Created: 2026-07-05
> Sequence: `docs/horizons/accounting-intelligence-expansion.md`
> Previous: `docs/horizons/toolkit-packaging-readiness.md`

## Goal

회계법인에 보여줄 PoC 설명 패키지를 만든다. 대상은 회계자문/F-S support 팀을 1순위로 두고,
감사팀은 회계이슈 검토와 주석 요구사항 대사 보조 적용처로 설명한다.

## Why next

`toolkit-packaging-readiness`는 로컬 도구킷이 공개 산출물과 재현 명령 기준으로 실행 가능한지
확인했다. 하지만 회계법인 미팅에서는 "무엇을 설치할 수 있는가"보다 "어느 팀의 어떤 일을 줄이는가",
"무엇을 보여줄 수 있는가", "PoC에서 무엇을 요청하는가"가 먼저 필요하다.

이 horizon은 기존 company/service-line map, field feedback package, demo PoC, readiness checker를
하나의 firm-facing narrative로 묶는다.

## Milestones

### PB1. Horizon and Phase Setup

`firm-facing-poc-brief`를 실제 active horizon으로 열고 phase plan을 만든다.

Deliverable:

- `docs/horizons/firm-facing-poc-brief.md`
- `phases/firm-facing-poc-brief/index.json`
- `phases/firm-facing-poc-brief/step1.md` ~ `step4.md`

Acceptance:

- ROADMAP/OBJECTIVE가 active horizon을 가리킨다.
- phase index가 PB1~PB4를 포함한다.

Status: completed (2026-07-05)

### PB2. PoC Brief

회계법인 담당자가 읽고 "우리 팀에서 어떤 PoC를 해볼지" 판단할 수 있는 본문 브리프를 작성한다.

Deliverable:

- `docs/reports/firm-facing-poc/2026-07-05-poc-brief.md`

Acceptance:

- target team, problem, current proof, demo path, risk boundary, PoC ask가 포함된다.
- F-ACC를 1순위, F-AUD를 보조 적용처로 설명한다.

Status: completed (2026-07-05)

### PB3. One-Page Brief and Index

미팅 전송용 1페이지 요약과 폴더 index를 만든다.

Deliverable:

- `docs/reports/firm-facing-poc/2026-07-05-one-page-brief.md`
- `docs/reports/firm-facing-poc/INDEX.md`

Acceptance:

- 10분 소개 흐름과 30분 데모 흐름이 분리되어 있다.
- 다음 요청사항이 3개 이하로 정리되어 있다.

Status: completed (2026-07-05)

### PB4. Close Gate

브리프가 기존 readiness/demo/feedback 산출물과 연결되는지 검증하고 close report를 남긴다.

Deliverable:

- `docs/reports/2026-07-05-pb4-firm-facing-poc-brief-close-report.md`

Acceptance:

- toolkit readiness and quality preflight pass.
- protected source data boundary를 위반하는 문구가 없다.
- ROADMAP/OBJECTIVE가 다음 horizon을 제안한다.

Status: completed (2026-07-05)
