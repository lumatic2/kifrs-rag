# Step 4: Demo Smoke And Navigation Gate

## 읽어야 할 파일

- `docs/reports/end-to-end-demo/INDEX.md` - 왜: smoke 대상 packet이다.
- `docs/reports/2026-07-05-e2e2-scenario-contract.md` - 왜: smoke가 확인해야 할 stage contract다.

## 작업

packet의 모든 report reference가 존재하고, protected boundary strings가 없고, missing-report failure path가 설명되는지 확인하는 smoke gate를 만든다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_e2e_demo_smoke_gate.py -q
python scripts\e2e_demo_smoke_gate.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. missing report를 synthetic failure로 잡는 테스트가 있는지 확인
3. `phases/end-to-end-demo-scenario/index.json` step 업데이트

## 금지사항

- 단순 존재 확인만으로 demo-ready를 선언하지 마라. 이유: navigation과 public-safety도 DoD다.
