# Step 4: Coverage Depth Metric Update

## 읽어야 할 파일

- `docs/reports/2026-07-05-wcd3-minimal-adapter-expansion.md` - 왜: 새 workflow evidence다.
- `docs/reports/2026-07-05-wce4-coverage-metric-update.md` - 왜: 기존 coverage metric baseline이다.

## 작업

service-line/workflow-surface coverage depth metric을 업데이트한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_workflow_coverage_depth_metric.py -q
python scripts\workflow_coverage_depth_metric.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. metric이 과장 없이 evidence 기반인지 확인
3. phase index 업데이트

## 금지사항

- 자동화율을 실제 현업 검증 완료율로 과장하지 마라.
