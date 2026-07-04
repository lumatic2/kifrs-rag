# MSI4 — Provenance and Citation Manifest

## Objective

MSI2/MSI3에서 만든 ingestion records를 답변·워크플로우가 추적 가능한 evidence trail로 연결한다.
`source_id`, record id, locator, storage policy, citation role을 별도 provenance/citation manifest로 검증한다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-msi1-connector-contract.md` — 왜: connector envelope와 citation/storage 경계.
- `docs/reports/2026-07-05-msi2-metadata-catalog-prototype.md` — 왜: document metadata record와 validator 동작.
- `docs/reports/2026-07-05-msi3-structured-fact-fixture.md` — 왜: structured fact record와 fact evidence boundary.
- `docs/ingestion/source_manifest.example.json` — 왜: citation manifest가 참조할 record source.
- `kifrs/ingestion/manifest.py` — 왜: validator 확장 또는 별도 citation validator가 여기와 맞아야 함.

## 작업

1. citation/provenance manifest shape를 정한다.
   - record reference: `record_type` + `record_id`
   - source reference: `source_id`
   - locator reference: manifest record locator or filing locator
   - role: `supporting_interpretation`, `legal_boundary`, `fact_evidence`
   - storage policy: manifest record storage policy
2. public-safe example을 만든다.
   - 후보 path: `docs/ingestion/evidence_manifest.example.json`
   - source body나 quoted excerpt 없이 locator만 둔다.
3. validator를 구현한다.
   - evidence item이 source manifest의 실제 record를 가리키는지 확인한다.
   - citation role과 storage policy가 source manifest record와 일치하는지 확인한다.
   - `primary_evidence`와 외부 supporting/fact evidence가 섞이지 않도록 role boundary를 검사한다.
4. tests와 MSI4 결과 report를 작성한다.

## Acceptance Criteria

```powershell
python scripts\validate_ingestion_manifest.py docs\ingestion\source_manifest.example.json
python scripts\validate_ingestion_evidence.py docs\ingestion\evidence_manifest.example.json
python -m pytest tests\test_ingestion_manifest.py tests\test_ingestion_evidence.py -q
python scripts\quality_preflight.py --format text
git diff --check
```

## Deliverable

- `docs/ingestion/evidence_manifest.example.json`
- `kifrs/ingestion/evidence.py`
- `scripts/validate_ingestion_evidence.py`
- `tests/test_ingestion_evidence.py`
- `docs/reports/2026-07-05-msi4-provenance-citation-manifest.md`

## 금지사항

- evidence manifest에 source body, copied quote, 법령 조문, 질의회신 본문을 넣지 않는다.
- primary K-IFRS paragraph evidence와 외부 supporting/fact evidence를 같은 authority class로 취급하지 않는다.

