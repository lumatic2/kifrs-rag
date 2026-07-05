# Horizon: RAG Reliability Revalidation

> Status: closed
> Created: 2026-07-05
> Sequence: `docs/horizons/accounting-intelligence-expansion.md`

## Goal

K-IFRS RAG를 다시 검증하고, opt-in repair retriever를 언제 default로 올릴 수 있는지 기준을 정한다.
이 horizon은 외부 회계사 outreach 없이 내부 평가, regression, public-safe evidence만으로 진행한다.

## Why First

남은 핵심 작업은 source 확장, parser hardening, product UX다. 하지만 이 셋은 모두 RAG가 흔들리지
않는다는 전제 위에 올라간다. 먼저 현재 K-IFRS 검색/인용/답변 품질을 다시 재고, 실패 유형과 승격
기준을 정해야 다음 horizon에서 데이터 소스를 늘려도 회귀를 판단할 수 있다.

## Milestones

### RR1. Baseline Inventory

현재 품질 관련 스크립트, 리포트, 테스트, 보호 데이터 의존성을 한 장으로 정리한다.

Deliverable:

- `docs/reports/2026-07-05-rr1-rag-baseline-inventory.md`

Acceptance:

- 실행 가능한 public-safe command와 private-data-dependent command가 분리되어 있다.
- 현재 default retriever와 opt-in repair retriever 상태가 설명되어 있다.
- 다음 milestone에서 돌릴 최소 검증 세트가 명확하다.

### RR2. Eval Matrix and Seed Coverage

질문 유형별 eval coverage를 다시 묶는다.

Deliverable:

- `docs/reports/2026-07-05-rr2-eval-matrix.md`

Acceptance:

- 기준서 직접 검색, 판단형 질문, workflow 질문, disclosure 질문, user_note 의존 질문이 분리되어 있다.
- 비공개 dogfood 본문 없이도 공개 가능한 seed/metadata만 남는다.

### RR3. Retrieval and Citation Diagnostics

현재 default와 opt-in retriever의 실패 유형을 비교한다.

Deliverable:

- `docs/reports/2026-07-05-rr3-retrieval-citation-diagnostics.md`

Acceptance:

- recall/citation/answer gate 결과가 한 표로 정리되어 있다.
- 실패 유형이 query wording, chunk boundary, term bridge, rerank, citation assembly 중 어디인지 분류된다.

### RR4. Repair Policy Candidate

default 변경 없이 opt-in repair path의 정책 후보를 정리한다.

Deliverable:

- code or policy patch
- `docs/reports/2026-07-05-rr4-repair-policy-candidate.md`

Acceptance:

- multi-query, task routing, citation coverage gate 중 무엇을 지금 적용하고 무엇을 보류할지 정해져 있다.
- default retriever guard가 계속 통과한다.

### RR5. Promotion Gate and Handoff

RAG 품질 horizon을 닫고 다음 horizon으로 넘길 기준을 정한다.

Deliverable:

- `docs/reports/2026-07-05-rr5-rag-promotion-gate.md`

Acceptance:

- default promotion 여부가 명시되어 있다.
- 다음 horizon인 non-IFRS source dataization에서 사용할 regression command가 정해져 있다.
- `python scripts\quality_preflight.py --format text`가 통과한다.

Evidence:

- `docs/reports/2026-07-05-rr5-rag-promotion-gate.md`

## Close Criteria

- K-IFRS RAG baseline, eval coverage, failure taxonomy, promotion criteria가 public-safe report로 남아 있다.
- default retriever 변경 여부가 명확하다.
- 다음 horizon에서 source를 늘려도 회귀를 판단할 수 있는 command set이 있다.

## Close Result

- Closed: 2026-07-05
- Default promotion: false
- Runtime default: `hybrid`
- Opt-in repair retriever: `ifrs1109_classification_hybrid`
- Next candidate horizon: `non-ifrs-source-dataization`
- Close report: `docs/reports/2026-07-05-rag-reliability-revalidation-close-report.md`
