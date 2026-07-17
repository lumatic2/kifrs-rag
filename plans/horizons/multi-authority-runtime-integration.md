# Horizon: Multi-Authority Runtime Integration

> Status: closed
> Created: 2026-07-05
> Sequence: `docs/horizons/accounting-intelligence-expansion.md`
> Previous: `docs/horizons/multi-source-ingestion-pipeline.md`

## Goal

ingestion/evidence manifest를 실제 회계 workflow runtime에서 쓸 수 있게 연결한다. F-ACC review pack,
statement draft, answer composer가 K-IFRS primary evidence와 external supporting/fact evidence를 구분해
표시하는 것이 목표다.

## Why next

`multi-source-ingestion-pipeline`은 외부 자료를 안전하게 담고 검증하는 skeleton을 만들었다. 그러나 아직
workflow runtime은 그 evidence를 읽거나 산출물에 표시하지 않는다. 다음 단계는 안전한 manifest를 실제
회계 업무 산출물에 연결하는 것이다.

## Candidate Milestones

### RT1. Runtime Evidence Loader

source/evidence manifest를 validated runtime evidence objects로 변환한다.

Deliverable:

- runtime evidence dataclasses
- loader/query helpers
- tests

### RT2. Review-Pack Evidence Panel

1116/1109/1115 review pack에 external evidence section을 붙인다.

Deliverable:

- review pack evidence panel
- markdown/json rendering tests

### RT3. Statement Draft Fact Evidence Hook

statement draft 후보가 structured fact evidence를 참조할 수 있게 한다.

Deliverable:

- statement line candidate evidence references
- synthetic fact linkage tests

### RT4. Answer Boundary Composer

primary K-IFRS evidence, supporting interpretation, legal boundary, fact evidence를 답변에서 분리한다.

Deliverable:

- boundary rendering helper
- answer convention tests

### RT5. Runtime Close Demo

하나의 회계 업무 시나리오에서 K-IFRS evidence + external metadata + synthetic fact evidence를 함께 보여준다.

Deliverable:

- runtime demo report
- close gate
