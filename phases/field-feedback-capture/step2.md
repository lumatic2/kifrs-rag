# Step FC2: Feedback Notes Capture Contract

## 읽어야 할 파일

- `kifrs/feedback/case_intake.py` - 왜: public-safe validation issue와 reviewer correction schema를 재사용한다.
- `kifrs/feedback/queue.py` - 왜: safe correction을 queue record로 변환한다.
- `docs/reports/field-feedback-runbook/2026-07-05-30min-session-runbook.md` - 왜: recording template의 필드를 capture schema로 옮긴다.

## 작업

field feedback notes schema, validation, queue conversion, markdown report renderer를 추가한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_field_feedback_capture.py -q
```

## 검증 절차

1. focused test를 실행한다.
2. protected payload rejection과 safe queue conversion을 확인한다.
3. FC2를 completed로 업데이트한다.

## 금지사항

- notes 전체를 workpaper store로 만들지 않는다. queue에는 correction candidate만 넣는다.
