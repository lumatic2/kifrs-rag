# Step 1: Operator Command Inventory

## 읽어야 할 파일
- docs/horizons/operator-experience-hardening.md — 왜: OEH1 acceptance와 horizon 경계를 확인한다.
- docs/plans/2026-07-05-operator-experience-hardening.md — 왜: OEH milestone tree와 decision log를 따른다.
- docs/reports/2026-07-05-product-weakness-horizon-candidates.md — 왜: operator hardening이 제품 약점 queue의 마지막 horizon인 이유를 연결한다.
- docs/reports/2026-07-05-accounting-intelligence-progress-map.md — 왜: 현재 active horizon과 다음 leaf를 operator inventory에 반영한다.

## 작업
operator가 목적별로 실행할 명령을 inventory한다. 그룹은 demo/readiness, quality/RAG, parser/private, source/authority, workflow/coverage, retriever promotion, diagnostics/recovery를 포함한다.

## Acceptance Criteria
```bash
python -m pytest tests\test_operator_command_inventory.py -q
python scripts\operator_command_inventory.py --format text --write
```

## 검증 절차
1. AC 커맨드 실행.
2. inventory가 operator goal, command, report, safety note를 포함하는지 확인.
3. phase index step 1 상태를 completed로 갱신한다.

## 금지사항
- protected data path, secret, raw source text를 command output에 넣지 마라.
