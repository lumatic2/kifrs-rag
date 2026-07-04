# Current Capability Map

> Date: 2026-07-05
> Purpose: 현재 구현된 것이 무엇인지, 무엇이 아직 아닌지, 다음 확장이 왜 필요한지 쉽게 설명한다.

## 한 줄 정의

지금 구현된 것은 완성 제품이 아니라 **K-IFRS RAG 위에 회계 판단 초안 생성기가 어디까지 올라갈 수
있는지 보여주는 로컬 PoC 스택**이다.

즉, "기준서를 검색해서 답한다"에서 멈추지 않고, 특정 회계 이슈에 대해 다음 산출물을 자동으로
만들어보는 데까지 확장했다.

- 판단 구조
- 분개 초안
- 주석 후보
- 검토 메모
- review pack
- 재무제표 후보
- 감사 분석 메모
- 데모 번들

## 구현된 층위

### 1. K-IFRS 검색/RAG 기반

이미 구현된 기반은 다음과 같다.

- 100개 기준서 / 8,328개 문단 인덱스
- lexical, semantic, hybrid, reranked, hierarchical 검색 계열
- `user_note_v2` runtime 및 legacy fallback
- public-safe source pack / quality preflight
- 기준서 원문과 임베딩은 비공개 로컬 데이터로 두고, 공개 레포에는 파이프라인과 평가 하네스만 둔다.

현재 한계:

- 최근 product PoC 작업은 RAG 자체 품질을 새로 끌어올린 것이 아니라, 기존 RAG 위에 workflow를 얹은 것이다.
- 질문 유형별 gold set, multi-query, authority ranking, citation conflict policy는 다시 점검해야 한다.

### 2. 회계자문형 판단 엔진

현재 가장 많이 확장된 축은 F-ACC, 즉 회계자문/회계처리 검토 업무다.

구현된 도메인:

- K-IFRS 1116 리스 review pack
- K-IFRS 1109 금융상품 review pack 및 hardening
- K-IFRS 1115 수익인식 엔진

각 도메인에서 만든 산출물:

- 입력 fixture schema
- 판단/분류 로직
- 측정표
- 분개 초안
- 주석 skeleton
- 검토 메모
- NeedsHumanReview 항목
- review pack

의미:

- 회계사가 바로 서명할 결과물이 아니라, 회계사가 검토할 수 있는 "결정준비 초안"이다.
- 사람이 해야 하는 판단은 `NeedsHumanReview`로 남긴다.

### 3. 공통 산출물 표면

도메인별 엔진을 따로 만든 뒤, 공통 산출물로 묶는 작업도 시작했다.

- disclosure checklist 공통 schema
- 재무상태표/손익/OCI/주석 후보 draft
- 감사 analytical procedure 메모
- demo PoC bundle

의미:

- "기준서 답변"에서 "업무 산출물"로 이동하기 시작했다.
- 다만 아직 실제 회사 자료, DART/XBRL, 감사조서, 회계법인 내부 template와 연결된 상태는 아니다.

## 아직 아닌 것

현재 구현된 것은 다음이 아니다.

- 회계법인에 바로 설치 가능한 production product
- K-IFRS 외 정보까지 포괄하는 accounting knowledge base
- 외감법, 상법, 자본시장법, 감사기준, KASB/FSS 질의회신까지 포함한 multi-authority RAG
- 임의 PDF/웹문서/공시를 자동 수집해 chunking/embedding/indexing하는 일반 ingestion system
- 실제 익명화 client case를 회계사가 검토한 검증 완료 사례

## 왜 다음 horizon이 RAG 품질이어야 하는가

지금까지는 workflow surface를 빠르게 늘렸다. 그 결과 "무엇을 만들 수 있는지"는 보이기 시작했지만,
아래 기반 품질 질문이 남았다.

- 검색이 회계 이슈별로 안정적인가?
- citation이 항상 충분하고 정확한가?
- K-IFRS 문단, user note, source pack 사이 우선순위가 명확한가?
- 답변이 기준서 문단을 놓치거나 엉뚱한 문단을 끌어오는 실패가 어디서 나는가?
- 새 정보원(KASB 질의회신, 감사기준, 법령, DART)을 붙여도 깨지지 않을 구조인가?

따라서 다음 순서는 "제품 포장"이 아니라 **RAG 품질 refresh -> 비IFRS 정보원 지도 -> multi-source
ingestion/RAG**가 맞다.

