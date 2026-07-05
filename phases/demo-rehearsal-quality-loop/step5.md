# Step 5: Horizon Close And Objective Gap Audit

## 읽어야 할 파일

- `docs/reports/2026-07-05-drq1-demo-rehearsal-script.md` - 왜: rehearsal script evidence다.
- `docs/reports/2026-07-05-drq2-demo-run-quality-checklist.md` - 왜: checklist evidence다.
- `docs/reports/2026-07-05-drq3-demo-rehearsal-evidence.md` - 왜: rehearsal run evidence다.
- `docs/reports/2026-07-05-drq4-demo-improvement-backlog.md` - 왜: improvement backlog evidence다.

## 작업

demo rehearsal quality loop horizon을 close하고 objective-gap queue의 남은 상태를 audit한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_demo_rehearsal_quality_close_gate.py -q
python scripts\demo_rehearsal_quality_close_gate.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. ROADMAP/OBJECTIVE/phase 상태를 close 결과와 동기화한다
3. phase index 업데이트

## 금지사항

- objective 전체 완료를 evidence 없이 선언하지 마라.
