# Step AF3: Incorporation Report Command

## 읽어야 할 파일

- `kifrs/feedback/incorporation.py` - 왜: report와 question supplement renderer를 호출한다.
- `docs/reports/real-transaction-poc/feedback-queue.jsonl` - 왜: sample queue input이다.

## 작업

명령 하나로 feedback incorporation report와 review question supplement를 생성한다.

## Acceptance Criteria

```powershell
python scripts\feedback_incorporation_report.py --queue docs\reports\real-transaction-poc\feedback-queue.jsonl --out docs\reports\2026-07-05-af3-feedback-incorporation-report.md --questions-out docs\reports\field-feedback\2026-07-05-incorporated-review-questions.md
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. 두 report가 생성됐는지 확인한다.
3. AF3을 completed로 업데이트한다.

## 금지사항

- original questionnaire를 덮어쓰지 않는다. supplement로 둔다.
