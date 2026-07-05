# Step 3: Rehearsal Evidence Capture

## 읽어야 할 파일

- `docs/reports/2026-07-05-drq2-demo-run-quality-checklist.md` - 왜: rehearsal evidence의 pass/fail schema다.

## 작업

public-safe rehearsal run fixture를 만들고 stage results와 timing metadata를 capture한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_demo_rehearsal_evidence_capture.py -q
python scripts\demo_rehearsal_evidence_capture.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. timing metadata가 과장 없이 기록되는지 확인
3. phase index 업데이트

## 금지사항

- 실제 사용자/회계사 개인정보를 evidence fixture로 넣지 마라.
