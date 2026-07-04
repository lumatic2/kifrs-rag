# Step 3: reclassification-memo-skeleton

Status: completed (2026-07-05)

## 읽어야 할 파일

- `kifrs/workflows/kifrs1109/review_pack.py` — 왜: NeedsHumanReview pack에 skeleton memo를 연결한다.
- `kifrs/workflows/kifrs1109/fixtures.py` — 왜: scenario_08 reclassification fixture가 있다.

## 작업

사업모형 변경 재분류 케이스에 검토메모 skeleton을 제공한다. 자동 결론은 내지 않고, 필요한 입력과 판단
질문을 섹션화한다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_1109_reclassification.py tests/test_1109_review_pack.py
git diff --check
```

## 결과

- `kifrs/workflows/kifrs1109/reclassification.py` 추가.
- reclassification NeedsHumanReview pack에 `review_memo` skeleton 포함.
- report: `docs/reports/2026-07-05-fh3-reclassification-skeleton.md`.
