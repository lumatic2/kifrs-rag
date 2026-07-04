# MSI3 Structured Fact Fixture Prototype

> Horizon: `multi-source-ingestion-pipeline`
> Step: MSI3 — Structured Fact Fixture Prototype
> Date: 2026-07-05

## 한 줄 결론

OpenDART-like structured financial facts를 synthetic fixture로 manifest에 추가했다. 이제 ingestion manifest는
문서형 metadata뿐 아니라 회사 재무제표 수치형 record도 같은 public-safe gate에서 검증한다.

## 구현된 것

### Structured fact source seed

Paths:

- `docs/authority/sources.json`
- `docs/authority/source_pack.json`

추가 source:

- `opendart-structured-financials`

이 source는 회계 기준 권위가 아니라 공시 수치 fact source 후보이므로 `source_pack`에서는
`collection_seed`로만 둔다. Raw filing, API payload, parsed real-company cache는 public repo에 두지 않는다.

### Synthetic structured fact records

Path:

- `docs/ingestion/source_manifest.example.json`

추가 record:

| Fact id | Statement | Line item | Value | Unit |
|---|---|---|---:|---|
| `synthetic-dart-2025-annual-001-assets-current` | `financial_position` | `current_assets` | 1250000000 | KRW |
| `synthetic-dart-2025-annual-001-revenue` | `profit_or_loss` | `revenue` | 3780000000 | KRW |

두 record 모두 `public_synthetic_fixture`이며 `fact_evidence` citation role을 사용한다. 실제 회사 공시나
API 응답을 복사하지 않았다.

### Validator hardening

Path:

- `kifrs/ingestion/manifest.py`

추가 검증:

- `structured_fact`는 `fact_evidence` citation role만 사용
- public fixture에서는 `public_synthetic_fixture` storage policy만 사용
- `value`는 numeric
- `dimensions`는 object
- `filing_locator`는 non-empty object
- `quality_flags`는 list
- raw dump/API-key류 forbidden field는 recursive rejection

### Tests

Path:

- `tests/test_ingestion_manifest.py`

추가 coverage:

- structured fact accept
- raw XML-like field reject
- invalid numeric/dimensions shape reject

## 검증 결과

```powershell
python scripts\validate_authority_sources.py
# ok: true, total: 7

python scripts\validate_authority_source_pack.py
# ok: true, total: 7

python scripts\validate_ingestion_manifest.py docs\ingestion\source_manifest.example.json
# ok: true, total: 5

python -m pytest tests\test_ingestion_manifest.py tests\test_authority.py tests\test_authority_source_pack.py -q
# 14 passed

python scripts\quality_preflight.py --format text
# ok: True, public_safe: True
```

Pytest cache warning은 `.pytest_cache` 쓰기 권한 문제이고 테스트 실패는 아니다.

## 다음 단계

MSI4에서는 manifest record를 answer/workflow evidence로 쓰기 위한 provenance and citation manifest를 만든다.
핵심은 `source_id`, `record id`, `locator`, `body_storage_policy`, `citation_role`을 하나의 evidence trail로
검증하는 것이다.

