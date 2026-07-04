# RQ1 — Current Quality Baseline

## Objective

현재 K-IFRS RAG 품질을 다시 측정하기 위한 baseline을 만든다. 이번 step은 바로 최적화하지 않고,
"현재 무엇을 검증할 수 있고, 어떤 실패가 보이는지"를 먼저 고정한다.

## Work

1. 현재 품질/평가/테스트 스크립트 inventory를 만든다.
2. public-safe command와 private-data command를 분리한다.
3. 실행 가능한 command를 돌려 현재 결과를 기록한다.
4. 실패/경고/coverage gap을 다음 RQ2~RQ4 작업 후보로 분류한다.

## Deliverable

- `docs/reports/2026-07-05-rq1-current-quality-baseline.md`

## Verification Candidates

```powershell
python scripts/quality_preflight.py --format text
python -m pytest tests/test_demo_poc.py tests/test_audit_analytics.py tests/test_statement_draft.py
git diff --check
```

