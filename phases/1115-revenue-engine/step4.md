# Step 4: review-memo-renderer

Status: completed (2026-07-05)

## 읽어야 할 파일

- `kifrs/workflows/kifrs1115/classify.py` — 왜: 판단 경로와 5단계 결론을 메모에 넣는다.
- `kifrs/workflows/kifrs1115/measurement.py` — 왜: 측정 결과와 배분표를 메모에 넣는다.
- `kifrs/workflows/kifrs1115/journal_entry.py` — 왜: 분개 초안을 메모에 렌더링한다.
- `kifrs/workflows/kifrs1109/review_memo.py` — 왜: 기존 markdown 검토메모 구조를 참고한다.

## 작업

1115 판단 결과를 회계자문팀 검토메모 초안으로 렌더링한다. 섹션은 거래 개요, 5단계 판단, 측정,
분개 초안, 결론으로 고정한다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_workflow_1115.py
git diff --check
```

## 결과

- `kifrs/workflows/kifrs1115/review_memo.py`: `generate_review_memo()` 추가.
- material right 메모는 5단계 판단, 계약부채, citation을 포함한다.
- repurchase financing 메모는 금융부채/스프레드를 렌더하고 수익 라인을 만들지 않는다.
