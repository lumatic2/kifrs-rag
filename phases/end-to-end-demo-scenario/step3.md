# Step 3: Demo Packet Builder

## 읽어야 할 파일

- `docs/reports/2026-07-05-e2e1-demo-asset-inventory.md` - 왜: packet에 포함할 demo order의 출처다.
- `docs/reports/2026-07-05-e2e2-scenario-contract.md` - 왜: packet이 따라야 할 stage contract다.

## 작업

`docs/reports/end-to-end-demo/INDEX.md`를 생성하는 builder를 만든다. packet은 demo narrative, ordered reports, rerun commands, recovery hints를 포함한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_e2e_demo_packet_builder.py -q
python scripts\e2e_demo_packet_builder.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. packet link와 command가 local/public-safe 경계 안에 있는지 확인
3. `phases/end-to-end-demo-scenario/index.json` step 업데이트

## 금지사항

- 패키징이나 설치 배포를 완료된 것처럼 말하지 마라. 이유: 이 horizon은 demo scenario다.
