# RT1 Runtime Evidence Loader

> Horizon: `multi-authority-runtime-integration`
> Step: RT1 — Runtime Evidence Loader
> Date: 2026-07-05

## 한 줄 결론

ingestion/evidence manifest를 workflow runtime이 바로 사용할 수 있는 immutable evidence object로 변환하는
loader를 추가했다. 이제 review pack, statement draft, answer composer는 manifest 파일 구조를 직접 알지
않고도 role별 external evidence를 조회할 수 있다.

## 구현된 것

### Runtime module

Paths:

- `kifrs/runtime/__init__.py`
- `kifrs/runtime/evidence.py`

주요 API:

- `load_runtime_evidence()`
- `EvidenceBundle`
- `RuntimeEvidence`

`load_runtime_evidence()`는 먼저 `validate_evidence_manifest()`를 실행한다. source/evidence manifest가
안전하지 않거나 서로 맞지 않으면 빈 bundle을 만들지 않고 `ValueError`를 발생시킨다.

### Runtime evidence object

`RuntimeEvidence`는 아래 정보를 가진다.

- `evidence_id`
- `record_type`
- `record_id`
- `source_id`
- `citation_role`
- `body_storage_policy`
- `locator`
- `evidence_label`
- `allowed_output_level`
- `record`
- `notes`

`to_reference_dict()`는 downstream output에 넣기 좋은 locator/reference만 반환하고, source record payload는
포함하지 않는다.

### Query helpers

`EvidenceBundle`은 role별 query를 제공한다.

- `by_role(role)`
- `supporting_interpretations`
- `legal_boundaries`
- `fact_evidence`
- `get(evidence_id)`

## 검증 결과

```powershell
python -m pytest tests\test_runtime_evidence.py tests\test_ingestion_manifest.py tests\test_ingestion_evidence.py -q
# 14 passed

python scripts\validate_ingestion_manifest.py docs\ingestion\source_manifest.example.json
# ok: true, total: 5

python scripts\validate_ingestion_evidence.py docs\ingestion\evidence_manifest.example.json
# ok: true, total: 3
```

Pytest cache warning은 `.pytest_cache` 쓰기 권한 문제이고 테스트 실패는 아니다.

## 다음 단계

RT2에서는 review pack에 external evidence panel을 붙인다. 첫 대상은 기존 산출물 구조가 안정된
1116/1109/1115 review pack이다. RT2는 새 evidence를 판단 로직에 섞지 않고, 산출물에 별도 section으로
표시하는 범위로 제한한다.

