# MSI4 Provenance and Citation Manifest

> Horizon: `multi-source-ingestion-pipeline`
> Step: MSI4 — Provenance and Citation Manifest
> Date: 2026-07-05

## 한 줄 결론

ingestion records를 답변·워크플로우 evidence로 추적하는 `evidence_manifest`를 추가했다. 이제 source id,
record id, locator, citation role, storage policy가 source manifest와 일치하는지 검증할 수 있다.

## 구현된 것

### Evidence manifest

Path:

- `docs/ingestion/evidence_manifest.example.json`

포함 evidence:

| Evidence | Record | Role | Output level |
|---|---|---|---|
| `ev-kasb-interpretation-catalog-seed` | KASB document metadata | `supporting_interpretation` | metadata locator only |
| `ev-commercial-act-capital-locator` | Commercial Act locator | `legal_boundary` | metadata locator only |
| `ev-synthetic-dart-revenue` | Synthetic DART revenue fact | `fact_evidence` | synthetic fact only |

Evidence item은 source body나 copied quote를 담지 않고 source manifest의 실제 record를 참조한다.

### Validator

Paths:

- `kifrs/ingestion/evidence.py`
- `scripts/validate_ingestion_evidence.py`

검증하는 것:

- evidence manifest policy: `public_manifest_safe=true`, `body_text_committed=false`
- source manifest가 먼저 valid인지
- evidence item required fields
- `record_type + record_id`가 source manifest의 실제 record를 가리키는지
- `source_id`, `citation_role`, `body_storage_policy`가 source record와 일치하는지
- external evidence role은 `supporting_interpretation`, `legal_boundary`, `fact_evidence`만 허용
- copied quote/body/raw/credential류 forbidden field recursive rejection

### Tests

Path:

- `tests/test_ingestion_evidence.py`

Coverage:

- default evidence manifest accept
- unknown source record reject
- citation role mismatch reject
- copied quote field reject

## 검증 결과

```powershell
python scripts\validate_ingestion_manifest.py docs\ingestion\source_manifest.example.json
# ok: true, total: 5

python scripts\validate_ingestion_evidence.py docs\ingestion\evidence_manifest.example.json
# ok: true, total: 3

python -m pytest tests\test_ingestion_manifest.py tests\test_ingestion_evidence.py -q
# 10 passed
```

Pytest cache warning은 `.pytest_cache` 쓰기 권한 문제이고 테스트 실패는 아니다.

## 다음 단계

MSI5에서 이 horizon을 닫기 전 public-safe ingestion gate를 묶는다. 목표는 `validate_ingestion_manifest`,
`validate_ingestion_evidence`, authority/source-pack validation, `quality_preflight`, `git diff --check`를
하나의 close gate로 확인하고, 다음 runtime horizon으로 넘길 입력을 정리하는 것이다.

