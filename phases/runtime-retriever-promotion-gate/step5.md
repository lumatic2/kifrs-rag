# Step 5: Promotion Gate Close Report

## 읽어야 할 파일
- docs/reports/2026-07-05-rpg1-promotion-evidence-inventory.md — 왜: close gate의 evidence inventory 입력이다.
- docs/reports/2026-07-05-rpg2-regression-latency-gate.md — 왜: promote/defer 판단의 regression 입력이다.
- docs/reports/2026-07-05-rpg3-failure-rollback-policy.md — 왜: rollback evidence 입력이다.
- docs/reports/2026-07-05-rpg4-operator-promotion-command.md — 왜: operator surface 입력이다.
- docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md — 왜: 직전 horizon close evidence를 이어받는다.

## 작업
RPG1~RPG4 evidence를 묶어 `promote`, `defer`, `block` 중 하나로 close result를 낸다. 다음 horizon은 operator-experience-hardening이다.

## Acceptance Criteria
```bash
python -m pytest tests\test_runtime_retriever_promotion_close_gate.py -q
python scripts\runtime_retriever_promotion_close_gate.py --format text --write
```

## 검증 절차
1. AC 커맨드 실행.
2. close result와 rollback evidence가 함께 있는지 확인.
3. ROADMAP, horizon doc, phase index를 completed/next active로 갱신한다.

## 금지사항
- 증거가 약한데 promote로 닫지 마라. `defer`는 유효한 제품 결정이다.
