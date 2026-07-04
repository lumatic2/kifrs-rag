# RQ5 — Quality Gate Report

## Objective

RQ1~RQ4 결과를 하나의 품질 gate 기준으로 정리한다. 이 step은 `rag-quality-refresh` horizon을 닫을지
판단하기 위한 최종 report를 만든다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-rq1-current-quality-baseline.md` — 왜: 현재 실행 결과와 timeout baseline.
- `docs/reports/2026-07-05-rq2-eval-coverage-refresh.md` — 왜: gate coverage gap.
- `docs/reports/2026-07-05-rq3-retrieval-failure-taxonomy.md` — 왜: failure buckets.
- `docs/reports/2026-07-05-rq4-policy-upgrade.md` — 왜: 코드 변경과 gate split policy.
- `docs/horizons/accounting-intelligence-expansion.md` — 왜: 다음 horizon(source map/ingestion)으로 넘어갈 조건.

## 작업

1. mandatory gate / diagnostic gate / private-local gate를 구분한다.
2. 다음 horizon으로 넘어가기 위한 minimum quality 조건을 적는다.
3. 남은 RAG 개선 backlog를 RQ 이후 후보로 분리한다.
4. `rag-quality-refresh` horizon close 여부를 판단한다.

## Acceptance Criteria

```powershell
python scripts\quality_preflight.py --format text
python -m pytest tests\test_eval_retrieval.py tests\test_quality_preflight.py -q
python -m kifrs.eval.retrieval --k 20 --retrievers lexical hybrid --no-save
git diff --check
```

## Deliverable

- `docs/reports/2026-07-05-rq5-quality-gate-report.md`

## 금지사항

- RQ5에서 새 retrieval 최적화를 추가하지 않는다. 이유: gate report는 close 판단 문서다.
- 다음 horizon을 구현하지 않는다. 이유: source ingestion은 gate 조건 확인 후 별도 horizon에서 시작한다.

