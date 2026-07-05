# Step 4: Coverage Metric Update

## 읽어야 할 파일
- docs/OBJECTIVE.md — 왜: coverage axis의 의미와 측정법을 확인한다.
- docs/reports/2026-07-05-wce3-minimal-review-pack-adapter.md — 왜: 새 workflow가 coverage에 들어갈 수 있는지 증거로 쓴다.
- scripts/accounting_intelligence_gap_audit.py — 왜: 기존 automation snapshot 계산 방식을 확인한다.

## 작업
새 workflow 후보를 objective coverage map에 반영하는 metric/report를 구현한다. 구현된 것, 조건부인 것, 아직 불가한 것을 분리해 제품 설명이 과장되지 않게 한다.

## Acceptance Criteria
```bash
python -m pytest tests\test_workflow_coverage_metric_update.py -q
python scripts\workflow_coverage_metric_update.py --format text --write
```

## 검증 절차
1. AC 커맨드 실행.
2. coverage report가 새 workflow의 capability와 limits를 모두 포함하는지 확인.
3. `phases/workflow-coverage-expansion/index.json` step 4 상태를 completed로 갱신한다.

## 금지사항
- coverage 비율을 근거 없이 부풀리지 마라.
