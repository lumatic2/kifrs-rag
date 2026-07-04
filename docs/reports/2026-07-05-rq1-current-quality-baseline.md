# RQ1 Current Quality Baseline

> Horizon: `rag-quality-refresh`
> Step: RQ1 — Current Quality Baseline
> Date: 2026-07-05

## 한 줄 결론

현재 K-IFRS RAG 품질 gate는 **public-safe smoke / local-rag answer gate / authority metadata / user note
audit / 전체 pytest** 기준으로 통과한다. 다만 full retrieval benchmark는 5개 retriever 전체를 한 번에 돌리면
timeout이 발생해, RQ2/RQ3에서 eval coverage와 retrieval failure taxonomy를 분리해 다뤄야 한다.

## Command Inventory

### Public-safe gate

| Command | 역할 | 현재 결과 | 비고 |
|---|---|---:|---|
| `python scripts/quality_preflight.py --format json` | public-safe quality bundle | PASS | protected asset 불필요 |
| `python scripts/eval_quality_gate.py --runner local-rag --only Q019 Q020 Q021 Q022 Q023 --min-composite 0.6 --min-cite 0.45 --format json` | local-rag answer threshold | PASS | 5문항 focused gate |
| `python -m pytest tests -q` | 전체 공개 테스트 | PASS | 176 passed |
| `python -m kifrs.eval.retrieval --k 20 --retrievers lexical hybrid --no-save` | retrieval-only lexical/hybrid baseline | PASS | 50문항, 45.6s |

### Long-running / needs split

| Command | 관찰 | 다음 처리 |
|---|---|---|
| `python -m kifrs.eval.retrieval --k 20 --no-save` | 124s timeout | retriever별/문항군별로 분리 |
| `python -m kifrs.eval.retrieval --k 20 --retrievers hierarchical --no-save` | 184s timeout | RQ3에서 performance/failure bucket으로 추적 |
| `python -m kifrs.eval.retrieval --k 20 --retrievers reranked --only Q001 Q004 Q006 Q008 Q029 Q039 Q040 Q041 Q048 --no-save` | 184s timeout | miss-focused rerank gate 재설계 필요 |

### Private or local-only boundary

| Surface | 이유 |
|---|---|
| `data/eval/goldset.json` | 로컬에는 존재하지만 공개 배포 가능한 원천 데이터인지 별도 확인 필요 |
| `data/eval/manual/*` | manual answer/evidence는 local-only 평가 산출물로 취급 |
| 기준서 원문/DB/임베딩 | 저작권·재배포 금지 원칙상 공개 레포 commit 금지 |
| `kifrs-mcp` / `baseline-noretrieval` runner | 외부 모델/API 또는 MCP runtime 조건이 개입될 수 있어 public-safe gate와 분리 |

## Executed Results

### Quality preflight

Command:

```powershell
python scripts\quality_preflight.py --format json
```

Result:

- `ok`: true
- `public_safe`: true
- `protected_assets_required`: false
- focused pytest: 18 passed
- local-rag threshold gate: PASS
- authority registry: PASS, total 6
- authority source pack: PASS, total 6
- user_note_v2 audit: PASS, total 17

Warning:

- `.pytest_cache` write permission warning exists. It does not fail tests, but it should be cleaned separately if noisy.

### Local-rag threshold gate

Command:

```powershell
python scripts\eval_quality_gate.py --runner local-rag --only Q019 Q020 Q021 Q022 Q023 --min-composite 0.6 --min-cite 0.45 --format json
```

Result:

- `ok`: true
- `items`: 5
- `mean_composite`: 0.921
- `mean_cite`: 0.763
- `mean_global_rules`: 1.0
- `failing_items`: 0

Interpretation:

- 현재 answer gate는 너무 넓은 품질 보증이 아니라, Q019~Q023 focused smoke다.
- RQ2에서 질문 유형별 coverage를 확장해야 한다.

### Full public tests

Command:

```powershell
python -m pytest tests -q
```

Result:

- 176 passed
- 1 warning: `.pytest_cache` permission warning

Interpretation:

- 공개 코드 표면은 회귀 없이 통과한다.
- 이 테스트는 workflow/authority/user_note/demo까지 넓게 보지만, retrieval quality score 전체를 대체하지는 않는다.

### Retrieval lexical/hybrid baseline

Command:

```powershell
python -m kifrs.eval.retrieval --k 20 --retrievers lexical hybrid --no-save
```

Result:

| Retriever | recall@1 | recall@3 | recall@5 | recall@10 | recall@20 | MRR | NDCG@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| lexical | 0.153 | 0.330 | 0.407 | 0.517 | 0.723 | 0.366 | 0.363 |
| hybrid | 0.227 | 0.427 | 0.597 | 0.763 | 0.907 | 0.509 | 0.527 |

Top-20 miss list under hybrid reference output:

- Q001: 1115-27
- Q004: 1001-69
- Q006: 1115-51
- Q008: 1109-2.1
- Q029: 1116-45
- Q039: 1037-14
- Q040: 1109-4.1.4
- Q041: 1102-11
- Q048: 1036-18

Interpretation:

- hybrid recall@20 0.907 is usable as a baseline.
- misses are not random. Some are likely query wording/section boundary problems, and Q039/Q048 were already known as multi-query candidates in the previous RAG optimization notes.

### Semantic focused baseline

Command:

```powershell
python -m kifrs.eval.retrieval --k 20 --retrievers semantic --only Q019 Q020 Q021 Q022 Q023 --no-save
```

Result:

| Retriever | recall@1 | recall@3 | recall@5 | recall@10 | recall@20 | MRR | NDCG@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| semantic | 0.200 | 0.600 | 0.600 | 0.600 | 0.900 | 0.529 | 0.523 |

Miss:

- Q022: 1019-127

Interpretation:

- semantic retriever itself works on a focused set.
- full semantic/hierarchical/reranked evaluation needs runtime splitting or timeout tuning.

## Coverage Gaps for RQ2

RQ1 confirms that current quality gates do not yet cover all question types evenly.

Needed buckets:

- direct paragraph lookup
- cross-paragraph judgement
- cross-standard judgement
- workflow seed scenario
- disclosure generation
- source pack / user note dependent answer
- citation conflict / insufficient evidence
- long-running retrieval benchmark

## Failure Buckets for RQ3

Initial candidates:

- timeout/performance: hierarchical and reranked retrieval commands did not finish within 180s.
- query wording miss: Q001, Q006, Q029 class candidates.
- section/chapter boundary miss: Q004, Q041 candidates.
- exact paragraph identifier miss: Q008, Q040 candidates.
- multi-query decomposition miss: Q039, Q048 candidates.
- semantic focused miss: Q022.

## RQ1 Decision

RQ1 is complete enough to move to RQ2.

What is proven:

- public-safe quality preflight passes.
- local-rag answer gate passes on the focused Q019~Q023 set.
- full public tests pass.
- lexical/hybrid retrieval baseline is measurable and gives concrete miss IDs.

What remains deliberately open:

- full retrieval benchmark cannot be the default gate until timeout is fixed or split.
- evaluation coverage is currently focused and must be expanded by question type.
- failure taxonomy needs item-level diagnosis, not just aggregate metrics.

