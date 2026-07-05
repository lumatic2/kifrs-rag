# Plan: Multi-Authority Runtime Hardening

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/multi-authority-runtime-hardening.md`
> Previous gate: `docs/reports/2026-07-05-nis5-dataization-gate.md`

## 산문 요약

이번 horizon은 K-IFRS 외 source를 "데이터로 준비했다"에서 끝내지 않고, 실제 workflow runtime이 그 evidence를
권위별로 분리해 쓰게 만드는 단계다. 회계처리 판단은 K-IFRS primary evidence가 중심이고, KASB/FSS-style
metadata는 supporting interpretation, 법령은 legal boundary, DART-style 수치는 fact evidence, client-private
자료는 local-only fact로 분리한다. 산출물 목표는 review pack, statement draft, answer composer, close demo가
모두 같은 authority boundary를 따르는 것이다.

## Horizon Order

1. `multi-authority-runtime-hardening` — K-IFRS, 법령, 질의회신, 공시, private facts를 권위별로 분리해 답변에 쓴다.
2. `client-private-parser-runtime` — 계약서/TB/회계정책서 같은 로컬 private 파일 parser와 deletion/runtime gate.
3. `firm-facing-product-surface` — 회계법인에 보여줄 demo surface, operator UX, install/readiness 패키지.

## Milestone / Step Tree

### MAH1 — Runtime Evidence Boundary Audit

- [ ] MAH1.1 — Inventory runtime evidence surfaces. (verify: report lists `kifrs/runtime/*`, review packs, statement draft, answer boundary tests)
- [ ] MAH1.2 — Compare NIS handoff contract to current runtime fields. (verify: report maps NIS record types to runtime role support)
- [ ] MAH1.3 — Classify hardening gaps by surface. (verify: report has MAH2~MAH5 gap table)
- [ ] MAH1.4 — Produce MAH1 audit report. (verify: `docs/reports/2026-07-05-mah1-runtime-evidence-boundary-audit.md` exists)

### MAH2 — Runtime Evidence Contract Hardening

- [ ] MAH2.1 — Define authority role enum/helpers. (verify: `python -m pytest tests\test_runtime_authority_boundary.py -q`)
- [ ] MAH2.2 — Add source-record to runtime-evidence adapter. (verify: adapter rejects protected body-like fields)
- [ ] MAH2.3 — Preserve primary vs non-primary evidence split. (verify: tests assert primary K-IFRS evidence is separate from supporting/legal/fact/private)
- [ ] MAH2.4 — Write MAH2 contract report. (verify: `docs/reports/2026-07-05-mah2-runtime-evidence-contract.md` exists)

### MAH3 — Review Pack Authority Panel

- [ ] MAH3.1 — Define shared authority panel payload. (verify: panel tests cover 5 authority groups)
- [ ] MAH3.2 — Attach panel to 1116 review pack fixture output. (verify: `python -m pytest tests\test_1116_review_pack.py -q`)
- [ ] MAH3.3 — Attach panel to 1109 review pack fixture output. (verify: `python -m pytest tests\test_1109_review_pack.py -q`)
- [ ] MAH3.4 — Attach panel to 1115 review pack fixture output. (verify: `python -m pytest tests\test_1115_review_pack.py -q`)
- [ ] MAH3.5 — Write MAH3 report. (verify: report includes boundary text: external evidence does not replace K-IFRS primary evidence)

### MAH4 — Statement Draft and Analytics Fact Hook

- [ ] MAH4.1 — Add structured fact reference shape for statement draft. (verify: `python -m pytest tests\test_statement_draft.py -q`)
- [ ] MAH4.2 — Add structured fact hook to audit analytics fixture. (verify: focused audit analytics test passes)
- [ ] MAH4.3 — Ensure structured facts cannot become primary authority. (verify: negative test rejects primary promotion)
- [ ] MAH4.4 — Write MAH4 report. (verify: report shows synthetic fact linkage only)

### MAH5 — Authority Composer Gate and Runtime Demo

- [ ] MAH5.1 — Implement authority composer helper. (verify: `python -m pytest tests\test_answer_boundary.py -q`)
- [ ] MAH5.2 — Build runtime demo fixture with five evidence groups. (verify: demo report renders all groups)
- [ ] MAH5.3 — Implement `scripts\multi_authority_runtime_gate.py`. (verify: `python scripts\multi_authority_runtime_gate.py --format text`)
- [ ] MAH5.4 — Run carried regressions from NIS/RR. (verify: NIS gate, source record validator, chunking policy, default guard, quality preflight)
- [ ] MAH5.5 — Close horizon. (verify: `docs/reports/2026-07-05-multi-authority-runtime-hardening-close-report.md` exists)

## 결정 로그

- 결정: K-IFRS paragraph evidence는 primary evidence로 유지한다.
- 결정: KASB/FSS metadata는 supporting interpretation이고 primary evidence를 대체하지 않는다.
- 결정: law locator는 legal boundary로 표시한다.
- 결정: DART/OpenDART-style structured fact는 fact evidence로만 표시한다.
- 결정: client-private source는 local-only placeholder로만 runtime boundary를 잡고, 실제 private file parsing은 다음 horizon으로 넘긴다.
- 결정: live external connector/API 호출, real client file parsing, default retriever promotion은 이 horizon 범위 밖이다.
- 사용자 소유 결정: 현재 없음.

## 중단점

- protected body, raw filing payload, copied law/source material, real client content가 필요해지면 중단하고 placeholder/policy로 남긴다.
- source authority가 primary K-IFRS evidence를 대체하는 설계가 나오면 중단하고 boundary를 재검토한다.
- RAG reliability 또는 non-IFRS dataization regression이 실패하면 runtime 확장보다 회귀 원인을 먼저 고친다.

## Regression Commands Carried Forward

- `python scripts\non_ifrs_dataization_gate.py --format text`
- `python scripts\validate_non_ifrs_source_records.py --format text`
- `python scripts\validate_non_ifrs_chunking_policy.py --format text`
- `python scripts\default_retriever_guard.py --format text`
- `python scripts\quality_preflight.py --format text`
- `python scripts\rag_quality_final_gate.py --format text`

## Planning Gate

```yaml
planning_gate:
  team_validation_mode: manual-pass
  spec_delta: "Open multi-authority-runtime-hardening horizon and decompose MAH1~MAH5 into runtime hardening steps."
  perspectives:
    product: "Turns source dataization into visible workflow evidence separation, which is closer to firm-facing review-pack value."
    architecture: "Introduces one runtime authority boundary instead of ad hoc evidence sections per workflow."
    security: "No source body, raw filing payload, private client content, external access material, or embedding file enters public repo."
    qa: "Each milestone has a focused test/report plus final gate and carried RAG/NIS regressions."
    skeptic: "Risk is overbuilding display plumbing before real private data; mitigated by using public-safe fixtures and preserving next horizon for private parser runtime."
  dod:
    - "MAH1~MAH5 reports/gates exist and pass."
    - "Runtime outputs keep primary K-IFRS evidence separate from supporting/legal/fact/private evidence."
```
