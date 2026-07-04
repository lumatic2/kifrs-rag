# Step FB3: Runbook Manifest and Checker

## 읽어야 할 파일

- `docs/reports/field-feedback-runbook/2026-07-05-30min-session-runbook.md` - 왜: required section 검증 대상이다.
- `docs/reports/field-feedback-runbook/2026-07-05-operator-checklist.md` - 왜: required artifact다.

## 작업

runbook 필수 입력 자료와 section을 manifest로 만들고 checker/test를 추가한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_field_feedback_runbook.py -q
python scripts\field_feedback_runbook_check.py --manifest docs\reports\field-feedback-runbook\runbook_manifest.json
```

## 검증 절차

1. focused test와 checker를 실행한다.
2. missing artifact 실패 경로가 테스트되는지 확인한다.
3. FB3을 completed로 업데이트한다.

## 금지사항

- checker가 protected 자료를 필수 artifact로 요구하지 않게 한다.
