# Step 1: disclosure-surface-inventory

Status: completed (2026-07-05)

## 읽어야 할 파일

- `docs/horizons/f-acc-disclosure-generalization.md` — 왜: horizon 목표와 DG milestone sequence가 있다.
- `docs/practice-map/team-workflows.md` — 왜: F-ACC B5 주석 작성 업무의 위치가 있다.
- `kifrs/workflows/kifrs1116/disclosure.py` — 왜: 기존 1116 주석 checklist/초안 산출물이다.
- `kifrs/workflows/kifrs1115/review_pack.py` — 왜: 1115 output에서 주석 후보 source를 찾는다.
- `kifrs/workflows/kifrs1109/review_pack.py` — 왜: 1109 output에서 주석 후보 source를 찾는다.

## 작업

1116, 1115, 1109의 산출물 중 주석 checklist/draft로 재사용 가능한 field를 inventory로 정리한다.

## Acceptance Criteria

```powershell
git diff --check
```

## 결과물

- `docs/reports/2026-07-05-dg1-disclosure-surface-inventory.md`

## 결과

- 1116: 기존 `DisclosureRequirement`/portfolio contribution이 common schema 기준점.
- 1115: path, measurement, human review action을 주석 후보 source로 재사용.
- 1109: classification, SPPI/사업모형, 후속측정/위험자료 요청을 주석 후보 source로 재사용.
- DG2 구현 방향: `DisclosureChecklistItem` schema + domain adapter.
