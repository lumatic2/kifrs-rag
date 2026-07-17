# Horizon: Toolkit Packaging Readiness

> Status: closed
> Created: 2026-07-05
> Sequence: `docs/horizons/accounting-intelligence-expansion.md`
> Previous: `docs/horizons/feedback-eval-backlog-integration.md`

## Goal

회계법인 소개/PoC 전에 로컬 도구킷을 설치·실행·demo 재현 가능한 상태로 설명하고 검증하는 readiness
package를 만든다.

## Why next

Accounting Intelligence Expansion은 source-aware demo, anonymized intake, reviewer correction, eval/backlog
queue까지 이어졌다. 다음 병목은 "다른 사람이 무엇을 실행하면 같은 demo와 gate를 볼 수 있는가"이다.
이 horizon은 실제 릴리스를 만들기 전에 설치/실행/검증 절차와 산출물 경계를 명확히 한다.

## Milestones

### TK1. Readiness Manifest

도구킷에 필요한 공개 산출물, 재생성 command, protected-data boundary를 manifest로 정의한다.

Deliverable:

- `docs/toolkit/readiness_manifest.json`
- `docs/toolkit/README.md`

Acceptance:

- demo, workflow rebuild, feedback queue, quality preflight command가 포함된다.
- protected assets are excluded 문구가 포함된다.

### TK2. Readiness Checker

manifest를 읽어 파일 존재, command 실행, public-safe gate를 확인한다.

Deliverable:

- `scripts/toolkit_readiness.py`
- `tests/test_toolkit_readiness.py`

Acceptance:

- 기본 sample manifest가 통과한다.
- missing file/failed command를 실패로 표시한다.
- protected asset path가 required artifact로 들어오면 실패한다.

### TK3. Readiness Report

readiness checker 결과를 markdown report로 생성한다.

Deliverable:

- `docs/reports/2026-07-05-tk3-toolkit-readiness-report.md`

Acceptance:

- command 하나로 report를 재생성한다.
- PASS/FAIL/SKIP 결과와 다음 action을 보여준다.

### TK4. Close Gate

tests, readiness report, quality preflight, ROADMAP/OBJECTIVE sync를 끝낸다.

Deliverable:

- `docs/reports/2026-07-05-tk4-toolkit-readiness-close-report.md`

Acceptance:

- readiness tests pass.
- readiness command passes.
- `quality_preflight.py` public-safe gate passes.
