# BACKLOG

> Compressed milestone archive. ROADMAP.md is capped at 150 lines.

## Completed

### 2026-07-05 — Compressed closed horizon archive
- Completed: 2026-07-04~2026-07-05
- Result: ROADMAP 150-line cap 유지를 위해 오래된 closed horizon 상세를 압축 보관. 포함: `workflow-automation`, `practice-map`, `automation-expansion`, `firm-service-map`, F-ACC sequence(`f-acc-review-pack`, `f-acc-1109-review-pack`, `f-acc-1115-revenue-engine`, `f-acc-disclosure-generalization`, `f-acc-1109-hardening`, `f-acc-financial-statement-draft`), `f-audit-analytical-procedures`, `product-packaging-poc`, `rag-quality-refresh`, `authority-source-map`, `multi-source-ingestion-pipeline`, `multi-authority-runtime-integration`.
- Evidence: 각 horizon 원문은 `docs/horizons/`에 유지. 주요 산출물은 `docs/practice-map/`, `kifrs/workflows/`, `kifrs/runtime/`, `kifrs/ingestion/`, `docs/authority/`, `docs/ingestion/`, `docs/reports/demo-poc/`.
- Verification: 각 horizon별 close report와 ROADMAP 이전 이력 기준.

### 2026-07-04 — PM3: 자동화 가능성 매핑 + 다음 대상 추천
- Completed: 2026-07-04
- Result: 33 task 전수 판정(가능 6/조건부 5/불가 5/미실험-유망 6/미실험-보류 11 — 로컬 검증성 rubric 포함), 유망 후보 5개 심층 분석. 추천: 자동화 확장 horizon에 B3-확장(1116 엔진 이식, 먼저) + B5(주석 초안, 다음). D3(비상장 주식평가)은 tax-agent 이관 권고, A5·E2 보류. practice-map horizon 조건부 close(PM2 현업검증 이월).
- Evidence: `docs/practice-map/taxonomy.md`; `docs/practice-map/candidates.md`; `docs/horizons/practice-map.md`
- Verification: `python -m pytest tests/ -q` 92/92 (문서 작업, 비퇴행).

### 2026-07-04 — PM1: 회계사 업무 taxonomy 초안
- Completed: 2026-07-04
- Result: 공개자료 20건 + 사용자 1차 관찰 기반 taxonomy v0 — 5대분류(감사·인증/결산·F/S지원/세무(tax-agent 경계)/재무자문/기타인증) 33 task, 각 task에 빈도·판단강도·입출력·현AI활용 4메타. 핵심 발견: 법인 AI는 리서치(A8)·문서 대량처리(A6)에 집중, 판단 본질 task(B3 회계처리판단·B5 주석·A10 감사보고서)는 공백 — Objective 차별점과 일치. 커버리지 축 0차 측정 2/33(6%): A8=가능(dogfood 86%), B3=조건부(1109 엔진 6/10).
- Evidence: `docs/practice-map/taxonomy.md`; `docs/practice-map/sources.md`; `docs/plans/2026-07-04-pm1-practice-taxonomy.md`
- Verification: `python -m pytest tests/ -q` 92/92 (문서 작업, 비퇴행).

### 2026-07-03 — RO1: 잔여 검색 miss 진단
- Completed: 2026-07-03
- Result: M4(2026-06-27) 이후 잔여 miss 9건 재검증. 얕은 랭킹 2건(Q004/Q041)은 `search_reranked`가 이미 top-20 안(순위 6, 13)에 넣고 있었다 — 코드 변경 불필요, eval 스크립트의 hybrid 전용 miss 출력이 오독을 유발했을 뿐. 깊은 랭킹 7건은 3개 원인 카테고리(A: 순수 어휘 부재, B: 일반어 매칭 판별력 부족, C: 크로스 개념/표준 쏠림)로 분류, RO2는 카테고리 C(2건, 멀티 쿼리 분해)만 좁게 스코프하기로 권고.
- Evidence: `docs/reports/2026-07-03-ro1-deep-miss-diagnosis.md`; `docs/horizons/rag-optimization-resume.md`; `docs/plans/2026-07-03-ro1-residual-miss-diagnosis.md`
- Verification: `python -m pytest tests/ -q` 92/92 통과(비퇴행, 소스 변경 없음).

### 2026-07-03 — RGA1: 런타임 citation 존재 검증
- Completed: 2026-07-03
- Result: `kifrs/workflows/kifrs1109/`의 결정 엔진 인용을 `kifrs.store` 직접 import로 런타임 존재 검증, 불일치 시 `NeedsHumanReview` 에스컬레이션. 의미적 일치 검증(reason 문구가 조항 내용과 부합하는지)은 keyword overlap·cosine 유사도·cross-encoder 리랭커 실측 결과 정답/오답 구분 불가로 RGA1 범위에서 제외 — 별도 후속 필요.
- Evidence: `kifrs/workflows/kifrs1109/grounding.py`; `tests/test_workflow_1109_grounding.py`; `docs/plans/2026-07-03-rga1-runtime-citation-grounding.md`; `docs/reports/2026-07-03-wa1-completion-rate.md`
- Verification: `python -m pytest tests/ -q` 92/92 통과. `quality_preflight.py --format text` ok. 완료율 6/10 유지(자동화 6건 전부 grounding 통과).

### 2026-07-03 — WA1: 1109 파일럿 결정 엔진 + 완료율 측정
- Completed: 2026-07-03
- Result: 구조화 거래 입력 → SPPI/사업모형 분류 → 최초인식 분개 → 상각표 포함 후속측정 → 검토메모까지 코드로 실행, 기존 10개 1109 시나리오를 회귀 fixture로 재현해 "시나리오 완료율" 첫 측정값 산출(6/10=60%).
- Evidence: `kifrs/workflows/kifrs1109/`; `tests/test_workflow_1109.py`; `tests/test_workflow_1109_regression.py`; `docs/reports/2026-07-03-wa1-completion-rate.md`
- Verification: `python -m pytest tests/test_workflow_1109_regression.py -q` 통과, 완료율 6/10 기록.
- Follow-up: RAG 엔진↔에이전트 통합 horizon(RGA1)으로 이어짐 — `docs/horizons/rag-agent-integration.md`. WA2/WA3는 workflow-automation horizon에 paused로 남음.

### 2026-07-03 — Engine Hardening EH1: test safety net + refactor + MCP consolidation
- Completed: 2026-07-03
- Result: 5개 changeset(CS-1~CS-5)으로 검색 엔진 하드닝 완료 — mcp_server.py/embed.py 테스트 안전망, search_reranked N+1 수정 + 임베딩/centroid 캐싱, mcp_server dual-backend dedup + ToolError 구조화 에러 + 시작 시 DB 체크, search tool 5종→1종(`search(mode=...)`) 통합 + `/accounting` SKILL.md 동기화, `TERM_BRIDGE` 하드코딩→`user_note_v2` DB 이관.
- Evidence: `changesets/20260703-engine-test-safety-net/README.md`; `changesets/20260703-engine-perf-refactor/README.md`; `changesets/20260703-mcp-server-dedup-errors/README.md`; `changesets/20260703-mcp-search-tool-consolidation/README.md`; `changesets/20260703-term-bridge-user-note-migration/README.md`
- Verification: `python -m pytest tests/ -q` 46개 통과. `quality_preflight.py --format text` ok. `engine_quality_expanded_smoke.py --format text` ok. recall@5/@10/@20/MRR 실측 비퇴행 확인(hybrid/hierarchical/reranked).
- Follow-up: Workflow Automation horizon으로 이어짐 — `docs/horizons/workflow-automation.md`.

### 2026-06-30 — Engine Quality Ops EQ5: quality preflight CI
- Completed: 2026-06-30
- Result: local-rag threshold gate, focused pytest, authority registry/source-pack validators, `user_note_v2` audit를 하나의 public-safe preflight 명령으로 묶고 GitHub Actions workflow 템플릿이 같은 명령을 실행하도록 문서화.
- Evidence: `docs/plans/2026-06-30-quality-preflight-ci.md`; `changesets/20260630-quality-preflight-ci/README.md`; `scripts/quality_preflight.py`; `docs/ci/quality.yml`; `tests/test_quality_preflight.py`; `README.md`
- Verification: targeted pytest 8개 통과. expanded focused pytest 22개 통과. `python scripts/quality_preflight.py --format text` -> ok, `public_safe=True`, `protected_assets_required=False`. `engine_quality_expanded_smoke.py --format text` ok. `compileall kifrs scripts` 통과.
- Follow-up: Engine Quality Ops 현재 scope 완료. 다음은 새 horizon 또는 Phase 4 scenario expansion 여부 결정.

### 2026-06-30 — Engine Quality Ops EQ3: authority source pack rules
- Completed: 2026-06-30
- Result: authority source category를 문서/링크 단위 metadata source pack으로 확장. `source_pack_rules.md`로 primary/supporting/boundary/convention 사용 경계를 정하고, `source_pack.json` 6개 item을 metadata/link-only로 추가. validator는 source id, authority type, allowed use, locator, keywords, body-field 금지를 검증한다.
- Evidence: `docs/plans/2026-06-30-authority-source-pack-rules.md`; `changesets/20260630-authority-source-pack-rules/README.md`; `docs/authority/source_pack_rules.md`; `docs/authority/source_pack.json`; `scripts/validate_authority_source_pack.py`; `tests/test_authority_source_pack.py`
- Verification: authority focused pytest 8개 통과. expanded focused pytest 18개 통과. `validate_authority_sources.py` ok, `validate_authority_source_pack.py` ok(total 6). `authority_index_smoke.py --query "금융감독원 질의회신 수익"` FSS hit. `search_source_pack("금융감독원 질의회신 수익")` returns `fss-accounting-inquiry-index`. `engine_quality_expanded_smoke.py --format text` ok. `compileall kifrs scripts` 통과.
- Follow-up: EQ5 local-rag threshold CI hook만 남음.

### 2026-06-30 — Engine Quality Ops EQ4: user_note v2 runtime layer
- Completed: 2026-06-30
- Result: `user_note_v2`를 projection에서 runtime 우선 레이어로 승격. 신규 seed/write는 typed v2 row를 쓰고 legacy mirror를 유지하며, query expansion과 `get_user_notes()`는 v2 active row를 우선 읽고 v2가 비어 있으면 legacy `user_note`로 fallback한다.
- Evidence: `docs/plans/2026-06-30-user-note-v2-runtime.md`; `changesets/20260630-user-note-v2-runtime/README.md`; `kifrs/store.py`; `kifrs/user_notes.py`; `scripts/seed_user_notes.py`; `scripts/audit_user_notes.py`; `tests/test_user_note_v2_runtime.py`
- Verification: focused pytest 8개 통과, expanded focused pytest 16개 통과. `seed_user_notes.py --apply` idempotent(existing 13, new 0). `audit_user_notes.py --source v2 --format json` 13 rows `ok=true`; legacy audit도 13 rows `ok=true`. `engine_quality_expanded_smoke.py --format text`와 기존 `engine_quality_smoke.py --format text` 모두 `ok: True`. `compileall kifrs scripts` 통과.
- Follow-up: EQ3 source pack 실제 수집 전략 또는 EQ5 local-rag threshold CI hook 중 하나만 active로 승격.

### 2026-06-30 — Engine Quality Ops EQ2: expanded quality loop
- Completed: 2026-06-30
- Result: EQ1의 세 축을 운영 가능한 다음 단계로 확대. `local-rag` 자동 채점에 threshold gate를 추가하고, 외부 권위 source pack을 6개 metadata source로 확장했으며, 기존 `user_note`를 건드리지 않는 additive `user_note_v2` projection migration을 구현.
- Evidence: `docs/plans/2026-06-30-engine-quality-loop-expanded.md`; `changesets/20260630-auto-grading-expanded/`; `changesets/20260630-authority-source-pack/`; `changesets/20260630-user-note-schema-v2/`; `scripts/eval_quality_gate.py`; `scripts/validate_authority_sources.py`; `scripts/migrate_user_notes_v2.py`; `scripts/engine_quality_expanded_smoke.py`
- Verification: focused pytest 13개 통과. Q019~Q023 gate mean composite `0.921`, mean cite `0.763`, global rules `1.000`, failing items `0`. authority registry 6개 source validate 통과. `금융감독원 질의회신 수익` query에서 FSS source hit. `user_note_v2` migration apply 13건 insert 후 재실행 dry-run planned 0. expanded smoke `ok: True`. `compileall kifrs scripts` 통과.
- Follow-up: EQ3 source pack 실제 수집 전략, EQ4 user_note v2 write path 전환, EQ5 local-rag threshold CI hook 중 다음 active 선택.

### 2026-06-30 — Engine Quality Ops EQ1: RAG 품질 운영 루프
- Completed: 2026-06-30
- Result: Phase 4 dogfood 이후 남은 세 축을 tooling changeset으로 구현. `user_note` parser/audit CLI, no-network `local-rag` 자동 채점 runner, metadata-only external authority registry, integrated smoke 추가.
- Evidence: `docs/horizons/engine-quality-ops.md`; `docs/plans/2026-06-30-engine-quality-ops.md`; `changesets/20260630-user-note-quality/`; `changesets/20260630-auto-grading/`; `changesets/20260630-authority-index/`; `scripts/engine_quality_smoke.py`
- Verification: focused pytest 18개 통과. `audit_user_notes.py` 13 rows ok. `local-rag` Q019~Q021 composite 0.783. `authority_index_smoke.py` 상법 자본거래 query hit. `engine_quality_smoke.py --format text` ok. `compileall kifrs scripts` 통과(기존 validate_parse warning 1건).
- Follow-up: EQ2 자동 채점 확대, EQ3 권위 source pack, EQ4 user_note schema migration 중 다음 active 선택.

### 2026-06-30 — Phase 4 콘텐츠 축 P4C5: 1019 확정급여 도메인 승격
- Completed: 2026-06-30
- Result: q06을 1019 확정급여와 1037 구조조정충당부채 workflow로 승격. EB-01은 정산·제도개정·재측정·자산인식상한, EB-02는 구조조정충당부채와 해고급여 해석 분기를 다룸. 검색 전 확장이 아니라 답변 작성 단계에서 `exam_convention`/`interpretation_note`를 조회하도록 `get_user_notes` helper와 MCP tool 추가.
- Evidence: `docs/plans/2026-06-30-p4c5-employee-benefits-entry.md`; `data/scenarios/1019_employee_benefits/WORKFLOW.md`; `data/scenarios/1019_employee_benefits/EB-01_defined_benefit_settlement_amendment/`; `EB-02_restructuring_termination_benefits/`; `kifrs/store.py`; `kifrs/mcp_server.py`
- Verification: 1019/1037 citation 14개 DB/PDF 검증 완료. EB-01/EB-02 각 scenario 필수 파일 3/3 존재 확인. `get_user_notes` smoke에서 `중간 정산 순이자`, `자산인식상한 적용 시점`, `해고급여 vs 구조조정 충당부채`가 각각 q06 user_note를 반환. `python -m compileall kifrs/store.py kifrs/mcp_server.py scripts/seed_user_notes.py` 통과.
- Follow-up: Phase 4 콘텐츠 후보는 P4C1~P4C5로 일단 닫힘. 다음은 새 engine horizon 결정.

### 2026-06-30 — Phase 4 콘텐츠 축 P4C4: 1113 공정가치 도메인 진입 설계
- Completed: 2026-06-30
- Result: 1113 공정가치 도메인의 P4C4 범위를 기준서 판단 중심으로 고정. DCF 엔진·옵션모델·외부 시장데이터 수집은 제외하고, 공정가치 정의/가치평가기법/투입변수 관측가능성/서열체계/공시 체크로 workflow를 구성. 수준 1 상장주식, 수준 2 회사채, 수준 3 비상장 지분 seed scenario 3개 작성. 종가/수익률 곡선/DCF term_bridge 3건을 SQLite `user_note` seed로 승격.
- Evidence: `docs/plans/2026-06-30-p4c4-fair-value-entry.md`; `data/scenarios/1113_fair_value/WORKFLOW.md`; `data/scenarios/1113_fair_value/FV-01_level1_listed_equity/`; `FV-02_level2_corporate_bond/`; `FV-03_level3_private_equity/`; `data/scenarios/1113_fair_value/user_note_candidates.md`
- Verification: P4C4 citation map 14개 DB/PDF 검증 완료. FV-01~FV-03 scenario citations 11개 고유 문단 DB/PDF 검증 완료. 각 scenario 폴더에 `transaction.md`, `retrieval_trace.md`, `review_memo.md` 3/3 존재 확인. user_note dry-run idempotency `existing rows: 13`, `new rows: 0`; 1113 FTS top10 smoke에서 수준 1/2/3 target 문단 hit.
- Follow-up: 1019 확정급여(q06)를 다음 실무 scenario workflow로 전환하거나, 새 engine horizon을 정의.

### 2026-06-30 — Phase 4 콘텐츠 축 P4C3: user_note 운영 시작
- Completed: 2026-06-30
- Result: q05/q06/q07/P4C2에서 나온 failure mode를 user_note seed 10건으로 승격. 이후 P4C4 1113 seed 3건을 추가해 총 13건. `scripts/seed_user_notes.py` idempotent seeder 추가, SQLite `user_note`에 insert, `kifrs/store.py` 검색 전 query expansion이 `type=term_bridge`와 `type=retriever_policy` user_note를 읽도록 연결.
- Evidence: `data/user_notes/2026-06-30-p4c3-seed-preview.md`; `scripts/seed_user_notes.py`; `kifrs/store.py`
- Verification: seed dry-run `existing rows: 10, new rows: 0`; query expansion smoke for `갱신선택권`, `외상거래할인권`, `공매도`; seed anchor citations 10개 DB/PDF 검증.
- Follow-up: P4C4 1113 공정가치 도메인 진입 설계.

### 2026-06-30 — Phase 4 콘텐츠 축 P4C2: 1116 리스 잔여 closeout
- Completed: 2026-06-30
- Result: 1116 리스 워크플로 5/10 → 10/10 완성. 신규 산출: 시나리오 3 단기·소액 면제, 시나리오 4 금융리스 제공자 금융→운용 변경, 시나리오 6 금융→금융 정기리스료 변경, 시나리오 7 리스기간 재평가, 시나리오 8 매수선택권 행사 거의 확실. 각 시나리오별 `transaction.md`, `workflow_log.md`, `entries.md`, `review_memo.md` 작성.
- Evidence: `data/scenarios/1116_lease/WORKFLOW.md`; `data/scenarios/1116_lease/scenario_03_short_low_value_exemption/`; `scenario_04_lessor_finance_to_operating/`; `scenario_06_lessor_finance_to_finance_payment_change/`; `scenario_07_lessee_term_reassessment/`; `scenario_08_lessee_purchase_option_reasonably_certain/`
- Verification: cited paragraphs checked against DB/PDF for scenario 3(9), 4(10), 6(7), 7(8), 8(5) with 0 missing and 0 mismatch.
- Follow-up: P4C3 user_note 운영 시작. q07 term_bridge/exam_convention 후보와 1116에서 나온 interpretation notes를 seed 후보로 정리.

### 2026-06-30 — Phase 4 콘텐츠 축 P4C1: 1115 수익 q07 RAG eval case
- Completed: 2026-06-30
- Result: q07을 clean input + retrieval trace + 본인 풀이 + 채점 + user_note 후보까지 닫음. 직관 5/7, 해석 인정 6/7, 인용 정확도 13/13. q07-2 할인권, q07-3 유의적 금융요소, q07-4 콜옵션 재매입약정은 pass. q07-1 갱신선택권은 citation은 맞았지만 계약부채 vs 잔여 수행의무 표시와 진행률 반올림 관습에서 partial.
- Evidence: `data/dogfood/cpa2/q/q07.md`; `data/eval/manual/q07_1115_revenue_trace.md`; `data/scenarios/1115_revenue/WORKFLOW.md`; `data/scenarios/1115_revenue/user_note_candidates.md`
- Follow-up: P4C2 1116 리스 잔여 closeout. q07 term_bridge/exam_convention 후보는 P4C3 user_note 운영 시작 때 seed 우선순위로 반영.

### 2026-06 — 검색 파이프라인 고도화 (Current Horizon)
- M1 — 측정 기반 구축 (Retrieval Eval Harness)
  - Completed: 2026-06-27
  - Result: retrieval-only evaluator(recall@k·MRR·nDCG, API 不要)가 goldset을 lexical/semantic/hybrid로 돌려 baseline 산출. goldset 8→50 확장. Baseline(50문항,K=20): semantic=hybrid recall@5=0.557/@10=0.720/@20=0.847, MRR=0.555, nDCG@10=0.538
  - Evidence: `kifrs/eval/retrieval.py` + `data/eval/results/retrieval_20260627_154807.json` + `data/eval/goldset.json`(50문항, must_cite 50/50 DB 검증)
  - Plan: `docs/plans/2026-06-27-retrieval-eval-harness.md`

- M3 — Query 가공 / 용어 브리지 (천장 상승)
  - Completed: 2026-06-27
  - Result: hybrid recall@20 0.847 → M3a 0.877(lexical 0→0.693 부활) → M3b 0.907(+6.0pp 누적). M3b 동의어로 Q005·Q022 hit 전환. reranked(M3+M2) recall@5=0.640/MRR=0.612
  - Evidence: data/eval/results/retrieval_20260627_165615.json
  - Plan: `docs/plans/2026-06-27-query-expansion.md`

- M2 — Cross-encoder 리랭킹 프로덕션 wiring
  - Completed: 2026-06-27
  - Result: search_reranked MCP tool + 리랭커 warmup(데몬 스레드) + /accounting SKILL.md 정밀 인용 1순위. GPU per-query 0.44s로 인터랙티브 viable
  - Evidence: kifrs/mcp_server.py
  - Plan: `docs/plans/2026-06-27-rerank-production-wiring.md`

- M4 — Hierarchical retrieval + evidence curation
  - Completed: 2026-06-27
  - Result: 계층 검색(섹션 centroid) hybrid 전 지표 비퇴행/개선. recall@10 0.763→0.827. search_hierarchical MCP tool 노출. evidence curation/후보 풀 교체는 측정상 가치 낮아 보류
  - Evidence: `data/eval/results/retrieval_20260627_225318.json`
  - Plan: `docs/plans/2026-06-27-hierarchical-retrieval.md`

- M5 — 평가 리포트 + 아키텍처 글
  - Completed: 2026-06-28
  - Result: "측정이 거절한 두 기능: 검색 엔진을 평가 하네스로 키운 기록" 발행. M1~M4 누적 before/after 메트릭과 하네스가 폐기한 기능 판단을 공개 가능한 범위에서 정리. 기준서 원문·문단·기출은 미포함
  - Evidence: `https://askewly.com/blog/eval-harness-rejects-features`
  - Plan: option track from ROADMAP M5

---

## Phase 이력 (Phase 1~4, 콘텐츠·시나리오 축 — 2026-04~05 압축)

### Phase 1 — PoC ✅ (2026-04-14)
인프라 구축. tax-agent 패턴 재사용 + KASB 일괄 다운로더 + 파서 + SQLite + FastMCP.
- 100 기준서(K-IFRS 63 + 일반기업회계기준 36 + special 1) / **8,328 paragraphs**(2026-04-24 letter-suffix 616건 복구 포함)
- SQLite DB 29MB + paragraph_fts(trigram + LIKE fallback). FastMCP tools 7종. /accounting 스킬 + dogfood 10건 통과. goldset 8문항(Q001~Q008)

### Phase 2 — 시험 수준 검증 ✅ 졸업 (2026-04-28)
목표: 회계사 2차 기출 정확도 80%+. **누적 86%(cpa2 5 + textbook 21)로 졸업**.
- Dogfood R1(2026-04-27): cpa2 5문항 풀이+직관 채점. 검색 실패 5건 식별
- 검색 품질 개선: bge-m3 임베딩(1024d, 8,328 인덱싱) + hybrid RRF(search_semantic/search_hybrid). 검색 실패 5건 중 3 완벽/1 부분/1 본문부재(공매도)
- 답변 포맷 유연화: SKILL.md §3 `(고정)`→`가치는 고정, 형태는 질문에 맞춘다`. 5 질문유형 매핑표
- Dogfood R2: hybrid 재풀이 → 검색 매칭 60%→80%. R3 mini: 계산형/서술형 두 형태 새 가이드 검증
- Textbook dogfood: 1102 6/6 + 1033 9/9 + 1116 6/6 = **21/21 100%**(모범답안 포함 정량)
- Baseline A/B: ch14 Engine 9/9 vs Naive Claude 5/9(+44%p). 엔진 우위 = 매 단계 본문 검증
- cpa2 정량 채점: q01 71%/q02 70%/q03 82%/q04 100%/q05 50% = 평균 75%(해석 인정 85%). q04 상법 영역도 본인 지식 정확. q05 IFRIC19[2119] 해석 약점

### Phase 3 — 실무 시나리오(1109 금융상품 분류·측정) ✅ 10/10 (2026-04-28)
신규 거래 입력 → 1109 분류 워크플로 자동 산출. `data/scenarios/1109_classification/`.
- WORKFLOW.md: §1 SPPI 결정트리 → §2 사업모형 4축 → §3 분류 매트릭스 → §4·5 분개 → §6 검토메모 7섹션
- 기본 분류 5건: AC / FVOCI(부채) / SPPI Fail→FVPL / FVOCI(자본·지분) / IFRIC19[2119] 자기지분 부채소멸
- 경계 케이스 5건: 변동금리 SPPI nuance[B4.1.9C] / 전환사채 발행자[1032-31]vs보유자[1109] / 재분류 6패턴[4.4.1] / FVPL 지정[4.1.5] / 외화채권 1109+1021
- 학습: 같은 SPPI Pass라도 사업모형이 분류 결정 / FVOCI 부채vs자본 처분 OCI 차이 / "측정 불가=대체 공정가치"

### Phase 4 — 시나리오 확장 + 누적 (2026-04-29~05-02, 진행 중 → 현재 콘텐츠 축)
- 1116 리스 WORKFLOW.md + template. 시나리오 1·2·5·9·10 완성(5/10):
  - 시1 단순 사무실(부채/자산 3,545,950) / 시2 복구의무+선급(자산 4,107,300, 1116+1037)
  - 시5 운용→금융 변경(textbook ch15 물음1, 6/6) / 시9 추가+축소 동시(q08 물음1, 분리트랙 정정, 모범답안 3/3) / 시10 기간연장(q08 물음2, 2/2)
- cpa2 q06(1019+1037) 풀이+채점: 직관 1/5 + 해석 인정 4/5 ≈ 80%(2026-05-02)
- 잔여 1116 시나리오: 3(단기·저가 면제) / 6(금융→금융) / 7(기간 재평가) / 8(매수선택권)
- 다른 도메인 미착수: 1115 수익 / 1113 공정가치(KICPA 부담 1위 27.08%) / user_note 활성화

### 2026-07
- EQ1 - EQ1
  - Completed: 2026-07-03
  - Result: 자동 채점, 외부 권위 인덱스, user_note 운영 품질을 각각 최소 로컬 실행 가능한 tooling surface로 구현하고, 세 축을 함께 확인하는 integrated smoke를 남긴다.
  - Evidence: `changesets/20260630-user-note-quality/README.md`; `changesets/20260630-auto-grading/README.md`; `changesets/20260630-authority-index/README.md`; `scripts/engine_quality_smoke.py`

- EQ2 - EQ2
  - Completed: 2026-07-03
  - Result: 자동 채점 범위를 확대하고 threshold gate를 추가하며, 외부 권위 source pack을 metadata-only로 확장하고, user_note v2 schema migration을 backward-compatible하게 설계·검증한다.
  - Evidence: `changesets/20260630-auto-grading-expanded/README.md`; `changesets/20260630-authority-source-pack/README.md`; `changesets/20260630-user-note-schema-v2/README.md`; `scripts/engine_quality_expanded_smoke.py`

- EQ4 - EQ4
  - Completed: 2026-07-03
  - Result: user_note_v2 runtime write/read path completed with legacy fallback
  - Evidence: `changesets/20260630-user-note-v2-runtime/README.md`; `docs/plans/2026-06-30-user-note-v2-runtime.md`; `scripts/seed_user_notes.py`; `scripts/audit_user_notes.py`

- EQ3 - EQ3
  - Completed: 2026-07-03
  - Result: authority source pack rules completed with metadata-only validator
  - Evidence: `changesets/20260630-authority-source-pack-rules/README.md`; `docs/plans/2026-06-30-authority-source-pack-rules.md`; `docs/authority/source_pack_rules.md`; `docs/authority/source_pack.json`; `scripts/validate_authority_source_pack.py`

- EQ5 — local-rag threshold CI hook
  - Completed: 2026-06-30
  - Result: public-safe quality preflight and CI hook completed
  - Evidence: `changesets/20260630-quality-preflight-ci/README.md`; `scripts/quality_preflight.py`; `docs/ci/quality.yml`

- P4C1~P4C5 — Phase 4 콘텐츠 dogfood 마무리 (1115 수익, 1116 리스 closeout, user_note 운영 시작, 1113 공정가치 entry, 1019 확정급여 승격)
  - Completed: 2026-06-30
  - Result: 1115 q07 RAG eval trace, 1116 리스 10/10 완성, user_note 13건 seed + query expansion 연결, 1113/1019 도메인 workflow 진입
  - Evidence: `data/scenarios/1115_revenue/`; `data/scenarios/1116_lease/`; `data/scenarios/1113_fair_value/`; `data/scenarios/1019_employee_benefits/`; `scripts/seed_user_notes.py`
