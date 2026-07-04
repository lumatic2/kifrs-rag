# RT4 Answer Boundary Composer

> Horizon: `multi-authority-runtime-integration`
> Step: RT4 — Answer Boundary Composer
> Date: 2026-07-05

## 한 줄 결론

primary K-IFRS evidence와 external evidence를 분리해 렌더링하는 answer boundary helper를 추가했다.
external evidence가 primary K-IFRS evidence로 승격되지 않는 구조를 runtime layer에 만들었다.

## 구현된 것

### Answer boundary module

Path:

- `kifrs/runtime/answer_boundary.py`

주요 API:

- `PrimaryEvidenceRef`
- `EvidenceBoundary`
- `compose_evidence_boundary(bundle, primary_citations=None)`
- `render_evidence_boundary(boundary)`

### Boundary sections

`EvidenceBoundary`는 네 그룹으로 분리된다.

- `primary_kifrs_evidence`
- `supporting_interpretation`
- `legal_boundary`
- `fact_evidence`

`primary_citations`를 명시하지 않으면 primary section은 빈 list로 남는다. external evidence는 supporting,
legal, fact section에만 들어가며 primary로 승격되지 않는다.

### Tests

Path:

- `tests/test_answer_boundary.py`

Coverage:

- primary/external role separation
- primary citation이 없을 때 external evidence가 primary로 승격되지 않음
- rendered boundary에 source record payload나 copied source text가 노출되지 않음

## 검증 결과

```powershell
python -m pytest tests\test_answer_boundary.py tests\test_runtime_evidence.py -q
# 7 passed

python scripts\validate_ingestion_manifest.py docs\ingestion\source_manifest.example.json
# ok: true, total: 5

python scripts\validate_ingestion_evidence.py docs\ingestion\evidence_manifest.example.json
# ok: true, total: 3

python scripts\quality_preflight.py --format text
# ok: True, public_safe: True
```

Pytest cache warning은 `.pytest_cache` 쓰기 권한 문제이고 테스트 실패는 아니다.

## 다음 단계

RT5에서는 runtime close demo를 만든다. 기존 PoC demo에 `load_runtime_evidence()`를 연결해 review pack,
statement candidates, evidence boundary가 하나의 demo output bundle에서 같이 보이도록 한다.

