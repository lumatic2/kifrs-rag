# Step 1: Validation Corpus And Acceptance Contract

## 읽어야 할 파일

- `docs/horizons/rag-quality-fresh-validation.md` - 왜: RQF1 acceptance와 horizon boundary를 확인한다.
- `docs/plans/2026-07-05-rag-quality-fresh-validation.md` - 왜: RQF milestone tree와 결정 로그를 따른다.
- `docs/reports/2026-07-05-accounting-intelligence-gap-audit.md` - 왜: RAG 품질이 왜 첫 objective-gap horizon인지 근거다.
- `docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md` - 왜: 기존 retriever promotion defer evidence다.
- `docs/reports/2026-07-05-default-retriever-guard.md` - 왜: default retriever 변경 금지/허용 조건의 현재 증거다.

## 작업

`scripts/rag_quality_validation_contract.py`를 만들어 RAG 품질 검증에 사용할 command, metric, threshold, public-safety boundary, promotion blocker를 명시한다. 이 step은 실제 default retriever를 바꾸지 않는다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_rag_quality_validation_contract.py -q
python scripts\rag_quality_validation_contract.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. 보고서에 protected local data path나 secret이 없는지 확인
3. `phases/rag-quality-fresh-validation/index.json` step 업데이트

## 금지사항

- default retriever를 변경하지 마라. 이유: RQF1은 계약 단계다.
- 기준서 원문, DB dump, embeddings, dogfood, private payload를 출력하지 마라. 이유: 공개 가능 경계.
