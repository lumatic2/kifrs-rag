# Step 3: Failure And Rollback Policy

## 읽어야 할 파일
- docs/reports/2026-07-05-rpg2-regression-latency-gate.md — 왜: 실패/보류 조건을 rollback policy와 연결한다.
- docs/reports/2026-07-05-ptq3-failure-boundary-matrix.md — 왜: 기존 failure boundary를 재사용한다.
- docs/horizons/runtime-retriever-promotion-gate.md — 왜: RPG3 acceptance를 확인한다.

## 작업
retriever promotion이 실패하거나 runtime에서 문제를 만들 때 current default로 되돌아가는 rollback policy를 정의하고 검증한다.

## Acceptance Criteria
```bash
python -m pytest tests\test_retriever_failure_rollback_policy.py -q
python scripts\retriever_failure_rollback_policy.py --format text --write
```

## 검증 절차
1. AC 커맨드 실행.
2. rollback states, failure cases, operator remediation이 모두 있는지 확인.
3. phase index step 3 상태를 completed로 갱신한다.

## 금지사항
- rollback 없는 promotion path를 만들지 마라.
