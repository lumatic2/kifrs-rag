# MSI5 Ingestion Gate Close Report

> Horizon: `multi-source-ingestion-pipeline`
> Step: MSI5 — Ingestion Gate and Close Report
> Date: 2026-07-05

## 한 줄 결론

`multi-source-ingestion-pipeline` horizon은 닫을 수 있다. K-IFRS 외부 자료를 public-safe metadata/fact/evidence
형태로 등록하고 검증하는 skeleton이 생겼다.

## 무엇이 가능해졌나

### 1. 문서형 외부 자료를 body 없이 등록

`document_metadata` record로 KASB/FSS 해석자료, 법령 locator 같은 문서형 source를 등록한다.

현재 fixture:

- KASB interpretation material catalog seed
- FSS accounting inquiry catalog seed
- Commercial Act capital locator seed

### 2. 수치형 회사 fact를 structured record로 등록

`structured_fact` record로 OpenDART-like 재무제표 수치를 등록한다.

현재 fixture:

- synthetic current assets
- synthetic revenue

둘 다 실제 회사 공시가 아니라 public-safe synthetic fixture다.

### 3. 답변 근거 trail을 evidence manifest로 추적

`evidence_manifest`가 source manifest record를 참조하고, 아래 값이 일치하는지 검증한다.

- `source_id`
- `record_type + record_id`
- `citation_role`
- `body_storage_policy`
- locator

### 4. protected body gate

다음 field들은 ingestion/evidence manifest에서 recursive reject된다.

- `body`
- `text`
- `content`
- `full_text`
- `source_body`
- `excerpt`
- `quote`
- `embedding`
- `raw_xml`
- `xbrl_dump`
- `pdf_bytes`
- `api_key`
- `token`
- `credential`

## 구현 산출물

Manifest:

- `docs/ingestion/source_manifest.example.json`
- `docs/ingestion/evidence_manifest.example.json`

Validators:

- `kifrs/ingestion/manifest.py`
- `kifrs/ingestion/evidence.py`
- `scripts/validate_ingestion_manifest.py`
- `scripts/validate_ingestion_evidence.py`

Tests:

- `tests/test_ingestion_manifest.py`
- `tests/test_ingestion_evidence.py`

Reports:

- `docs/reports/2026-07-05-msi1-connector-contract.md`
- `docs/reports/2026-07-05-msi2-metadata-catalog-prototype.md`
- `docs/reports/2026-07-05-msi3-structured-fact-fixture.md`
- `docs/reports/2026-07-05-msi4-provenance-citation-manifest.md`
- `docs/reports/2026-07-05-msi5-ingestion-gate-close-report.md`

## Close Gate

```powershell
python scripts\validate_authority_sources.py
# ok: true, total: 7

python scripts\validate_authority_source_pack.py
# ok: true, total: 7

python scripts\validate_ingestion_manifest.py docs\ingestion\source_manifest.example.json
# ok: true, total: 5

python scripts\validate_ingestion_evidence.py docs\ingestion\evidence_manifest.example.json
# ok: true, total: 3

python -m pytest tests\test_ingestion_manifest.py tests\test_ingestion_evidence.py tests\test_authority.py tests\test_authority_source_pack.py -q
# 18 passed

python scripts\quality_preflight.py --format text
# ok: True, public_safe: True

git diff --check
# no whitespace errors
```

Pytest cache warning이 발생했지만 `.pytest_cache` 쓰기 권한 문제이고 테스트 실패는 아니다.

## Deliberately Out of Scope

- no external API call
- no KASB/FSS body fetch
- no law article body copy
- no raw DART filing/XML/XBRL commit
- no embeddings/vector store
- no client-private intake
- no final accounting treatment decision from external source alone

## Next Horizon Recommendation

Recommended next horizon:

- `multi-authority-runtime-integration`

Why:

이제 source를 안전하게 담는 skeleton은 생겼다. 다음은 runtime이 이 evidence를 실제 회계 워크플로우에 쓰게
해야 한다. 목표는 F-ACC review pack/statement draft/audit analytics가 `K-IFRS paragraph evidence`와
`external supporting/fact evidence`를 분리해서 표시하는 것이다.

Candidate milestones:

1. Runtime evidence loader
   - source/evidence manifest를 로드해 workflow에서 쓸 수 있는 evidence object로 변환한다.
2. Review-pack evidence panel
   - 1116/1109/1115 review pack에 external supporting/fact evidence section을 추가한다.
3. Answer composer boundary
   - primary K-IFRS evidence, supporting interpretation, legal boundary, fact evidence를 답변에서 분리한다.
4. RAG quality refresh follow-up
   - K-IFRS retrieval quality gate와 external evidence display가 충돌하지 않는지 확인한다.
5. Runtime close demo
   - 하나의 회계 업무 시나리오에서 기준서 문단 + 해석자료 metadata + synthetic company fact를 같이 보여준다.

