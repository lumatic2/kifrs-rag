# MSI2 Metadata-Only Document Catalog Prototype

> Horizon: `multi-source-ingestion-pipeline`
> Step: MSI2 — Metadata-Only Document Catalog Prototype
> Date: 2026-07-05

## 한 줄 결론

MSI1의 connector contract를 실제 public-safe manifest와 validator로 옮겼다. 이제 외부 문서형 자료는
본문 없이 `document_metadata` record로 등록하고, source registry와 storage/citation policy를 기계적으로
검증할 수 있다.

## 구현된 것

### Public manifest fixture

Path:

- `docs/ingestion/source_manifest.example.json`

포함 record:

| Record | Source id | Role | Storage |
|---|---|---|---|
| KASB catalog seed | `kasb-interpretation-material` | `supporting_interpretation` | `public_metadata_only` |
| FSS inquiry catalog seed | `fss-accounting-inquiry` | `supporting_interpretation` | `public_metadata_only` |
| Commercial Act locator seed | `commercial-act-capital` | `legal_boundary` | `no_store_link_only` |

세 record 모두 title, publisher, locator, topic, chunk strategy 같은 metadata만 가진다. 질의회신 본문,
법령 조문, 교육자료 본문, PDF body는 포함하지 않는다.

### Validator

Paths:

- `kifrs/ingestion/manifest.py`
- `scripts/validate_ingestion_manifest.py`

검증하는 것:

- manifest policy: `public_manifest_safe=true`, `body_text_committed=false`,
  `forbidden_fields_rejected=true`
- record envelope required fields
- `source_id`가 `docs/authority/sources.json`에 존재하는지
- `body_storage_policy`가 AS3 storage label인지
- public manifest에서 public-safe storage policy만 쓰는지
- `citation_role`이 MSI ingestion role인지
- `document_metadata` required fields
- forbidden field name recursive rejection

Forbidden fields:

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

### Tests

Path:

- `tests/test_ingestion_manifest.py`

Coverage:

- default public manifest accept
- body-like field reject
- unknown source id reject

## 검증 결과

```powershell
python scripts\validate_ingestion_manifest.py docs\ingestion\source_manifest.example.json
# ok: true, total: 3

python -m pytest tests\test_ingestion_manifest.py -q
# 3 passed
```

Pytest cache warning이 발생했지만 `.pytest_cache` 쓰기 권한 문제이고 테스트 실패는 아니다.

## 다음 단계

MSI3에서는 document metadata가 아니라 `structured_fact`를 구현한다. 범위는 synthetic OpenDART-like
financial facts fixture, structured fact validator coverage, raw dump/API-key field rejection이다.

