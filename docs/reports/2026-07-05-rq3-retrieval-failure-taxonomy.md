# RQ3 Retrieval Failure Taxonomy

> Horizon: `rag-quality-refresh`
> Step: RQ3 — Retrieval Failure Taxonomy
> Date: 2026-07-05

## 한 줄 결론

현재 retrieval 문제는 한 종류가 아니다. **hybrid 후보 풀 밖으로 밀리는 진짜 검색 실패**, **reranked가
회복했는데 콘솔 miss가 hybrid 기준이라 오해되는 reporting 실패**, **hierarchical/reranked full
benchmark가 timeout되는 performance 실패**가 섞여 있다. RQ4는 이 셋을 분리해 가장 작은 code/policy
개선부터 해야 한다.

## Retriever Boundary

현재 retriever 경계는 다음과 같다.

| Retriever | 구현 | 역할 | RQ3 관찰 |
|---|---|---|---|
| lexical | `store.search_fts` | `expand_query()` 후 FTS5/BM25, fallback LIKE | 빠르고 full 50-item 가능 |
| semantic | `embed.semantic_search` | query embedding vs paragraph embedding cosine | focused set 가능, full run은 비용 고려 필요 |
| hybrid | `embed.search_hybrid` | lexical 50 + semantic 50 RRF | 현재 안정 baseline, recall@20 0.907 |
| hierarchical | `embed.search_hierarchical` | section centroid + hybrid 3-way RRF | full run 180s timeout |
| reranked | `embed.search_reranked` | hybrid candidate 50 -> cross-encoder rerank | miss-focused run도 180s timeout |

Important implementation detail:

- `search_reranked()`는 `search_hybrid(..., limit=candidates)` 후보 풀 안에서만 재정렬한다.
- 따라서 정답이 hybrid candidate pool 밖이면 reranker로는 해결되지 않는다.
- `retrieval.py`의 miss 출력은 hybrid가 있으면 hybrid 기준을 대표로 보여준다. 여러 retriever를 같이 돌릴 때 이 출력은 "전체 retriever miss"가 아니다.

## Failure Buckets

### F1. True first-stage retrieval miss

정의:

- lexical/semantic/hybrid 1차 후보에 정답 문단이 충분히 올라오지 않는 경우.
- reranked로도 해결되기 어렵다. 이유: reranked는 hybrid 후보 풀 안에서만 재정렬한다.

Current candidates:

| Item | Anchor | Likely reason | RQ4 implication |
|---|---|---|---|
| Q001 | 1115-27 | 사례 표현과 기준서 추상 문구 사이 어휘 부재 | term bridge보다 query decomposition/metadata 필요 |
| Q006 | 1115-51 | 일반어가 많아 특정 문단 판별력 약함 | section/paragraph distinctive signal 검토 |
| Q008 | 1109-2.1 | scope 문단, 기준서 전체의 흔한 용어에 묻힘 | exact scope/rule query expansion 후보 |
| Q029 | 1116-45 | 리스/리스부채 일반어 과다 | standard-local discriminative keyword 필요 |
| Q040 | 1109-4.1.4 | classification rule과 사례 표현 간 gap | term bridge 또는 rule-title metadata 후보 |

### F2. Cross-concept / multi-query miss

정의:

- 질문이 둘 이상의 회계 개념 또는 기준서를 건드리며, 단일 query embedding/FTS가 한쪽 개념으로 쏠리는 경우.

Current candidates:

| Item | Anchor | Likely reason | RQ4 implication |
|---|---|---|---|
| Q039 | 1037-14 | 리스 원상복구와 충당부채 인식 요건이 섞임 | multi-query decomposition 최우선 후보 |
| Q048 | 1036-18 | 손상/회수가능액 하위개념이 섞임 | multi-query decomposition 후보 |

Why this matters:

- 이전 RO1도 카테고리 C를 가장 가치 있는 다음 개선으로 봤다.
- K-IFRS 외 정보원까지 붙이면 cross-concept 질문은 더 늘어난다.

### F3. Reporting / interpretation failure

정의:

- retriever 자체가 회복한 결과를 콘솔 summary가 다른 기준으로 보여줘 사람이 오독하는 경우.

Current candidates:

| Item | Observation | RQ4 implication |
|---|---|---|
| Q004 | RO1에서 reranked rank 6으로 회복됐으나 hybrid miss summary에 계속 표시 | per-retriever miss report 필요 |
| Q041 | RO1에서 reranked rank 13으로 회복됐으나 hybrid miss summary에 계속 표시 | per-retriever miss report 필요 |

Why this matters:

- "검색이 못 찾는다"와 "hybrid는 못 찾지만 reranked는 찾는다"는 다른 문제다.
- RQ4에서 가장 작고 안전한 code improvement는 `retrieval.py`의 miss 출력 개선이다.

### F4. Timeout / benchmark operability failure

정의:

- 품질 자체와 별개로 benchmark command가 기본 시간 예산 안에 끝나지 않아 gate로 쓸 수 없는 경우.

Observed:

| Command | Result |
|---|---|
| `python -m kifrs.eval.retrieval --k 20 --no-save` | 124s timeout |
| `python -m kifrs.eval.retrieval --k 20 --retrievers hierarchical --no-save` | 184s timeout |
| `python -m kifrs.eval.retrieval --k 20 --retrievers reranked --only ... --no-save` | 184s timeout |

Likely cause:

- hierarchical는 section centroid 계산과 embedding matrix work가 heavy하다.
- reranked는 cross-encoder scoring이 heavy하고, candidate 50 x item count 비용이 크다.
- current CLI에는 benchmark split/profile preset이 없다.

RQ4 implication:

- default quality gate에는 lexical/hybrid full run 또는 focused retrieval subset만 넣는다.
- slow retrievers는 separate long-running gate나 item subset gate로 분리한다.

### F5. Coverage metadata failure

정의:

- goldset item이 어떤 task type인지 metadata가 없어 gate 구성이 수작업/추정에 의존하는 경우.

Observed:

- goldset schema has `source`, `source_ref`, `must_cite`, `may_cite`, `keywords`, `forbidden_keywords`, `notes`.
- no explicit `task_type`, `source_type`, `difficulty`, `workflow_domain`, `coverage_bucket`.

RQ4 implication:

- 코드 변경 최소 후보는 별도 sidecar coverage map을 두는 것이다.
- goldset 자체를 직접 바꾸는 것은 local-only/public boundary를 먼저 확인해야 한다.

## Priority for RQ4

RQ4에서 바로 구현/정책화할 후보는 우선순위가 다르다.

| Priority | Candidate | Why |
|---:|---|---|
| 1 | `retrieval.py` per-retriever miss reporting | 작고 안전하며 RO1 오독을 바로 줄임 |
| 2 | quality gate split policy | timeout gate와 always-on gate를 분리해야 함 |
| 3 | focused retrieval subset/preset | slow retriever를 운영 가능하게 함 |
| 4 | multi-query decomposition prototype | Q039/Q048에 효과 가능, 하지만 구현 blast radius가 큼 |
| 5 | goldset coverage sidecar | RQ5 gate report에 유용하지만 데이터 경계 확인 필요 |

## Recommended RQ4 Scope

RQ4는 한 번에 multi-query까지 가기보다 다음 작은 changeset부터 닫는 것이 맞다.

1. `kifrs.eval.retrieval` miss output을 retriever별로 보여주도록 개선한다.
2. full slow retriever timeout을 release blocker로 보지 않도록 gate policy를 문서화한다.
3. 필요하면 `--miss-report all|reference` 같은 작은 CLI 옵션을 추가한다.

이렇게 해야 RQ4 이후에도 "무엇이 실제 검색 실패이고 무엇이 리포트 문제인지"를 착각하지 않는다.

