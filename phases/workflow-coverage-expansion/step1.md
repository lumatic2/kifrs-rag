# Step 1: Coverage Gap Ranking

## 읽어야 할 파일
- docs/OBJECTIVE.md — 왜: 업무 지도 커버리지와 시나리오 완료율 축을 ranking 기준으로 쓴다.
- docs/horizons/workflow-coverage-expansion.md — 왜: 이 horizon의 WCE1 acceptance와 후속 milestone 경계를 확인한다.
- docs/plans/2026-07-05-workflow-coverage-expansion.md — 왜: WCE1 step tree와 decision log를 따른다.
- docs/reports/2026-07-05-product-weakness-horizon-candidates.md — 왜: 제품 약점 queue에서 WCE가 왜 다음인지 연결한다.
- docs/horizons/firm-service-map.md — 왜: 회계법인 팀과 workflow map을 ranking 후보의 근거로 쓴다.

## 작업
firm-service map과 기존 자동화 증거를 바탕으로 다음 workflow 후보를 점수화한다. 후보는 적어도 1113 fair value, 1036 impairment, 1037 provisions, 1110 consolidation, disclosure/closing support를 포함한다. 점수 기준은 firm-service value, data availability, determinism, verification cost이며, 결과는 다음 WCE2에서 하나의 workflow contract로 이어질 수 있어야 한다.

## Acceptance Criteria
```bash
python -m pytest tests\test_workflow_coverage_gap_ranking.py -q
python scripts\workflow_coverage_gap_ranking.py --format text --write
```

## 검증 절차
1. AC 커맨드 실행.
2. ranking 결과가 후보별 점수, 추천 후보, 근거, 한계를 포함하는지 확인.
3. 공개 리포트에 기준서 원문, private payload, secret, raw source body가 들어가지 않았는지 확인.
4. `phases/workflow-coverage-expansion/index.json` step 1 상태를 completed로 갱신한다.

## 금지사항
- 실제 외부 회계사 연락이나 피드백 세션을 reopen하지 마라. 이유: 사용자가 명시적으로 계획에서 제외했다.
- 기준서 원문, private client payload, parsed DB, embedding dump를 commit하지 마라. 이유: 공개 레포 경계.
