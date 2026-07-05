# Step 4: Retrieval Gate For Controlled Lane

## 읽어야 할 파일

- `docs/reports/2026-07-05-sbi3-synthetic-body-parser-chunker.md` — 왜: retrieval gate가 대상으로 삼을 synthetic chunks.
- `scripts/product_trust_quality_gate.py` — 왜: carried trust/quality gate와 연결한다.

## 작업

controlled lane chunks가 supporting interpretation 또는 legal boundary evidence로 발견되는지 검증한다. K-IFRS primary evidence를 대체하지 않는다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_controlled_lane_retrieval_gate.py -q
python scripts\controlled_lane_retrieval_gate.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. `docs/reports/2026-07-05-sbi4-controlled-lane-retrieval-gate.md` 생성 확인
3. 성공 시 step 4를 completed로 갱신

## 금지사항

- controlled source를 primary K-IFRS evidence로 승격하지 않는다.
- default retriever promotion과 이 step을 섞지 않는다.
