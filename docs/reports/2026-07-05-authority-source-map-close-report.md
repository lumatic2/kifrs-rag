# Authority Source Map Close Report

> Horizon: `authority-source-map`
> Date: 2026-07-05
> Status: closed

## 한 줄 결론

K-IFRS 외 회계 업무 정보원은 이제 `source_class`, authority/citation role, storage policy, ingestion lane,
first connector 후보까지 한 번에 설명할 수 있다. 다음 구현 horizon은 `multi-source-ingestion-pipeline`이다.

## 무엇이 됐나

### 1. Source class가 고정됐다

AS1에서 7개 source class를 정했다.

- `primary_accounting_standard`
- `interpretive_accounting_material`
- `primary_audit_standard`
- `law_regulation`
- `filing_data`
- `client_private`
- `supporting_material`

의미: 앞으로 RAG evidence는 raw retrieval score로만 섞지 않고, 이 class별 역할에 따라 답변에 배치한다.

### 2. Authority와 citation policy가 분리됐다

AS2에서 질문 유형별 우선순위를 정했다.

- 회계처리 질문: K-IFRS primary evidence가 먼저다.
- 감사 workflow 질문: audit authority가 필요하다.
- 법적/procedural 질문: law/regulation locator가 필요하다.
- 회사 수치 질문: filing/client fact가 factual evidence다.

의미: FSS/KASB 자료나 DART 수치는 답변을 풍부하게 만들 수 있지만, K-IFRS 회계처리 결론을 단독으로
대체하지 않는다.

### 3. Public/private storage boundary가 고정됐다

AS3에서 공개 repo 허용 범위를 정했다.

공개 repo 허용:

- metadata
- schema
- code
- aggregate metrics
- synthetic fixture
- author-written notes

공개 repo 금지:

- 기준서 본문
- 외부 문서 본문
- 법령/질의회신/guide 복사문
- DB dump
- embeddings
- client-private 자료

의미: 다음 ingestion 구현은 처음부터 `body_storage_policy`를 가져야 한다.

### 4. Ingestion lane이 갈라졌다

AS4에서 하나의 parser로 해결하지 않기로 했다.

- `document_rag`: K-IFRS, KASB/FSS, audit standard, law locator
- `structured_data`: DART/OpenDART/XBRL/재무제표 수치
- `local_private_case_facts`: 계약서, TB, 회계정책, 조서
- `metadata_support_only`: 보조 자료, public guide, 기사

의미: 문서 RAG와 structured fact retrieval은 처음부터 다른 record type으로 간다.

### 5. 첫 connector 후보가 정해졌다

AS5에서 다음 horizon의 첫 구현 후보를 3개로 좁혔다.

1. `kasb-fss-interpretive-catalog`
2. `opendart-structured-financials`
3. `law-regulation-locator`

보류:

- `audit-standards-namespace`
- `client-private-case-intake`
- `firm-public-guides`

의미: 다음 구현은 모든 source를 한 번에 붙이지 않고, metadata-only document source와 structured fact source를
먼저 구현한다.

## Verification

Commands:

```powershell
python scripts\authority_source_taxonomy_check.py --format text
python scripts\authority_storage_boundary_check.py --format text
python scripts\authority_ingestion_feasibility_check.py --format text
python scripts\authority_connector_recommendation_check.py --format text
python scripts\quality_preflight.py --format text
```

Expected result:

- all authority-source-map checkers return `ok: True`
- `quality_preflight.py` returns `ok: True` and `public_safe: True`

## Next Horizon

`multi-source-ingestion-pipeline`

Suggested milestone order:

1. MSI1 — connector contract and source manifest
2. MSI2 — metadata-only document catalog prototype
3. MSI3 — structured fact fixture prototype
4. MSI4 — provenance and citation manifest
5. MSI5 — ingestion gate and close report

## Close Decision

`authority-source-map` is closed. It answered:

- 어떤 정보원이 필요한가
- 어떤 권위로 쓰이는가
- 어디까지 저장 가능한가
- 어떤 ingestion lane으로 들어가는가
- 무엇부터 구현할 것인가

It did not implement fetchers, body ingestion, API calls, schema migration, or client-private intake. Those belong to
the next horizon.
