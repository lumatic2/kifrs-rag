# MSI2 — Metadata-Only Document Catalog Prototype

## Objective

MSI1에서 정의한 connector contract를 실제 public-safe manifest와 validator로 옮긴다. 첫 구현 대상은
`document_metadata` record type만이다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-msi1-connector-contract.md` — 왜: MSI2가 구현해야 하는 manifest shape와 validator rules.
- `docs/reports/2026-07-05-as3-storage-boundary.md` — 왜: public-safe storage labels와 금지 body 경계.
- `docs/authority/source_pack_rules.md` — 왜: 기존 forbidden field 정책과 source registry 연결 규칙.
- `kifrs/authority.py` — 왜: source registry loader/validator 패턴 재사용.
- `docs/authority/sources.json` — 왜: `source_id`가 실제 registry id인지 검증해야 함.

## 작업

1. `docs/ingestion/source_manifest.example.json`을 만든다.
   - `document_metadata` record 2-3개만 포함한다.
   - source body, copied article, copied inquiry reply, PDF body, raw document field는 넣지 않는다.
2. `kifrs/ingestion/manifest.py`를 추가한다.
   - manifest loader와 validator를 구현한다.
   - forbidden field를 nested object/list까지 재귀 검사한다.
   - `source_id`가 `docs/authority/sources.json`에 존재하는지 확인한다.
3. `scripts/validate_ingestion_manifest.py`를 추가한다.
   - 기본값은 `docs/ingestion/source_manifest.example.json`.
   - 실패 시 error list를 출력하고 non-zero exit.
4. `tests/test_ingestion_manifest.py`를 추가한다.
   - metadata-only fixture accept.
   - forbidden body-like field reject.
   - unknown source id reject.

## Acceptance Criteria

```powershell
python scripts\validate_ingestion_manifest.py docs\ingestion\source_manifest.example.json
python -m pytest tests\test_ingestion_manifest.py -q
python scripts\quality_preflight.py --format text
git diff --check
```

## Deliverable

- `docs/ingestion/source_manifest.example.json`
- `kifrs/ingestion/manifest.py`
- `scripts/validate_ingestion_manifest.py`
- `tests/test_ingestion_manifest.py`
- `docs/reports/2026-07-05-msi2-metadata-catalog-prototype.md`

## 금지사항

- 외부 API를 호출하지 않는다. 이유: MSI2는 manifest/validator prototype이다.
- source body를 fixture에 넣지 않는다. 이유: public-safe ingestion boundary 검증이 목적이다.
- `fact_evidence`나 structured facts를 구현하지 않는다. 이유: MSI3 범위다.

