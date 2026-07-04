# Step 5: review-pack-integration

Status: completed (2026-07-05)

## 읽어야 할 파일

- `kifrs/workflows/kifrs1115/review_memo.py` — 왜: pack의 검토메모 payload다.
- `kifrs/workflows/kifrs1115/journal_entry.py` — 왜: pack의 분개 초안 payload다.
- `kifrs/workflows/kifrs1109/review_pack.py` — 왜: F-ACC review pack 공통 표면 전례다.
- `tests/test_1109_review_pack.py` — 왜: automated/needs_human_review pack 검증 방식을 따른다.

## 작업

1115 산출물을 F-ACC review pack으로 묶는다. pack은 상태, 판단 경로, 판단 요약, 검토메모, 분개 초안,
리뷰 체크리스트, 사람 검토 필요 항목, citation id를 가진다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_1115_review_pack.py
git diff --check
```

## 결과

- `kifrs/workflows/kifrs1115/review_pack.py`: 1115 review pack contract와 markdown renderer 추가.
- 자동 fixture 4개가 모두 review pack으로 생성된다.
- 입력 부족 케이스는 `needs_human_review` pack으로 중단 사유와 추가자료를 노출한다.
