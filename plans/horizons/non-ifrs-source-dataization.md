# Horizon: Non-IFRS Source Dataization

> Status: closed
> Created: 2026-07-05
> Sequence: `docs/horizons/accounting-intelligence-expansion.md`
> Previous: `docs/horizons/rag-reliability-revalidation.md`

## Goal

K-IFRS 기준서 RAG 밖의 회계 업무 정보원을 실제 RAG 데이터 단위로 바꾼다. 대상은 KASB/FSS/FSC
해석 자료, 법령 locator, DART/OpenDART structured facts, 그리고 client-private local facts의 경계다.

이 horizon의 핵심은 "자료를 많이 긁기"가 아니라, 각 source를 어떤 권위와 저장 정책으로 다루고,
어떤 record/chunk/embedding/retrieval 단위로 넘길지 정하는 것이다.

## Why Now

`rag-reliability-revalidation`은 K-IFRS RAG baseline과 promotion gate를 닫았다. 다음 병목은 IFRS 본문만으로
답할 수 없는 회계 업무다.

- 실무 질의는 K-IFRS 문단 외에 해석 자료, 감독 자료, 법령, 공시 수치, client fact가 필요하다.
- 이전 `authority-source-map`과 `multi-source-ingestion-pipeline`은 source class와 public-safe manifest
  skeleton을 만들었지만, 실제 RAG runtime이 쓸 dataization 단위와 regression contract는 아직 느슨하다.
- 다음 `multi-authority-runtime-hardening`으로 가려면 먼저 source별 record type, chunk policy, citation role,
  private/public boundary를 기계적으로 검증할 수 있어야 한다.

## Milestones

### NIS1. Existing Source Asset Inventory

흩어진 source-map, ingestion, connector, parser 산출물을 inventory로 묶고 무엇을 재사용/폐기/보강할지 정한다.

Deliverable:

- `docs/reports/2026-07-05-nis1-source-asset-inventory.md`

Acceptance:

- 기존 source 관련 scripts, reports, fixtures, manifests가 source lane별로 분류되어 있다.
- 재사용할 산출물과 새로 만들 산출물이 분리되어 있다.
- 보호 본문, DB dump, embeddings, API key가 필요한 항목은 active 구현 범위에서 제외되어 있다.

### NIS2. Source Record Contract

문서형 source, 법령 locator, structured fact, private fact를 같은 RAG pipeline에 넘기기 위한 record contract를
정의한다.

Deliverable:

- `kifrs/ingestion/source_record.py`
- `tests/test_source_record_contract.py`
- `docs/reports/2026-07-05-nis2-source-record-contract.md`

Acceptance:

- record type별 필수 필드와 forbidden fields가 검증된다.
- `body_storage_policy`, `citation_role`, `authority_level`, `retrieval_lane`이 record에 포함된다.
- public fixture는 본문 없이 통과하고, body-like field는 실패한다.

### NIS3. Dataization Fixtures and Validators

각 source lane을 public-safe synthetic/metadata fixture로 만든다.

Deliverable:

- `docs/ingestion/non_ifrs_source_records.example.json`
- `scripts/validate_non_ifrs_source_records.py`
- `tests/test_non_ifrs_source_records.py`
- `docs/reports/2026-07-05-nis3-dataization-fixtures.md`

Acceptance:

- KASB/FSS-style metadata document, law locator, OpenDART-like structured fact, client-private placeholder fixture가 있다.
- fixture는 public-safe gate를 통과한다.
- protected body, raw XML dump, credential, embedding field는 실패한다.

### NIS4. Chunking and Embedding Plan

source lane별 chunking, embedding, indexing 정책을 코드가 읽을 수 있는 plan으로 고정한다.

Deliverable:

- `docs/ingestion/non_ifrs_chunking_policy.json`
- `scripts/validate_non_ifrs_chunking_policy.py`
- `docs/reports/2026-07-05-nis4-chunking-embedding-policy.md`

Acceptance:

- document metadata, law locator, structured fact, private fact의 chunk/index 전략이 분리되어 있다.
- 어떤 lane은 embed하지 않고 locator/structured lookup만 쓰는지 명시되어 있다.
- 다음 runtime horizon이 source priority를 읽을 수 있는 정책 파일이 있다.

### NIS5. Dataization Gate and Runtime Handoff

NIS1~NIS4를 묶어 다음 horizon인 `multi-authority-runtime-hardening`으로 넘길 수 있는 gate를 만든다.

Deliverable:

- `scripts/non_ifrs_dataization_gate.py`
- `tests/test_non_ifrs_dataization_gate.py`
- `docs/reports/2026-07-05-nis5-dataization-gate.md`
- `docs/reports/2026-07-05-non-ifrs-source-dataization-close-report.md`

Acceptance:

- NIS reports, source record fixtures, chunking policy, RAG regression commands가 모두 통과한다.
- K-IFRS default retriever는 변경하지 않는다.
- 다음 horizon에서 사용할 runtime handoff contract가 정리되어 있다.

## Close Criteria

- K-IFRS 외 source lane이 record type, storage policy, citation role, retrieval lane으로 데이터화되어 있다.
- public repo에는 metadata/schema/synthetic fixture만 남고 protected body는 남지 않는다.
- 다음 horizon이 source authority별 답변 조립을 구현할 수 있는 runtime handoff가 있다.
- `python scripts\quality_preflight.py --format text`와 RAG reliability regression command set이 통과한다.

## Close Result

- Closed: 2026-07-05
- Source record contract: `kifrs/ingestion/source_record.py`
- Public fixture: `docs/ingestion/non_ifrs_source_records.example.json`
- Chunk/index policy: `docs/ingestion/non_ifrs_chunking_policy.json`
- Dataization gate: `docs/reports/2026-07-05-nis5-dataization-gate.md`
- Close report: `docs/reports/2026-07-05-non-ifrs-source-dataization-close-report.md`
- Next candidate horizon: `multi-authority-runtime-hardening`

## Decision Log

- 이번 horizon은 external/live connector 호출을 기본값으로 하지 않는다. 먼저 public-safe fixture와 validator를 만든다.
- KASB/FSS/FSC 해석 자료는 기준서 본문을 대체하지 않고 supporting interpretation으로만 둔다.
- DART/OpenDART 계열은 document RAG가 아니라 structured fact retrieval lane으로 둔다.
- Client-private 자료는 local-only placeholder/contract까지만 public repo에 둔다.
- 사용자 소유 결정: 현재 없음.
