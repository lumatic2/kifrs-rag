# Step AF2: Feedback Incorporation Planner

## 읽어야 할 파일

- `kifrs/feedback/queue.py` - 왜: feedback queue record schema와 disposition split을 재사용한다.
- `docs/reports/real-transaction-poc/feedback-queue.jsonl` - 왜: 첫 sample queue input이다.
- `docs/reports/field-feedback/2026-07-05-feedback-questionnaire.md` - 왜: review question supplement가 붙을 대상이다.

## 작업

queue record를 제품 개선 action으로 변환하는 planner를 추가한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_feedback_incorporation.py -q
```

## 검증 절차

1. focused test를 실행한다.
2. eval seed/backlog/no-action이 분리되는지 확인한다.
3. AF2를 completed로 업데이트한다.

## 금지사항

- queue correction을 곧바로 최종 제품 판단으로 확정하지 않는다. action candidate로 남긴다.
