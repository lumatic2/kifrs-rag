# MSI3 — Structured Fact Fixture Prototype

## Objective

MSI1 contract의 두 번째 record type인 `structured_fact`를 구현한다. OpenDART-like 재무제표 수치 데이터를
외부 API 호출 없이 synthetic fixture로 만들고, document metadata와 같은 manifest validator에서 검증되게 한다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-msi1-connector-contract.md` — 왜: `structured_fact` required fields와 forbidden field rules.
- `docs/reports/2026-07-05-msi2-metadata-catalog-prototype.md` — 왜: 현재 manifest/validator 구현 상태와 MSI2 검증 결과.
- `docs/ingestion/source_manifest.example.json` — 왜: 기존 manifest에 structured fact records를 추가하거나 별도 example을 만들지 결정.
- `kifrs/ingestion/manifest.py` — 왜: structured fact validator branch를 완성/강화해야 함.
- `tests/test_ingestion_manifest.py` — 왜: structured fact accept/reject 테스트를 추가해야 함.

## 작업

1. synthetic OpenDART-like `structured_fact` records를 추가한다.
   - 회사/공시 id는 synthetic으로 둔다.
   - line item, value, unit, period, statement type을 포함한다.
   - raw XML/XBRL/file body/API key는 넣지 않는다.
2. `structured_fact` branch의 validator coverage를 강화한다.
   - numeric `value` 검증.
   - `dimensions` object 검증.
   - `quality_flags` list 검증.
3. tests를 추가한다.
   - valid structured fact accept.
   - raw dump-like field reject.
   - invalid value/dimensions shape reject.
4. MSI3 결과 report를 작성한다.

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
- `tests/test_ingestion_manifest.py`
- `docs/reports/2026-07-05-msi3-structured-fact-fixture.md`

## 금지사항

- OpenDART API를 호출하지 않는다. 이유: MSI3은 synthetic fixture prototype이다.
- 실제 공시 raw XML/XBRL 또는 downloaded filing body를 커밋하지 않는다.
- structured fact만 구현한다. provenance/citation manifest 통합은 MSI4 범위다.

