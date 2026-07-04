# Step 1: statement-draft-surface-inventory

Status: pending

## 읽어야 할 파일

- `docs/horizons/f-acc-financial-statement-draft.md` — 왜: horizon 목표와 milestone sequence가 있다.
- `kifrs/workflows/kifrs1109/review_pack.py` — 왜: 금융상품 분류/분개 output source.
- `kifrs/workflows/kifrs1115/review_pack.py` — 왜: 수익/계약부채/금융요소 output source.
- `kifrs/workflows/kifrs1116/review_pack.py` — 왜: 리스 사용권자산/리스부채/주석 output source.

## 작업

기존 review pack output 중 재무제표 본문/표시 draft에 쓸 수 있는 field를 inventory로 정리한다.

## Acceptance Criteria

```powershell
git diff --check
```

## 결과물

- `docs/reports/2026-07-05-fs1-statement-draft-surface-inventory.md`
