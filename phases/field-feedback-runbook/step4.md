# Step FB4: Close Gate

## 읽어야 할 파일

- `docs/reports/field-feedback-runbook/2026-07-05-30min-session-runbook.md` - 왜: 최종 runbook 내용 확인.
- `docs/reports/field-feedback-runbook/runbook_manifest.json` - 왜: checker 입력 확인.
- `ROADMAP.md` - 왜: horizon close와 다음 추천 horizon을 동기화한다.
- `docs/OBJECTIVE.md` - 왜: active horizon과 최근 완료 상태를 동기화한다.

## 작업

focused tests, checker, quality preflight를 실행하고 close report를 작성한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_field_feedback_runbook.py -q
python scripts\field_feedback_runbook_check.py --manifest docs\reports\field-feedback-runbook\runbook_manifest.json
python scripts\quality_preflight.py --format text
git diff --check
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. ROADMAP 150줄 제한을 확인한다.
3. close report를 작성하고 FB4를 completed로 업데이트한다.
4. ROADMAP/OBJECTIVE를 다음 horizon 추천 상태로 전환한다.

## 금지사항

- 세션 준비 완료를 실제 피드백 완료와 혼동하지 않는다.
