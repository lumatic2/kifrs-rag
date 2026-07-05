# Horizon: Multi-Authority Runtime Hardening

> Status: active
> Created: 2026-07-05
> Sequence: `docs/horizons/accounting-intelligence-expansion.md`
> Previous: `docs/horizons/non-ifrs-source-dataization.md`

## Goal

K-IFRS primary evidence, KASB/FSS-style supporting interpretation, law locator, DART/OpenDART-style structured fact,
and client-private local fact를 runtime에서 섞지 않고 분리해 읽고 표시하게 만든다.

이 horizon은 "source를 데이터화했다"에서 끝나지 않고, 실제 회계 workflow output이 그 source들을 권위별로
구분해 쓸 수 있게 만드는 단계다. 최종 목표는 review pack, statement draft, answer composer, close demo가
모두 같은 authority boundary를 따르는 것이다.

## Why Now

`non-ifrs-source-dataization`은 네 source lane을 public-safe record, fixture, chunk/index policy, gate로
닫았다. 하지만 runtime이 아직 그 계약을 업무 산출물에 안정적으로 반영하는 단계는 아니다.

- K-IFRS 문단은 회계처리 판단의 primary evidence로 유지되어야 한다.
- 해석자료/감독자료 metadata는 supporting interpretation일 뿐 primary evidence가 아니다.
- 법령 locator는 legal boundary로 분리되어야 한다.
- DART/OpenDART-style 수치는 fact evidence로만 쓰여야 한다.
- client-private fact는 local-only context로 표시되어야 한다.

## Milestones

### MAH1. Runtime Evidence Boundary Audit

현재 runtime evidence loader, evidence panel, review pack, statement draft, answer boundary가 source authority를
어떻게 다루는지 감사한다.

Deliverable:

- `docs/reports/2026-07-05-mah1-runtime-evidence-boundary-audit.md`

Acceptance:

- 기존 runtime evidence code와 tests가 어떤 authority role을 지원하는지 표로 정리되어 있다.
- NIS handoff contract와 현재 runtime 사이 gap이 분류되어 있다.
- MAH2~MAH5에서 보강할 code/test surface가 명확하다.

### MAH2. Runtime Evidence Contract Hardening

NIS source records와 기존 evidence manifest를 runtime evidence object로 안전하게 변환하는 contract를 보강한다.

Deliverable:

- `kifrs/runtime/authority_boundary.py`
- `tests/test_runtime_authority_boundary.py`
- `docs/reports/2026-07-05-mah2-runtime-evidence-contract.md`

Acceptance:

- primary/supporting/legal/fact/client-private role이 runtime object에서 분리된다.
- K-IFRS primary evidence와 non-IFRS supporting/fact evidence가 같은 field로 합쳐지지 않는다.
- forbidden/protected body field가 runtime reference에도 나타나지 않는다.

### MAH3. Review Pack Authority Panel

1116/1109/1115 review pack markdown/json에 authority-separated evidence panel을 붙인다.

Deliverable:

- review pack authority panel helper
- tests for 1116/1109/1115 panel rendering
- `docs/reports/2026-07-05-mah3-review-pack-authority-panel.md`

Acceptance:

- review pack에 K-IFRS primary evidence와 외부 supporting/legal/fact/client-private evidence가 별도 section으로 표시된다.
- 외부 source가 회계처리 결론을 단독 대체하지 않는다는 boundary가 산출물에 남는다.
- 기존 review pack regression이 깨지지 않는다.

### MAH4. Statement Draft and Analytics Fact Hook

statement draft와 audit analytics 쪽에서 structured fact evidence를 참조할 수 있게 한다.

Deliverable:

- structured fact evidence hook
- statement draft/audit analytics linkage tests
- `docs/reports/2026-07-05-mah4-structured-fact-runtime-hook.md`

Acceptance:

- structured fact는 calculation/fact evidence로만 연결되고 primary accounting authority로 승격되지 않는다.
- statement line candidate 또는 audit metric이 evidence reference를 보유한다.
- synthetic fixture만 사용하며 raw filing payload는 필요 없다.

### MAH5. Authority Composer Gate and Runtime Demo

authority-separated runtime을 하나의 demo와 gate로 닫는다.

Deliverable:

- answer/authority composer helper
- `scripts/multi_authority_runtime_gate.py`
- `tests/test_multi_authority_runtime_gate.py`
- `docs/reports/2026-07-05-mah5-runtime-demo-gate.md`
- `docs/reports/2026-07-05-multi-authority-runtime-hardening-close-report.md`

Acceptance:

- 하나의 demo output에서 K-IFRS primary, supporting interpretation, legal boundary, fact evidence, client-private placeholder가 분리 표시된다.
- `python scripts\multi_authority_runtime_gate.py --format text`가 통과한다.
- NIS dataization gate와 RAG reliability regression command가 계속 통과한다.

## Close Criteria

- Runtime evidence object가 authority role별로 분리되어 있다.
- Review pack/statement draft/answer composer가 같은 authority boundary를 따른다.
- K-IFRS default retriever는 변경하지 않는다.
- Public repo에는 metadata/schema/synthetic fixture/reference만 남고 protected body는 남지 않는다.
- 다음 horizon `client-private-parser-runtime`으로 넘길 때 private local fact boundary가 명확하다.

## Decision Log

- K-IFRS paragraph evidence는 primary evidence로 유지한다.
- Non-IFRS source는 supporting interpretation, legal boundary, fact evidence, client-private fact로 분리한다.
- 이 horizon은 live connector/API 호출이나 real client file parsing을 하지 않는다.
- Default retriever promotion은 이 horizon 범위 밖이다.
- 사용자 소유 결정: 현재 없음.
