# RT3 Statement Draft Fact Evidence Hook

> Horizon: `multi-authority-runtime-integration`
> Step: RT3 — Statement Draft Fact Evidence Hook
> Date: 2026-07-05

## 한 줄 결론

statement draft 후보가 `fact_evidence` reference를 가질 수 있게 했다. 이제 review pack에 주입된 external
evidence 중 수치 사실 근거가 재무제표 표시 후보의 amount-bearing line에 연결된다.

## 구현된 것

### Statement candidate schema

Path:

- `kifrs/workflows/statement_draft/schema.py`

추가 field:

- `evidence_refs: list[dict[str, object]] = field(default_factory=list)`

default empty list라 기존 statement draft 호출은 깨지지 않는다.

### Statement draft adapters

Path:

- `kifrs/workflows/statement_draft/adapters.py`

동작:

- review pack의 `external_evidence` 중 `citation_role == "fact_evidence"`만 추출한다.
- amount가 있고 `statement != "note"`인 line candidate에만 `evidence_refs`를 붙인다.
- note-only candidate에는 fact evidence를 붙이지 않는다.

### Tests

Path:

- `tests/test_statement_draft.py`

추가 coverage:

- fact evidence가 amount-bearing line candidate에 붙는지
- note candidate에는 붙지 않는지
- `record` payload가 evidence refs에 노출되지 않는지
- synthetic DART revenue fact id가 연결되는지

## 검증 결과

```powershell
python -m pytest tests\test_statement_draft.py tests\test_runtime_evidence.py tests\test_1115_review_pack.py -q
# 16 passed

python scripts\validate_ingestion_manifest.py docs\ingestion\source_manifest.example.json
# ok: true, total: 5

python scripts\validate_ingestion_evidence.py docs\ingestion\evidence_manifest.example.json
# ok: true, total: 3

python scripts\quality_preflight.py --format text
# ok: True, public_safe: True
```

Pytest cache warning은 `.pytest_cache` 쓰기 권한 문제이고 테스트 실패는 아니다.

## 다음 단계

RT4에서는 answer boundary composer를 만든다. 아직 독립 answer composer 모듈이 없으므로, 첫 단계는
primary K-IFRS evidence, supporting interpretation, legal boundary, fact evidence를 분리해 렌더링하는
runtime helper를 추가하는 것이다.

