# Step 4: Operator Promotion Command

## 읽어야 할 파일
- docs/reports/2026-07-05-rpg1-promotion-evidence-inventory.md — 왜: command가 표시할 evidence inventory다.
- docs/reports/2026-07-05-rpg2-regression-latency-gate.md — 왜: command가 표시할 gate result다.
- docs/reports/2026-07-05-rpg3-failure-rollback-policy.md — 왜: command가 표시할 rollback policy다.

## 작업
operator가 promote/defer 상태와 required evidence를 한 번에 볼 수 있는 dry-run command/report를 만든다. 이 command는 runtime default를 바꾸지 않는다.

## Acceptance Criteria
```bash
python -m pytest tests\test_retriever_promotion_command.py -q
python scripts\retriever_promotion_command.py --format text --write
```

## 검증 절차
1. AC 커맨드 실행.
2. output이 promote/defer/block 후보, missing evidence, rollback path를 표시하는지 확인.
3. phase index step 4 상태를 completed로 갱신한다.

## 금지사항
- dry-run command에서 설정 파일을 실제 변경하지 마라.
