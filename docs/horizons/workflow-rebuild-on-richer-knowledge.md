# Horizon: Workflow Rebuild on Richer Knowledge

> Status: closed
> Created: 2026-07-05
> Sequence: `docs/horizons/accounting-intelligence-expansion.md`
> Previous: `docs/horizons/multi-authority-runtime-integration.md`

## Goal

기존 1109/1115/1116 F-ACC review pack을 multi-authority runtime evidence 위에서 다시 훑고,
K-IFRS citation, 외부 근거 metadata, synthetic fact evidence, 사람 검토 항목이 업무 산출물에
어떻게 반영되는지 측정한다.

## Why next

Horizon 1~4는 품질 기준선, 정보원 지도, ingestion manifest, runtime evidence 표시까지 만들었다.
하지만 Objective가 묻는 것은 "회계 업무가 얼마나 자동화되는가"이다. 따라서 다음 단계는 정보원
레이어가 review pack, 재무제표 후보, 감사 분석 같은 업무 산출물에 실제로 어떤 차이를 만드는지
보여주는 것이다.

## Milestones

### WR1. Source-Aware Rebuild Plan and Phase Setup

`workflow-rebuild-on-richer-knowledge` phase를 만들고, source-aware rebuild가 측정할 범위를 정한다.

Deliverable:

- `phases/workflow-rebuild-on-richer-knowledge/`
- `docs/horizons/workflow-rebuild-on-richer-knowledge.md`

Acceptance:

- 1109/1115/1116 review pack을 모두 포함한다.
- 보호 본문 없이 metadata/synthetic fixture만 사용한다.
- 사람 검토 항목은 제거하지 않고 "남는 판단"으로 계량한다.

### WR2. Source-Aware Review Pack Analyzer

review pack 객체들을 공통 summary로 변환해 citation/evidence/human-review coverage를 측정한다.

Deliverable:

- `kifrs/workflows/source_aware_rebuild.py`
- `tests/test_source_aware_rebuild.py`

Acceptance:

- 1109/1115/1116 pack 모두 분석 가능하다.
- external evidence role별 count를 유지한다.
- raw source body/text/content 필드를 출력하지 않는다.

### WR3. Rebuild Report Command

source-aware rebuild 결과를 markdown report로 만든다.

Deliverable:

- `scripts/workflow_rebuild_report.py`
- `docs/reports/2026-07-05-wr3-source-aware-rebuild-report.md`

Acceptance:

- command 하나로 report를 재생성할 수 있다.
- report는 자동화 상태, citation count, external evidence role, fact evidence, 사람 검토 항목을 표로 보여준다.
- report는 데모/피드백 패키지에서 참조 가능한 public-safe 문서다.

### WR4. Close Gate

관련 테스트와 public-safe gate를 통과시키고 ROADMAP/OBJECTIVE 상태를 정리한다.

Deliverable:

- `docs/reports/2026-07-05-wr4-workflow-rebuild-close-report.md`

Acceptance:

- source-aware rebuild tests pass.
- 기존 review pack/demo tests pass.
- `quality_preflight.py` public-safe gate passes.
- ROADMAP이 다음 horizon 후보를 가리킨다.
