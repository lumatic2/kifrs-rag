# Step AF4: Close Gate

## 읽어야 할 파일

- `docs/reports/2026-07-05-af3-feedback-incorporation-report.md` - 왜: 최종 action plan을 확인한다.
- `docs/reports/field-feedback/2026-07-05-incorporated-review-questions.md` - 왜: review question 반영 후보를 확인한다.
- `ROADMAP.md` - 왜: horizon close와 다음 추천 horizon을 동기화한다.
- `docs/OBJECTIVE.md` - 왜: active horizon과 최근 완료 상태를 동기화한다.

## 작업

focused tests, report generation, quality preflight를 실행하고 close report를 작성한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_feedback_incorporation.py tests\test_feedback_queue.py -q
python scripts\feedback_incorporation_report.py --queue docs\reports\real-transaction-poc\feedback-queue.jsonl --out docs\reports\2026-07-05-af3-feedback-incorporation-report.md --questions-out docs\reports\field-feedback\2026-07-05-incorporated-review-questions.md
python scripts\quality_preflight.py --format text
git diff --check
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. protected payload가 report에 들어가지 않았는지 검색한다.
3. close report를 작성하고 AF4를 completed로 업데이트한다.
4. ROADMAP/OBJECTIVE를 다음 horizon 추천 상태로 전환한다.

## 금지사항

- sample correction을 실제 회계사 검증 결과로 과장하지 않는다.
