# Step 2: Local Fixture Parser Adapter

## 읽어야 할 파일

- `phases/real-local-parser-prototype/step1.md` — 왜: RLP1이 확정한 reusable asset과 gap을 이어받는다.
- `docs/reports/2026-07-05-rlp1-parser-prototype-asset-inventory.md` — 왜: adapter 구현에 쓸 자산 경계를 확인한다.
- `kifrs/feedback/local_parser.py` — 왜: adapter contract와 dry-run gate의 구현 위치.
- `kifrs/feedback/case_intake.py` — 왜: structured facts와 review-pack routing 경계.

## 작업

local-safe fixture-like 입력을 structured facts와 review questions로 변환하는 adapter를 구현한다.
출력은 structured facts only이며 raw private text를 복사하지 않는다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_local_fixture_parser_adapter.py -q
python scripts\local_fixture_parser_adapter.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. `docs/reports/2026-07-05-rlp2-local-fixture-parser-adapter.md` 생성 확인
3. 성공 시 `phases/real-local-parser-prototype/index.json` step 2를 completed로 갱신

## 금지사항

- actual private file parsing, OCR, private embedding namespace를 구현하지 않는다.
- protected payload를 public artifact에 남기지 않는다.
