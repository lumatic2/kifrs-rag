# Step 4: fx-dual-track-boundary

Status: completed (2026-07-05)

## 읽어야 할 파일

- `kifrs/workflows/kifrs1109/review_pack.py` — 왜: FX NeedsHumanReview pack에 boundary memo를 연결한다.
- `kifrs/workflows/kifrs1109/fixtures.py` — 왜: scenario_10 FX dual-track fixture가 있다.

## 작업

외화 금융상품 케이스에 1109 분류·측정과 1021 외화환산 표시를 분리한 boundary memo를 제공한다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_1109_fx_dual_track.py tests/test_1109_review_pack.py
git diff --check
```

## 결과

- `kifrs/workflows/kifrs1109/fx_dual_track.py` 추가.
- FX dual-track NeedsHumanReview pack에 `review_memo` boundary skeleton 포함.
- report: `docs/reports/2026-07-05-fh4-fx-dual-track-boundary.md`.
