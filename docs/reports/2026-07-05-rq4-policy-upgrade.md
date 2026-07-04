# RQ4 Retrieval/Answer Policy Upgrade

> Horizon: `rag-quality-refresh`
> Step: RQ4 — Retrieval/Answer Policy Upgrade
> Date: 2026-07-05

## 한 줄 결론

RQ4에서는 multi-query를 바로 구현하지 않고, 먼저 **retrieval benchmark의 miss summary를 retriever별로
분리**했다. 이제 hybrid miss를 전체 retriever 실패로 오독하지 않고, lexical/hybrid/reranked 등 각
retriever가 무엇을 놓쳤는지 따로 볼 수 있다.

## Changed

### `kifrs/eval/retrieval.py`

추가:

- `miss_summary_by_retriever(report)`

변경:

- 기존 aggregate metric table은 그대로 유지한다.
- 기존 "hybrid 기준 miss" 단일 summary를 제거하고, retriever별 miss summary를 출력한다.

Before:

```text
문항별 정답 miss (top-K 밖):
  Q004: [...]
```

After:

```text
문항별 정답 miss (top-K 밖, retriever별):
  [lexical]
    Q004: [...]
  [hybrid]
    Q004: [...]
```

### `tests/test_eval_retrieval.py`

추가한 회귀 테스트:

- retriever별 miss가 섞이지 않는지 검증
- miss가 없는 retriever는 summary에서 빠지는지 검증

## Verification

### Unit test

Command:

```powershell
python -m pytest tests\test_eval_retrieval.py tests\test_quality_preflight.py -q
```

Result:

- 4 passed
- 1 warning: `.pytest_cache` permission warning

### Retrieval command

Command:

```powershell
python -m kifrs.eval.retrieval --k 20 --retrievers lexical hybrid --no-save
```

Result:

- lexical/hybrid aggregate table still prints.
- miss summary now prints `[lexical]` and `[hybrid]` separately.
- hybrid baseline remains:
  - recall@20: 0.907
  - MRR: 0.509
  - nDCG@10: 0.527

### Quality preflight

Command:

```powershell
python scripts\quality_preflight.py --format text
```

Result:

- ok: True
- public_safe: True
- protected_assets_required: False
- focused_pytest: 0
- local_rag_threshold_gate: 0
- authority_registry: 0
- authority_source_pack: 0
- user_note_v2_audit: 0

## Gate Policy

RQ4 기준으로 gate를 다음처럼 분리한다.

| Gate | Command | Purpose | Blocking? |
|---|---|---|---|
| Always-on quality preflight | `python scripts\quality_preflight.py --format text` | public-safe smoke | yes |
| Focused retrieval baseline | `python -m kifrs.eval.retrieval --k 20 --retrievers lexical hybrid --no-save` | fast retrieval regression | yes, once RQ5 formalizes thresholds |
| Full pytest | `python -m pytest tests -q` | broad regression | yes before major close |
| hierarchical/reranked full benchmark | split command only | diagnostic/long-running | no, until timeout fixed |

## Why multi-query was not implemented yet

RQ3 identified Q039/Q048 as multi-query candidates. But implementing multi-query before reporting cleanup would make
before/after evidence harder to trust. RQ4 deliberately chose the smaller precursor:

1. make misses visible per retriever,
2. keep the fast gate stable,
3. let RQ5 define quality gate thresholds,
4. then start query/policy optimization as a later step.

## Next

RQ5 should turn RQ1~RQ4 into a formal quality gate report:

- which commands are mandatory,
- which warnings are tolerated,
- which slow benchmarks are diagnostic only,
- what minimum thresholds must hold before moving to non-IFRS source ingestion.

