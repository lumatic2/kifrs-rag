# Horizon: Authority Source Map

> Status: active
> Created: 2026-07-05
> Sequence: `docs/horizons/accounting-intelligence-expansion.md`
> Previous: `docs/horizons/rag-quality-refresh.md`

## Goal

K-IFRS 외 회계 업무 정보원을 권위 수준, 사용 목적, 저작권/저장 정책, ingestion 가능성, citation policy
기준으로 catalog화한다.

## Why now

`rag-quality-refresh`에서 K-IFRS RAG의 현재 품질 gate가 정리됐다. 이제 다음 문제는 "무슨 자료를
RAG에 넣을 것인가"다. 회계 업무에는 기준서 본문뿐 아니라 질의회신, 법령, 감사기준, 공시, 고객 내부
자료가 필요하다. 이들을 같은 weight로 섞으면 답변 신뢰도가 떨어지므로 source map이 먼저 필요하다.

## Milestones

### AS1. Source Taxonomy

K-IFRS 외 정보원을 source class로 나누고 각 class의 RAG 역할을 정의한다.

Deliverable:

- `docs/reports/2026-07-05-as1-source-taxonomy.md`

Status: complete. Seven source classes are fixed and checked by `scripts/authority_source_taxonomy_check.py`.

### AS2. Authority and Citation Policy

source class별 authority priority와 답변 citation 방식을 정한다.

Deliverable:

- `docs/reports/2026-07-05-as2-authority-citation-policy.md`

### AS3. Copyright and Storage Boundary

무엇을 공개 repo에 둘 수 있고, 무엇을 local/private namespace에 둬야 하는지 정한다.

Deliverable:

- `docs/reports/2026-07-05-as3-storage-boundary.md`

Status: complete. Storage labels are fixed and checked against ingestion manifest policy by
`scripts/authority_storage_boundary_check.py`.

### AS4. Ingestion Feasibility Matrix

각 source class를 fetch/parse/chunk/embed/index 가능성 기준으로 평가한다.

Deliverable:

- `docs/reports/2026-07-05-as4-ingestion-feasibility.md`

### AS5. First Connector Recommendation

multi-source ingestion pipeline에서 먼저 구현할 source connector 1~3개를 정한다.

Deliverable:

- `docs/reports/2026-07-05-as5-first-connector-recommendation.md`

## Close Criteria

- source class별 authority, use, storage, ingestion feasibility가 표로 정리되어 있다.
- 다음 horizon(`multi-source-ingestion-pipeline`)에서 바로 connector interface를 설계할 수 있다.
- public/private boundary가 분리되어 있다.
