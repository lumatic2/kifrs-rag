# RT2 Review-Pack Evidence Panel

> Horizon: `multi-authority-runtime-integration`
> Step: RT2 — Review-Pack Evidence Panel
> Date: 2026-07-05

## 한 줄 결론

1116/1109/1115 review pack에 optional external evidence panel을 붙였다. 판단 로직은 바꾸지 않고,
runtime evidence loader가 제공하는 safe reference만 markdown/json output에 별도 section으로 표시한다.

## 구현된 것

### Shared panel renderer

Path:

- `kifrs/runtime/evidence_panel.py`

주요 API:

- `evidence_references(bundle)`
- `render_external_evidence_panel(external_evidence)`

panel은 세 role을 분리해 표시한다.

- `supporting_interpretation` → 해석 보조 근거
- `legal_boundary` → 법적 경계 근거
- `fact_evidence` → 수치 사실 근거

### Review pack integration

Updated:

- `kifrs/workflows/kifrs1116/review_pack.py`
- `kifrs/workflows/kifrs1109/review_pack.py`
- `kifrs/workflows/kifrs1115/review_pack.py`

`generate_review_pack(..., evidence_bundle=None)` 형태로 optional parameter를 추가했다. 기존 호출은
그대로 동작하고, bundle을 넘긴 경우에만 `external_evidence`가 채워진다.

### Output boundary

review pack output에는 source body나 quote를 넣지 않는다. `RuntimeEvidence.to_reference_dict()` 결과만
사용하므로 아래 항목만 노출된다.

- evidence id
- source id
- record id
- citation role
- storage policy
- locator
- evidence label
- allowed output level

## 검증 결과

```powershell
python -m pytest tests\test_1116_review_pack.py tests\test_1109_review_pack.py tests\test_1115_review_pack.py tests\test_runtime_evidence.py -q
# 17 passed

python scripts\validate_ingestion_manifest.py docs\ingestion\source_manifest.example.json
# ok: true, total: 5

python scripts\validate_ingestion_evidence.py docs\ingestion\evidence_manifest.example.json
# ok: true, total: 3

python scripts\quality_preflight.py --format text
# ok: True, public_safe: True
```

Pytest cache warning은 `.pytest_cache` 쓰기 권한 문제이고 테스트 실패는 아니다.

## 다음 단계

RT3에서는 statement draft 후보에 fact evidence reference를 붙인다. 목표는 review pack에 표시된
`fact_evidence`가 재무제표 표시 후보와도 연결되도록 하는 것이다.

