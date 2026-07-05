# Step 5: Controlled Lane Close Gate

## 읽어야 할 파일

- `phases/source-body-ingestion-controlled-lane/index.json` — 왜: SBI1~SBI4 completion status 확인.
- `docs/reports/2026-07-05-sbi1-source-class-selection.md` — 왜: source selection evidence.
- `docs/reports/2026-07-05-sbi2-source-body-policy-record.md` — 왜: policy evidence.
- `docs/reports/2026-07-05-sbi3-synthetic-body-parser-chunker.md` — 왜: parser/chunker evidence.
- `docs/reports/2026-07-05-sbi4-controlled-lane-retrieval-gate.md` — 왜: retrieval evidence.

## 작업

authorization, policy, parser/chunker, retrieval, public-safe, and carried RAG regressions를 묶어 controlled lane close 여부를 판정한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_controlled_lane_close_gate.py -q
python scripts\controlled_lane_close_gate.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. `docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md` 생성 확인
3. 성공 시 step 5와 horizon을 completed로 갱신

## 금지사항

- authorization이 없는 실제 source body를 저장했다고 주장하지 않는다.
- public-safe synthetic lane을 실제 data ingestion으로 과장하지 않는다.
