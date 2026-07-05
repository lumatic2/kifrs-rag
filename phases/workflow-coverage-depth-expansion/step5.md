# Step 5: Horizon Close And Demo Rehearsal Handoff

## 읽어야 할 파일

- `docs/reports/2026-07-05-wcd1-service-line-coverage-rerank.md` - 왜: coverage rerank evidence다.
- `docs/reports/2026-07-05-wcd2-workflow-sample-contract-pack.md` - 왜: sample contract evidence다.
- `docs/reports/2026-07-05-wcd3-minimal-adapter-expansion.md` - 왜: adapter evidence다.
- `docs/reports/2026-07-05-wcd4-coverage-depth-metric.md` - 왜: metric evidence다.

## 작업

workflow coverage depth expansion horizon을 close하고 다음 objective-gap horizon을 지정한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_workflow_coverage_depth_close_gate.py -q
python scripts\workflow_coverage_depth_close_gate.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. ROADMAP/OBJECTIVE/phase 상태를 close 결과와 동기화한다
3. phase index 업데이트

## 금지사항

- close gate가 실패했는데 ROADMAP을 완료로 바꾸지 마라.
