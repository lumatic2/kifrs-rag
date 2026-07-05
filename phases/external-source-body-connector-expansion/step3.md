# Step 3: Chunking And Retrieval Dry Run

## 읽어야 할 파일

- `docs/reports/2026-07-05-esb2-source-body-fixture-contract.md` - 왜: synthetic chunks의 input contract다.

## 작업

synthetic chunks와 retrieval result metadata를 dry-run한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_external_source_body_chunk_retrieval_dry_run.py -q
python scripts\external_source_body_chunk_retrieval_dry_run.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. chunk/report가 public-safe인지 확인
3. phase index 업데이트

## 금지사항

- protected body text를 검색 결과로 출력하지 마라.
