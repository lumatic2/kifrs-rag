# Step 2: Current Retriever Baseline Snapshot

## 읽어야 할 파일

- `phases/rag-quality-fresh-validation/index.json` - 왜: RQF1 완료 summary를 이어받는다.
- `docs/reports/2026-07-05-rqf1-validation-contract.md` - 왜: baseline snapshot의 metric/threshold 계약이다.

## 작업

현재 default retriever baseline을 public-safe metadata 기준으로 스냅샷한다. local private eval asset이 필요하면 blocked가 아니라 missing-local-evidence로 명시하고 default 변경은 계속 금지한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_rag_quality_baseline_snapshot.py -q
python scripts\rag_quality_baseline_snapshot.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. baseline report가 missing evidence와 pass/fail을 분리하는지 확인
3. `phases/rag-quality-fresh-validation/index.json` step 업데이트

## 금지사항

- local private eval data를 공개 report에 넣지 마라.
