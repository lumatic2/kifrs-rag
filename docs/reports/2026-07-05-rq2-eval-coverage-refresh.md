# RQ2 Eval Coverage Refresh

> Horizon: `rag-quality-refresh`
> Step: RQ2 — Eval Coverage Refresh
> Date: 2026-07-05

## 한 줄 결론

현재 eval asset은 50문항 goldset과 176개 공개 테스트로 넓어졌지만, **품질 gate로 실제 강제되는
answer 평가 coverage는 Q019~Q023 5문항에 집중**되어 있다. retrieval-only 평가는 50문항 전체를
다루지만 timeout과 retriever별 miss 해석 문제가 있어, 기본 release gate로 쓰려면 bucket화와 split이
필요하다.

## Current Eval Surfaces

| Surface | Scope | 현재 강점 | 현재 한계 |
|---|---:|---|---|
| `data/eval/goldset.json` | 50 items | must/may cite, keywords, forbidden keywords가 있음 | task_type/source_type metadata가 없음 |
| `scripts/quality_preflight.py` | 5 bundled checks | public-safe quality bundle | answer gate는 5문항 focused |
| `scripts/eval_quality_gate.py` | configurable item subset | composite/cite/global threshold 강제 | 기본값은 Q019~Q021, preflight는 Q019~Q023 |
| `kifrs.eval.retrieval` | 50 items 가능 | retriever별 recall/MRR/nDCG 측정 | full all-retriever run timeout |
| `python -m pytest tests -q` | 176 tests | workflow/authority/user_note/demo 회귀 | retrieval quality score를 대체하지 않음 |

## Goldset Metadata Summary

Public report에는 문제 원문이나 manual answer를 복사하지 않고 metadata만 요약한다.

### Source distribution

| Source | Items |
|---|---:|
| `cpa-2` | 24 |
| `synth` | 12 |
| `scenario` | 10 |
| `textbook` | 3 |
| `cpa-1` | 1 |

### Standard distribution by item

| Standard | Items |
|---|---:|
| 1109 | 13 |
| 1116 | 10 |
| 1115 | 8 |
| 1037 | 6 |
| 1019 | 4 |
| 1002 | 2 |
| 1033 | 2 |
| 1001 | 1 |
| 1016 | 1 |
| 1032 | 1 |
| 1036 | 1 |
| 1038 | 1 |
| 1102 | 1 |
| 2119 | 1 |

### Citation shape

| must-cite count per item | Items |
|---|---:|
| 1 | 48 |
| 2 | 2 |

Interpretation:

- goldset은 1109/1116/1115 중심이지만 1037, 1019, 1001, 1002, 1036 등도 일부 포함한다.
- 대부분 단일 must-cite라서 direct retrieval score에는 좋지만, 실제 업무형 multi-evidence 답변 평가는 약하다.
- task type metadata가 없어 "이 문항이 direct lookup인지, judgement인지, disclosure인지"를 자동으로 구분하기 어렵다.

## Current Quality Gate Coverage

`quality_preflight.py`의 answer gate는 다음 focused set만 강제한다.

| Gate | Items | Standards | Source |
|---|---:|---|---|
| local-rag threshold in preflight | 5 | 1019 x4, 1037 x1 | cpa-2 |

Implication:

- 현재 preflight는 확정급여/충당부채 계열 focused smoke로는 유효하다.
- 1109 금융상품, 1115 수익, 1116 리스 workflow 질문이 answer gate에 직접 포함되어 있지 않다.
- disclosure, source pack/user note dependent answer, conflict/insufficient-evidence 질문도 gate에 없다.

## Coverage Buckets

| Bucket | Current status | Evidence | Gap |
|---|---|---|---|
| Direct paragraph lookup | covered | retrieval 50-item goldset | answer gate에는 대표성이 낮음 |
| Cross-paragraph judgement | partial | goldset must/may cite, keyword scorer | 대부분 must-cite 1개라 multi-evidence 약함 |
| Cross-standard judgement | partial | RO1 known Q039/Q048 class | 기본 gate에는 없음 |
| Workflow seed scenario | partial | workflow tests and demo tests | eval goldset과 workflow fixture가 분리됨 |
| Disclosure generation | partial | `test_1115_disclosure`, `test_1116_disclosure`, `test_1109_disclosure` | RAG answer gate에는 없음 |
| Source pack/user note dependent answer | partial | authority/user_note tests | eval goldset item으로 연결되어 있지 않음 |
| Citation conflict / insufficient evidence | missing | no explicit gate | "근거 부족" 선언 policy 필요 |
| Long-running retrieval benchmark | partial | lexical/hybrid full run works | hierarchical/reranked full run timeout |

## Recommended Gate Split

RQ4에서 gate를 손보기 전, RQ2 기준으로 다음처럼 나눠야 한다.

### Always-on public-safe gate

목적: 커밋/세션마다 빠르게 돌리는 smoke.

Candidate:

```powershell
python scripts\quality_preflight.py --format text
python -m pytest tests\test_eval_gates.py tests\test_authority.py tests\test_authority_source_pack.py tests\test_user_note_v2_runtime.py tests\test_user_notes.py tests\test_user_note_v2_migration.py -q
```

현재 상태:

- PASS
- already bundled by `quality_preflight.py`

### Focused answer gate

목적: local-rag answer composer와 scorer가 citation/keyword/global rules를 지키는지 확인.

현재:

```powershell
python scripts\eval_quality_gate.py --runner local-rag --only Q019 Q020 Q021 Q022 Q023 --min-composite 0.6 --min-cite 0.45 --format text
```

개선 필요:

- Q019~Q023 외에 1109/1115/1116 대표 문항을 추가해야 한다.
- source pack/user note dependent item을 별도 subset으로 만들어야 한다.
- conflict/insufficient evidence negative item이 필요하다.

### Retrieval benchmark gate

목적: retriever별 recall/MRR/nDCG를 본다.

현재 안정 실행:

```powershell
python -m kifrs.eval.retrieval --k 20 --retrievers lexical hybrid --no-save
```

개선 필요:

- hierarchical/reranked는 full run timeout 때문에 default gate에서 제외하거나 item subset으로 쪼갠다.
- miss 출력이 hybrid 기준으로만 보이는 오해를 줄여야 한다.
- RQ3에서 miss item을 failure bucket별로 분류한다.

### Full regression gate

목적: 공개 코드 전체 회귀.

Current:

```powershell
python -m pytest tests -q
```

현재 상태:

- 176 passed
- `.pytest_cache` permission warning only

## RQ3 Inputs

RQ3에서 바로 분류할 concrete candidates:

| Candidate | Why |
|---|---|
| Q001 | query wording / abstract standard wording mismatch candidate |
| Q004 | hybrid miss but reranked previously recovered candidate |
| Q006 | common term / paragraph discrimination candidate |
| Q008 | scope paragraph / exact identifier candidate |
| Q022 | semantic focused miss |
| Q029 | common lease term candidate |
| Q039 | cross-concept / multi-query candidate |
| Q040 | pure lexical gap / exact classification rule candidate |
| Q041 | hybrid miss but reranked previously recovered candidate |
| Q048 | cross-concept / multi-query candidate |

## RQ2 Decision

RQ2는 다음 결론으로 닫는다.

- 현재 eval asset은 존재하지만, gate coverage는 충분히 균형 잡혀 있지 않다.
- RQ3는 새 최적화 전에 위 candidate들을 failure taxonomy로 분류해야 한다.
- RQ4는 그 taxonomy를 보고 `quality_preflight.py` 또는 별도 gate split을 고쳐야 한다.

