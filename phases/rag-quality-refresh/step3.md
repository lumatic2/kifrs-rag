# RQ3 — Retrieval Failure Taxonomy

## Objective

RQ1/RQ2에서 확인한 retrieval miss와 timeout을 실패 유형별로 분류한다. 이번 step의 목표는 바로
retriever를 고치는 것이 아니라, 어떤 실패가 query rewriting, metadata, reranking, timeout, gate
reporting 중 어디에 속하는지 구분하는 것이다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-rq1-current-quality-baseline.md` — 왜: 실제 timeout과 miss ID baseline을 이어받는다.
- `docs/reports/2026-07-05-rq2-eval-coverage-refresh.md` — 왜: coverage bucket과 RQ3 candidate list를 이어받는다.
- `docs/reports/2026-07-03-ro1-deep-miss-diagnosis.md` — 왜: 이전 RO1의 miss 분류와 이번 baseline을 비교한다.
- `kifrs/eval/retrieval.py` — 왜: miss 출력과 retriever별 평가 방식을 확인한다.
- `kifrs/embed.py` / `kifrs/store.py` — 왜: lexical/semantic/hybrid/hierarchical/reranked 경계를 확인한다.

## 작업

1. RQ2 candidate item을 failure bucket별로 분류한다.
2. 이전 RO1 진단과 이번 RQ1 결과가 일치하는지 비교한다.
3. timeout/performance 문제와 retrieval quality miss를 분리한다.
4. RQ4에서 구현할 최소 policy/code 후보를 우선순위로 제안한다.

## Acceptance Criteria

```powershell
python scripts\quality_preflight.py --format text
git diff --check
```

## Deliverable

- `docs/reports/2026-07-05-rq3-retrieval-failure-taxonomy.md`

## 금지사항

- RQ3에서는 retriever 코드를 고치지 않는다. 이유: taxonomy 없이 고치면 효과 측정 기준이 흐려진다.
- 기준서 원문이나 문제 원문을 report에 복사하지 않는다. 이유: 공개 레포 경계 유지.

