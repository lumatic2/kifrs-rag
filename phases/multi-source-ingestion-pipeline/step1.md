# MSI1 — Connector Contract and Source Manifest

## Objective

AS5가 추천한 첫 connector 후보를 구현하기 전에, metadata-only document source와 structured fact source를
같은 ingestion pipeline에서 다룰 수 있는 최소 contract를 정의한다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-as5-first-connector-recommendation.md` — 왜: first connector 후보와 scope.
- `docs/reports/2026-07-05-as3-storage-boundary.md` — 왜: protected body 금지와 storage labels.
- `docs/reports/2026-07-05-as4-ingestion-feasibility.md` — 왜: document/structured/local-private lane 정의.
- `docs/authority/source_pack_rules.md` — 왜: forbidden body fields and allowed public metadata.
- `kifrs/authority.py` — 왜: current registry/source pack validators and schema constraints.

## 작업

1. connector output contract 초안을 정의한다.
2. metadata document source와 structured fact source의 공통/분리 필드를 정한다.
3. public-safe source manifest 위치와 validator 후보를 정한다.
4. 다음 MSI2/MSI3에서 구현할 fixture 범위를 정한다.

## Acceptance Criteria

```powershell
python scripts\validate_authority_sources.py
python scripts\validate_authority_source_pack.py
python scripts\quality_preflight.py --format text
git diff --check
```

## Deliverable

- `docs/reports/2026-07-05-msi1-connector-contract.md`

## 금지사항

- MSI1에서 외부 API 호출이나 body fetch를 하지 않는다. 이유: contract first.
- protected body field를 manifest에 추가하지 않는다. 이유: AS3 storage boundary.

