# RQ5 Quality Gate Report

> Horizon: `rag-quality-refresh`
> Step: RQ5 — Quality Gate Report
> Date: 2026-07-05

## 한 줄 결론

`rag-quality-refresh`는 닫아도 된다. K-IFRS RAG의 현재 품질 기준선, coverage gap, failure taxonomy,
retrieval reporting 개선, 다음 horizon 진입 gate가 문서화됐다. 다음 단계는 RAG를 더 포장하는 것이
아니라 **Authority Source Map / multi-source ingestion 설계**로 넘어가는 것이다.

## What RQ1~RQ4 Established

| Step | Result | Evidence |
|---|---|---|
| RQ1 | 현재 품질 baseline 고정 | `docs/reports/2026-07-05-rq1-current-quality-baseline.md` |
| RQ2 | eval coverage gap 확인 | `docs/reports/2026-07-05-rq2-eval-coverage-refresh.md` |
| RQ3 | retrieval failure taxonomy 분리 | `docs/reports/2026-07-05-rq3-retrieval-failure-taxonomy.md` |
| RQ4 | per-retriever miss reporting 구현 | `kifrs/eval/retrieval.py`, `tests/test_eval_retrieval.py`, `docs/reports/2026-07-05-rq4-policy-upgrade.md` |

## Mandatory Gates

다음 horizon으로 넘어가도 매번 유지해야 하는 gate다.

### G1. Public-safe quality preflight

Command:

```powershell
python scripts\quality_preflight.py --format text
```

Required result:

- `ok: True`
- `public_safe: True`
- `protected_assets_required: False`
- all bundled command return codes = 0

Blocks progress if:

- any bundled command fails
- public_safe becomes false
- protected assets become required for preflight

### G2. Retrieval reporting regression

Command:

```powershell
python -m pytest tests\test_eval_retrieval.py tests\test_quality_preflight.py -q
```

Required result:

- tests pass
- retriever별 miss summary helper remains covered

Blocks progress if:

- retriever miss reporting collapses back to a single hybrid-only summary
- quality preflight no longer declares public-safe commands

### G3. Fast retrieval baseline

Command:

```powershell
python -m kifrs.eval.retrieval --k 20 --retrievers lexical hybrid --no-save
```

Required minimum for now:

- command completes within normal interactive session time
- hybrid recall@20 remains close to the RQ1/RQ4 baseline of 0.907
- output prints retriever별 miss sections

Blocks progress if:

- command fails
- hybrid recall@20 materially regresses without explanation
- miss output no longer separates retrievers

### G4. Broad regression before horizon close

Command:

```powershell
python -m pytest tests -q
```

Required result:

- all public tests pass

Current known tolerated warning:

- `.pytest_cache` permission warning. It is noisy but non-blocking unless it starts hiding test failures.

## Diagnostic Gates

아래는 중요하지만 아직 mandatory release blocker로 두지 않는다.

| Gate | Why diagnostic only |
|---|---|
| `python -m kifrs.eval.retrieval --k 20 --no-save` | 5 retriever full run timed out at 124s |
| `python -m kifrs.eval.retrieval --k 20 --retrievers hierarchical --no-save` | 180s timeout |
| `python -m kifrs.eval.retrieval --k 20 --retrievers reranked ... --no-save` | 180s timeout |
| external/API runners | external model/MCP/network/runtime conditions can affect determinism |

These should be split into smaller commands or long-running CI jobs before becoming blockers.

## Private / Local-Only Boundary

다음 자료는 공개 레포 gate에 직접 넣지 않는다.

- K-IFRS 기준서 원문
- parsed DB dump
- embedding dump
- `data/eval/manual/*` answer material
- 회계사 dogfood 자료
- client-private contracts, TB, workpapers, policies

Public repo에는 command, schema, metadata, synthetic fixture, aggregate metrics, generated reports만 둔다.

## Minimum Condition for Next Horizon

다음 horizon인 Authority Source Map / source ingestion으로 넘어가기 위한 최소 조건은 충족됐다.

Evidence:

- public-safe preflight passes
- focused answer gate passes
- full public pytest passes
- lexical/hybrid retrieval baseline is measurable
- retrieval miss reporting now separates retrievers
- known slow gates are explicitly diagnostic, not hidden failures

Remaining RAG backlog:

- answer gate item coverage expansion
- goldset task-type/coverage metadata or sidecar
- slow retriever benchmark split/profile
- multi-query decomposition prototype for cross-concept items
- source-aware citation/conflict/insufficient-evidence policy

이 backlog는 RAG refresh를 계속 붙잡을 이유가 아니라, multi-source 확장 중 병행할 개선 후보로 남긴다.

## Close Decision

`rag-quality-refresh` horizon can close.

Next recommended horizon:

- `authority-source-map`

Purpose:

- K-IFRS 외 정보원(KASB/FSS 질의회신, 감사기준, 법령, DART/OpenDART, client-private 자료)을 authority,
  copyright/storage, ingestion feasibility, citation policy 기준으로 catalog화한다.

