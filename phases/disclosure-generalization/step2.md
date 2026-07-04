# Step 2: common-disclosure-checklist-schema

Status: completed (2026-07-05)

## 읽어야 할 파일

- `docs/reports/2026-07-05-dg1-disclosure-surface-inventory.md` — 왜: common schema 후보가 있다.
- `kifrs/workflows/kifrs1116/disclosure.py` — 왜: 1116 요구항목 adapter 기준점이다.
- `kifrs/workflows/kifrs1115/review_pack.py` — 왜: 1115 pack adapter source다.
- `kifrs/workflows/kifrs1109/review_pack.py` — 왜: 1109 pack adapter source다.

## 작업

기준서별 disclosure output을 공통 `DisclosureChecklistItem`으로 변환하는 schema와 adapter를 만든다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_disclosure_common.py
git diff --check
```

## 결과

- `kifrs/workflows/disclosure/schema.py`: `DisclosureChecklistItem`, `FillStatus` 추가.
- `kifrs/workflows/disclosure/adapters.py`: 1116 requirement, 1115 review pack, 1109 review pack adapter 추가.
- `tests/test_disclosure_common.py`: 1116 8/11 auto, 1115 decision/measurement/human item, 1109 classification/human item 검증.
