# Step 3: Synthetic Body Parser And Chunker

## 읽어야 할 파일

- `docs/reports/2026-07-05-sbi2-source-body-policy-record.md` — 왜: parser/chunker가 따라야 할 policy boundary.
- `docs/horizons/source-body-ingestion-controlled-lane.md` — 왜: protected body text commit 금지 조건.

## 작업

실제 protected text가 아닌 synthetic body fixture를 parser/chunker dry-run으로 변환한다. chunk output은 public-safe metadata와 short synthetic text only로 제한한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_synthetic_body_parser_chunker.py -q
python scripts\synthetic_body_parser_chunker.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. `docs/reports/2026-07-05-sbi3-synthetic-body-parser-chunker.md` 생성 확인
3. 성공 시 step 3을 completed로 갱신

## 금지사항

- protected source text, scrape result, copied regulatory body를 fixture로 쓰지 않는다.
- embedding dump나 private payload를 만들지 않는다.
