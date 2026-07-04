# Accounting Intelligence Expansion

> Status: planned sequence
> Created: 2026-07-05
> Objective link: `docs/OBJECTIVE.md`

## 문제 정의

현재 PoC는 K-IFRS 기반 회계처리 초안을 꽤 만들 수 있음을 보여줬다. 하지만 회계사가 실제로 하는 일은
K-IFRS 문단 검색만으로 끝나지 않는다.

필요한 지식층은 최소한 다음을 포함한다.

- K-IFRS 기준서 본문
- KASB 질의회신/실무 적용 자료
- FSC/FSS 회계감독/질의회신/감리 관련 자료
- 외감법, 상법, 자본시장법 등 법령
- 한국공인회계사회/감사기준 관련 자료
- DART/OpenDART 공시, XBRL, 재무제표 데이터
- 회사 내부 회계정책, 계약서, TB, 조서
- 회계법인 public guide와 해설 자료(보조 자료, authoritative source 아님)

따라서 다음 큰 arc는 "특정 기준서 workflow를 더 하나 만드는 것"이 아니라, 회계 업무에 필요한
정보원을 지도화하고, 데이터화하고, 검색/근거/산출물 생성까지 연결하는 것이다.

## 실행 순서

### Horizon 1. RAG Quality Refresh

목표: 기존 K-IFRS RAG 자체 품질을 다시 측정하고, multi-source 확장 전에 검색/답변/eval gate를 단단하게 만든다.

왜 먼저 하는가:

- 새 정보원을 붙이기 전에 현재 검색 실패 양상을 알아야 한다.
- K-IFRS citation 품질이 흔들리면 다른 정보원을 붙여도 답변 신뢰도가 올라가지 않는다.
- 이후 ingestion pipeline의 회귀 테스트 기준선이 필요하다.

주요 산출물:

- 현재 품질 baseline report
- 질문 유형별 eval set gap
- chunk/retrieval failure taxonomy
- retrieval/answer policy upgrade proposal
- quality gate command set

### Horizon 2. Authority Source Map

목표: 회계 업무에 필요한 K-IFRS 외 정보원을 "권위 수준, 사용 목적, 수집 가능성, 저장 정책" 기준으로 분류한다.

정보원 후보:

- Primary: K-IFRS, 법령, 감사기준
- Interpretive: KASB/FSS 질의회신, 회계감독 자료
- Filing/data: DART/OpenDART, XBRL, 사업보고서, 감사보고서
- Client-private: 계약서, 회계정책서, TB, 조서
- Supporting: 회계법인 public guide, 교육자료, 기사

산출물:

- source catalog
- authority ranking
- copyright/storage policy
- ingestion feasibility matrix
- first 3 source connectors 후보

### Horizon 3. Multi-Source Ingestion Pipeline

목표: 다양한 회계 정보원을 fetch/parse/chunk/embed/index 할 수 있는 재사용 파이프라인을 만든다.

핵심 단계:

- source connector interface
- document metadata schema
- parser/OCR boundary
- chunking strategy by source type
- embedding namespace
- provenance/citation schema
- reindex command
- ingestion smoke test

산출물:

- source registry
- chunk manifest
- embedding/index manifest
- ingestion quality report
- public-safe sample fixtures

### Horizon 4. Multi-Authority RAG Runtime

목표: 질문 하나에 대해 K-IFRS, 법령, 질의회신, 공시 데이터를 각각 다른 권위와 역할로 사용해 답변한다.

필요한 기능:

- query routing by task type
- authority priority policy
- evidence grouping
- conflict handling
- answer composer
- citation coverage gate
- "근거 부족" 선언 policy

산출물:

- runtime routing policy
- answer schema
- conflict examples
- source-aware eval set
- regression tests

### Horizon 5. Workflow Rebuild on Richer Knowledge

목표: 1115/1116/1109 workflow를 multi-source RAG 위에서 다시 돌려본다.

검증 질문:

- K-IFRS 본문만 쓸 때보다 판단 초안이 좋아지는가?
- 질의회신/법령/공시가 들어오면 어떤 `NeedsHumanReview`가 줄어드는가?
- 재무제표/감사 분석 산출물이 실제 회사 데이터와 연결되는가?

산출물:

- rebuilt review pack
- source-aware memo
- DART-linked examples
- delta report

### Horizon 6. Real Case Feedback Loop

목표: 익명화된 실제 업무 사례를 입력받아 회계사가 피드백할 수 있는 루프를 만든다.

산출물:

- anonymized case intake schema
- reviewer feedback form
- correction capture format
- eval seed conversion
- product improvement backlog

## 우선순위 원칙

순서는 선택지가 아니라 의존성이다.

1. RAG 품질이 기준선이다.
2. 정보원 지도가 있어야 수집 대상을 고른다.
3. 수집/청킹/임베딩 파이프라인이 있어야 데이터화한다.
4. multi-authority runtime이 있어야 답변에 반영한다.
5. workflow를 다시 돌려야 업무 자동화 효과를 측정한다.
6. 실제 피드백 루프가 있어야 제품으로 간다.

