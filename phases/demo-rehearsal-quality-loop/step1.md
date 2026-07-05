# Step 1: Demo Rehearsal Script And Timing Gate

## 읽어야 할 파일

- `docs/horizons/demo-rehearsal-quality-loop.md` - 왜: DRQ1 acceptance와 horizon boundary를 확인한다.
- `docs/plans/2026-07-05-demo-rehearsal-quality-loop.md` - 왜: DRQ milestone tree와 decision log를 따른다.
- `docs/reports/end-to-end-demo/INDEX.md` - 왜: 기존 demo packet entry point다.
- `docs/reports/2026-07-05-end-to-end-demo-scenario-close-report.md` - 왜: 기존 demo close evidence다.

## 작업

`scripts/demo_rehearsal_script.py`를 만들어 demo stages, timing budget, operator command, expected evidence outputs를 정의한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_demo_rehearsal_script.py -q
python scripts\demo_rehearsal_script.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. 외부 피드백/패키징을 다음 행동으로 넣지 않는지 확인
3. phase index 업데이트

## 금지사항

- 실제 외부 피드백 capture를 이 단계에 넣지 마라.
- packaging 작업을 이 horizon에 넣지 마라.
