# Step 5: Horizon Close Gate

## 읽어야 할 파일

- `docs/reports/2026-07-05-e2e1-demo-asset-inventory.md` - 왜: asset/storyboard evidence다.
- `docs/reports/2026-07-05-e2e2-scenario-contract.md` - 왜: scenario contract evidence다.
- `docs/reports/end-to-end-demo/INDEX.md` - 왜: demo packet evidence다.
- `docs/reports/2026-07-05-e2e4-demo-smoke-gate.md` - 왜: smoke/navigation evidence다.

## 작업

E2E1~E2E4 evidence를 묶어 end-to-end demo scenario를 close한다. 결과는 demo-ready, partial, blocked 중 하나여야 하며 다음 integration horizon을 명시한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_e2e_demo_close_gate.py -q
python scripts\e2e_demo_close_gate.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. ROADMAP/OBJECTIVE/phase 상태를 close 결과와 동기화한다
3. `phases/end-to-end-demo-scenario/index.json` step 업데이트

## 금지사항

- close gate가 실패했는데 ROADMAP을 완료로 바꾸지 마라. 이유: 상태판 신뢰성.
