# Step 2: Scenario Contract

## 읽어야 할 파일

- `phases/end-to-end-demo-scenario/index.json` - 왜: E2E1 완료 summary를 이어받는다.
- `docs/reports/2026-07-05-e2e1-demo-asset-inventory.md` - 왜: E2E2가 계약화할 demo stages의 입력이다.

## 작업

E2E1 inventory를 기반으로 demo stage contract를 만든다. 각 stage는 input, evidence, output, review checkpoint, operator command, failure boundary를 가져야 한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_e2e_scenario_contract.py -q
python scripts\e2e_scenario_contract.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. contract가 stage 누락과 protected-output 위험을 잡는지 확인
3. `phases/end-to-end-demo-scenario/index.json` step 업데이트

## 금지사항

- 실제 외부 피드백 또는 실사용자 인터뷰를 전제로 삼지 마라. 이유: 이 horizon 범위 밖이다.
