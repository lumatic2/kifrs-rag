# Step 5: Local Parser Prototype Close Gate

## 읽어야 할 파일

- `phases/real-local-parser-prototype/index.json` — 왜: RLP1~RLP4 completion status 확인.
- `docs/reports/2026-07-05-rlp1-parser-prototype-asset-inventory.md` — 왜: inventory evidence.
- `docs/reports/2026-07-05-rlp2-local-fixture-parser-adapter.md` — 왜: adapter evidence.
- `docs/reports/2026-07-05-rlp3-deletion-automation-simulation.md` — 왜: deletion simulation evidence.
- `docs/reports/2026-07-05-rlp4-private-payload-leak-tests.md` — 왜: leak-test evidence.

## 작업

RLP1~RLP4 evidence를 묶어 real-local-parser-prototype close gate를 만든다. close result는 synthetic/local-safe prototype
완료 여부와 아직 남은 real private file boundary를 명확히 분리한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_real_local_parser_prototype_close_gate.py -q
python scripts\real_local_parser_prototype_close_gate.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. `docs/reports/2026-07-05-real-local-parser-prototype-close-report.md` 생성 확인
3. 성공 시 `phases/real-local-parser-prototype/index.json` step 5와 horizon을 completed로 갱신

## 금지사항

- 실제 private parser, OCR, upload UI, private embedding을 구현했다고 주장하지 않는다.
- close report에 protected data나 private payload를 넣지 않는다.
