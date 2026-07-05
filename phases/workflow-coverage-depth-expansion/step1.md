# Step 1: Service-Line Coverage Rerank

## 읽어야 할 파일

- `docs/horizons/workflow-coverage-depth-expansion.md` - 왜: WCD1 acceptance와 horizon boundary를 확인한다.
- `docs/plans/2026-07-05-workflow-coverage-depth-expansion.md` - 왜: WCD milestone tree와 decision log를 따른다.
- `docs/practice-map/company-map.md` - 왜: firm-service map의 service-line sampling frame이다.
- `docs/practice-map/team-workflows.md` - 왜: service-line별 workflow surface를 확인한다.
- `docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md` - 왜: 기존 workflow coverage evidence다.

## 작업

`scripts/workflow_coverage_depth_rerank.py`를 만들어 service-line/workflow gaps를 automation value, evidence availability, implementation cost, public-safety boundary 기준으로 재랭킹한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_workflow_coverage_depth_rerank.py -q
python scripts\workflow_coverage_depth_rerank.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. 외부 피드백/패키징을 다음 행동으로 넣지 않는지 확인
3. phase index 업데이트

## 금지사항

- 실제 회계사에게 보낼 outreach 계획을 만들지 마라.
- packaging 작업을 이 horizon에 넣지 마라.
