# RQ4 — Retrieval/Answer Policy Upgrade

## Objective

RQ3에서 확인한 실패 유형 중 가장 작고 안전한 개선부터 구현한다. 이번 step은 multi-query 전체 구현이
아니라, retrieval benchmark가 오해를 만들지 않도록 miss reporting과 gate policy를 개선하는 것을
우선한다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-rq3-retrieval-failure-taxonomy.md` — 왜: RQ4 우선순위와 scope를 이어받는다.
- `kifrs/eval/retrieval.py` — 왜: miss output 개선 대상이다.
- `tests/` 내 retrieval 관련 테스트 — 왜: 새 reporting behavior를 회귀 테스트로 고정한다.
- `scripts/quality_preflight.py` — 왜: default gate에 어떤 retrieval command를 넣을지 판단한다.

## 작업

1. `kifrs.eval.retrieval`의 miss summary가 retriever별 miss를 보여주도록 개선한다.
2. 기존 출력과 호환되도록 aggregate table은 유지한다.
3. 작은 테스트를 추가해 hybrid와 reranked miss를 구분해 출력하는 helper를 검증한다.
4. RQ4 report에 gate policy를 기록한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_eval_retrieval.py tests\test_quality_preflight.py -q
python -m kifrs.eval.retrieval --k 20 --retrievers lexical hybrid --no-save
python scripts\quality_preflight.py --format text
git diff --check
```

## Deliverable

- code patch
- regression test
- `docs/reports/2026-07-05-rq4-policy-upgrade.md`

## 금지사항

- 이번 step에서 multi-query decomposition을 구현하지 않는다. 이유: reporting/gate 오독 제거가 선행되어야 한다.
- slow retriever full benchmark를 preflight에 넣지 않는다. 이유: RQ1에서 timeout이 확인됐다.

