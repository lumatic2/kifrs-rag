# Horizon: RAG Quality Refresh

> Status: active
> Created: 2026-07-05
> Sequence: `docs/horizons/accounting-intelligence-expansion.md`

## Goal

K-IFRS RAG 자체 품질을 현재 상태에서 다시 검증하고, K-IFRS 외 정보원 확장 전에 검색/답변/eval
기반을 단단하게 만든다.

## Why now

F-ACC sequence는 RAG 위에 업무 workflow를 얹어 "산출물 초안"을 만들었다. 하지만 다음 단계는
KASB/FSS 질의회신, 감사기준, 법령, DART 같은 비IFRS 정보원을 붙이는 일이다. 그러려면 현재
K-IFRS RAG가 어디서 잘 되고 어디서 흔들리는지 먼저 알아야 한다.

## Milestones

### RQ1. Current Quality Baseline

현재 품질 스크립트, gold/eval 데이터, 최근 demo scenario를 한 번에 훑어 baseline report를 만든다.

Deliverable:

- `docs/reports/2026-07-05-rq1-current-quality-baseline.md`

Acceptance:

- 현재 실행 가능한 quality/eval/test command 목록을 정리한다.
- public-safe로 돌릴 수 있는 것과 private data가 필요한 것을 분리한다.
- 실패/경고가 있으면 원인을 추적 대상에 올린다.

### RQ2. Eval Coverage Refresh

질문 유형별 평가 coverage를 다시 분류한다.

Coverage buckets:

- 기준서 문단 직접 검색
- 문단 조합/판단 질문
- workflow seed 질문
- disclosure 질문
- citation 부족/충돌 질문
- source pack/user note 의존 질문

Deliverable:

- `docs/reports/2026-07-05-rq2-eval-coverage-refresh.md`

### RQ3. Retrieval Failure Taxonomy

검색 실패를 유형화한다.

Failure buckets:

- query wording miss
- section/chapter boundary miss
- term bridge miss
- rerank miss
- chunk granularity miss
- citation assembly miss
- user note/source pack priority miss

Deliverable:

- `docs/reports/2026-07-05-rq3-retrieval-failure-taxonomy.md`

### RQ4. Retrieval/Answer Policy Upgrade

multi-source RAG로 가기 전 K-IFRS runtime policy를 정리하고 필요한 최소 구현을 한다.

Candidate upgrades:

- multi-query decomposition
- task-type routing
- authority/source priority
- citation coverage gate
- evidence grouping
- "근거 부족" 선언

Deliverable:

- code or policy patch
- regression tests
- `docs/reports/2026-07-05-rq4-policy-upgrade.md`

### RQ5. Quality Gate Report

다음 horizon인 authority source map / ingestion으로 넘어갈 수 있는 품질 gate를 문서화한다.

Deliverable:

- `docs/reports/2026-07-05-rq5-quality-gate-report.md`

Acceptance:

- 어떤 command를 매번 돌릴지 정해져 있다.
- 어떤 failure가 release blocker인지 정해져 있다.
- 다음 horizon에서 source ingestion을 시작해도 되는 최소 조건이 적혀 있다.

