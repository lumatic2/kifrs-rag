# kifrs-rag ROADMAP

> 마지막 업데이트: 2026-07-05 (WCD2 완료, WCD3 active)
> "회계사 업무를 AI로 어디까지 자동화할 수 있는가"에 실증으로 답하는 로컬 도구킷 프로덕트 (`docs/OBJECTIVE.md`). 공개 레포에는 코드·아키텍처·평가 하네스만 두고, 기준서 원문·파싱 DB·임베딩·dogfood 자료는 로컬에서만 보관.
> 완료 이력(Phase 1~4 + M1~M5) → **`BACKLOG.md`** · 다음 세션 진입점 → **`CLAUDE.local.md`**

## 배경 / 포지셔닝

K-IFRS 기준서를 프로그램적으로 조회할 공식 API/MCP 부재. 빅4 사내 AI는 비공개, 기준서 원문·파싱 텍스트·DB·임베딩·dogfood 자료는 KASB·IFRS Foundation 저작권 장벽 때문에 공개하지 않는다.
- 공개 범위: 코드, 아키텍처 설명, 평가 하네스, 메트릭, 운영 문서
- 비공개 범위: 기준서 PDF, 파싱 텍스트, SQLite DB, 임베딩, 회계사 기출 dogfood 자료
- `tax-agent` 패턴 재사용 → 신규 개발 비용 최소화

## 야망 (docs/OBJECTIVE.md 동기화 — 2026-07-04 프로덕트 지향 재정의)

"회계사 업무를 AI로 어디까지 자동화할 수 있는가"에 실증으로 답하고, 그 답을 **회계법인에 소개 가능한 로컬 도구킷 프로덕트**로 만든다. 성공 모습: 법인 소개/PoC 성사. 축: ① 업무 지도 커버리지(신설) ② 시나리오 완료율(도메인별). 세무는 tax-agent 분리.

| 단계 | 목표 | 상태 |
|---|---|---|
| **Phase 1** | 인프라 — 100 기준서 DB + MCP + /accounting | ✅ (2026-04-14) |
| **Phase 2** | 시험 수준 — 2차 기출 정확 인용 + 적용 해설 | ✅ 졸업 누적 86% (2026-04-28) |
| **Phase 3** | 실무 시나리오 1개 — 금융상품 분류·측정(1109) | ✅ 10/10 (2026-04-28) |
| **Phase 4 (현재)** | 시나리오 확장 + 누적 (리스·수익·공정가치·확정급여 + user_note) | 진행 중 (P4C1~P4C5 완료) |

> 상세 이력은 `BACKLOG.md` "Phase 이력" 참조.

---

## Remaining Horizon Order

1. `rag-reliability-revalidation` — 완료. K-IFRS RAG 품질 재검증과 default promotion 기준.
2. `non-ifrs-source-dataization` — 완료. KASB/FSS/법령/DART/client-private source lane을 실제 RAG 데이터화 단위로 확장.
3. `multi-authority-runtime-hardening` — 완료. K-IFRS, 법령, 질의회신, 공시, private facts를 권위별로 분리해 답변에 쓴다.
4. `client-private-parser-runtime` — 완료. 계약서/TB/회계정책서 같은 로컬 private 파일 parser와 deletion/runtime gate.
5. `firm-facing-product-surface` — 완료. 회계법인에 보여줄 demo surface, operator UX, install/readiness 패키지.
6. `product-trust-and-quality-evidence` — 완료. 데모 출력의 품질·근거·실패경계·retriever 승격 판단을 제품 표면에 붙인다.
7. `real-local-parser-prototype` — 완료. synthetic/parser contract를 실제 로컬 parser prototype에 가깝게 확장했다.
8. `source-body-ingestion-controlled-lane` — 완료. 권한·정책이 있는 비IFRS source-body lane 1개를 controlled RAG 단위로 구현했다.
9. `workflow-coverage-expansion` — 완료. firm-service map 기준으로 1037 provisions workflow를 conditional decision-prep adapter로 확장했다.
10. `runtime-retriever-promotion-gate` — 완료. opt-in repair retriever default 승격은 `defer`로 닫고 rollback evidence를 붙였다.
11. `operator-experience-hardening` — 완료. operator command discovery, run doctor, report manifest, recovery path를 다듬었다.

제품 약점 기준 재정렬: `docs/plans/2026-07-05-product-weakness-horizon-candidates.md`
Objective gap horizon queue: `docs/reports/2026-07-05-objective-gap-horizon-candidates.md`

## Current Horizon — workflow-coverage-depth-expansion

<!-- harness:goal id="workflow-coverage-depth-expansion" status="active" -->
`docs/horizons/workflow-coverage-depth-expansion.md` — firm-service map 대비 자동화 workflow 표본을 더 깊고 넓게 확장한다.

순서: WCD1 service-line coverage rerank ✅ → WCD2 workflow sample contract pack ✅ → WCD3 minimal adapter expansion → WCD4 coverage depth metric update → WCD5 close/handoff.

## Active Milestones

<!-- harness:milestone id="WCD1" status="completed" priority="P0" -->
### WCD1 — Service-Line Coverage Rerank
DoD: firm-service map gaps are ranked by automation value, evidence availability, implementation cost, and public-safety boundary.
Evidence: `docs/reports/2026-07-05-wcd1-service-line-coverage-rerank.md`
Gap: Closed by WCD1 service-line rerank script/tests/report.
Status: [x]

<!-- harness:milestone id="WCD2" status="completed" priority="P0" -->
### WCD2 — Workflow Sample Contract Pack
DoD: selected workflow samples have input facts, authority needs, output surface, review boundary, and failure states.
Evidence: `docs/reports/2026-07-05-wcd2-workflow-sample-contract-pack.md`
Gap: Closed by WCD2 workflow sample contract pack script/tests/report.
Status: [x]

<!-- harness:milestone id="WCD3" status="active" priority="P0" -->
### WCD3 — Minimal Adapter Expansion
DoD: at least one additional workflow produces decision-prep metadata without protected payload exposure.
Evidence: `docs/reports/2026-07-05-wcd3-minimal-adapter-expansion.md`
Gap: Need minimal adapter expansion script/tests/report.
Status: [ ]

<!-- harness:milestone id="WCD4" status="pending" priority="P0" -->
### WCD4 — Coverage Depth Metric Update
DoD: automation coverage depth is updated with service-line and workflow-surface counts.
Evidence: `docs/reports/2026-07-05-wcd4-coverage-depth-metric.md`
Gap: Pending WCD3.
Status: [ ]

<!-- harness:milestone id="WCD5" status="pending" priority="P0" -->
### WCD5 — Horizon Close And Demo Rehearsal Handoff
DoD: workflow coverage depth status is closed and demo rehearsal quality loop is named.
Evidence: `docs/reports/2026-07-05-workflow-coverage-depth-expansion-close-report.md`
Gap: Pending WCD4.
Status: [ ]

## Recently Closed External Source Body Horizon

- ESB1 source-body connector selection and policy gate — 완료 (`docs/reports/2026-07-05-esb1-source-body-connector-selection.md`)
- ESB2 synthetic source-body fixture contract — 완료 (`docs/reports/2026-07-05-esb2-source-body-fixture-contract.md`)
- ESB3 chunking and retrieval dry run — 완료 (`docs/reports/2026-07-05-esb3-chunking-retrieval-dry-run.md`)
- ESB4 connector leak and policy gate — 완료 (`docs/reports/2026-07-05-esb4-connector-leak-policy-gate.md`)
- ESB5 external source-body connector expansion close gate — 완료 (`docs/reports/2026-07-05-external-source-body-connector-expansion-close-report.md`)

## Recently Closed Private Parser Horizon

- PPR1 authorization-safe adapter proof plan — 완료 (`docs/reports/2026-07-05-ppr1-authorization-safe-adapter-proof.md`)
- PPR2 realistic local fixture adapter contract — 완료 (`docs/reports/2026-07-05-ppr2-fixture-adapter-contract.md`)
- PPR3 deletion and retention rehearsal — 완료 (`docs/reports/2026-07-05-ppr3-deletion-retention-rehearsal.md`)
- PPR4 parser leak and public report gate — 완료 (`docs/reports/2026-07-05-ppr4-public-report-leak-gate.md`)
- PPR5 private parser realism close gate — 완료 (`docs/reports/2026-07-05-private-parser-realism-hardening-close-report.md`)

## Recently Closed RAG Quality Horizon

<!-- harness:milestone id="RQF1" status="completed" priority="P0" -->
### RQF1 — Validation Corpus And Acceptance Contract
DoD: RAG quality commands, dataset boundaries, metrics, promotion blockers, and public-safety rules are explicit.
Evidence: `docs/reports/2026-07-05-rqf1-validation-contract.md`
Gap: Closed by RQF1 validation contract script/tests/report.
Status: [x]

<!-- harness:milestone id="RQF2" status="completed" priority="P0" -->
### RQF2 — Current Retriever Baseline Snapshot
DoD: current default retriever quality is measured against available public-safe eval metadata or documented as blocked by missing local private assets.
Evidence: `docs/reports/2026-07-05-rqf2-baseline-snapshot.md`
Gap: Closed by RQF2 baseline snapshot script/tests/report.
Status: [x]

<!-- harness:milestone id="RQF3" status="completed" priority="P0" -->
### RQF3 — Opt-In Retriever Regression Matrix
DoD: opt-in repair retriever is compared against baseline with pass/fail and rollback evidence.
Evidence: `docs/reports/2026-07-05-rqf3-regression-matrix.md`
Gap: Closed by RQF3 regression matrix script/tests/report.
Status: [x]

<!-- harness:milestone id="RQF4" status="completed" priority="P0" -->
### RQF4 — Promotion Decision Gate
DoD: result is explicit, reversible, and does not promote defaults without stronger evidence and authorization.
Evidence: `docs/reports/2026-07-05-rqf4-promotion-decision.md`
Gap: Closed by RQF4 promotion decision gate script/tests/report.
Status: [x]

<!-- harness:milestone id="RQF5" status="completed" priority="P0" -->
### RQF5 — Horizon Close And Next Gap Handoff
DoD: RAG quality status is closed as promote/defer/blocked and the next objective-gap horizon is named.
Evidence: `docs/reports/2026-07-05-rag-quality-fresh-validation-close-report.md`
Gap: Closed by RQF5 close gate script/tests/report.
Status: [x]

## Recent Closed Demo Horizon

<!-- harness:milestone id="E2E1" status="completed" priority="P0" -->
### E2E1 — Demo Asset Inventory And Storyboard
DoD: required public-safe reports are inventoried, ordered into one demo story, and checked for protected-data boundaries.
Evidence: `docs/reports/2026-07-05-e2e1-demo-asset-inventory.md`
Gap: Closed by E2E1 inventory script/tests/report.
Status: [x]

<!-- harness:milestone id="E2E2" status="completed" priority="P0" -->
### E2E2 — Scenario Contract
DoD: demo stages have input, evidence, output, review checkpoint, operator command, and failure boundary.
Evidence: `docs/reports/2026-07-05-e2e2-scenario-contract.md`
Gap: Closed by E2E2 scenario contract script/tests/report.
Status: [x]

<!-- harness:milestone id="E2E3" status="completed" priority="P0" -->
### E2E3 — Demo Packet Builder
DoD: one ordered packet/index lets an operator follow the demo without reading ROADMAP internals.
Evidence: `docs/reports/end-to-end-demo/INDEX.md`
Gap: Closed by E2E3 packet builder script/tests/index.
Status: [x]

<!-- harness:milestone id="E2E4" status="completed" priority="P0" -->
### E2E4 — Demo Smoke And Navigation Gate
DoD: packet links, public-safety checks, and missing-report failure path pass.
Evidence: `docs/reports/2026-07-05-e2e4-demo-smoke-gate.md`
Gap: Closed by E2E4 smoke gate script/tests/report.
Status: [x]

<!-- harness:milestone id="E2E5" status="completed" priority="P0" -->
### E2E5 — Horizon Close Gate
DoD: E2E1~E2E4 evidence is combined into demo-ready/partial/blocked close result and next horizon handoff.
Evidence: `docs/reports/2026-07-05-end-to-end-demo-scenario-close-report.md`
Gap: Closed by E2E5 close gate script/tests/report.
Status: [x]

## Horizon Milestones

- MAH1 runtime evidence boundary audit — 완료 (`docs/reports/2026-07-05-mah1-runtime-evidence-boundary-audit.md`)
- MAH2 runtime evidence contract hardening — 완료 (`docs/reports/2026-07-05-mah2-runtime-evidence-contract.md`)
- MAH3 review pack authority panel — 완료 (`docs/reports/2026-07-05-mah3-review-pack-authority-panel.md`)
- FPS1 product surface inventory and demo flow — 완료 (`docs/reports/2026-07-05-fps1-product-surface-inventory.md`)
- FPS2 operator demo command — 완료 (`docs/reports/2026-07-05-fps2-operator-demo-command.md`)
- FPS3 readiness checklist and local install path — 완료 (`docs/reports/2026-07-05-fps3-readiness-checklist.md`)
- FPS4 product narrative README surface — 완료 (`docs/reports/2026-07-05-fps4-product-narrative.md`)
- FPS5 firm-facing surface close gate — 완료 (`docs/reports/2026-07-05-firm-facing-product-surface-close-report.md`)
- PTQ1 trust evidence inventory — 완료 (`docs/reports/2026-07-05-ptq1-trust-evidence-inventory.md`)
- PTQ2 review pack confidence contract — 완료 (`docs/reports/2026-07-05-ptq2-review-pack-confidence-contract.md`)
- PTQ3 failure boundary matrix — 완료 (`docs/reports/2026-07-05-ptq3-failure-boundary-matrix.md`)
- PTQ4 promotion decision evidence pack — 완료 (`docs/reports/2026-07-05-ptq4-promotion-decision-evidence.md`)
- PTQ5 trust and quality close gate — 완료 (`docs/reports/2026-07-05-product-trust-quality-close-report.md`)
- RLP1 parser prototype asset inventory — 완료 (`docs/reports/2026-07-05-rlp1-parser-prototype-asset-inventory.md`)
- RLP2 local fixture parser adapter — 완료 (`docs/reports/2026-07-05-rlp2-local-fixture-parser-adapter.md`)
- RLP3 deletion automation simulation — 완료 (`docs/reports/2026-07-05-rlp3-deletion-automation-simulation.md`)
- RLP4 private payload leak tests — 완료 (`docs/reports/2026-07-05-rlp4-private-payload-leak-tests.md`)
- RLP5 local parser prototype close gate — 완료 (`docs/reports/2026-07-05-real-local-parser-prototype-close-report.md`)
- SBI1 source class selection and authorization boundary — 완료 (`docs/reports/2026-07-05-sbi1-source-class-selection.md`)
- SBI2 source body policy record — 완료 (`docs/reports/2026-07-05-sbi2-source-body-policy-record.md`)
- SBI3 synthetic body parser and chunker — 완료 (`docs/reports/2026-07-05-sbi3-synthetic-body-parser-chunker.md`)
- SBI4 retrieval gate for controlled lane — 완료 (`docs/reports/2026-07-05-sbi4-controlled-lane-retrieval-gate.md`)
- SBI5 controlled lane close gate — 완료 (`docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md`)
- WCE1 coverage gap ranking — 완료 (`docs/reports/2026-07-05-wce1-coverage-gap-ranking.md`)
- WCE2 first new workflow candidate contract — 완료 (`docs/reports/2026-07-05-wce2-first-workflow-contract.md`)
- WCE3 minimal review-pack adapter — 완료 (`docs/reports/2026-07-05-wce3-minimal-review-pack-adapter.md`)
- WCE4 coverage metric update — 완료 (`docs/reports/2026-07-05-wce4-coverage-metric-update.md`)
- WCE5 workflow coverage close gate — 완료 (`docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md`)
- RPG1 promotion evidence inventory — 완료 (`docs/reports/2026-07-05-rpg1-promotion-evidence-inventory.md`)
- RPG2 regression and latency gate — 완료 (`docs/reports/2026-07-05-rpg2-regression-latency-gate.md`)
- RPG3 failure and rollback policy — 완료 (`docs/reports/2026-07-05-rpg3-failure-rollback-policy.md`)
- RPG4 operator promotion command — 완료 (`docs/reports/2026-07-05-rpg4-operator-promotion-command.md`)
- RPG5 promotion gate close report — 완료 (`docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md`)
- OEH1 operator command inventory — 완료 (`docs/reports/2026-07-05-oeh1-operator-command-inventory.md`)
- OEH2 run doctor and environment checks — 완료 (`docs/reports/2026-07-05-oeh2-run-doctor.md`)
- OEH3 report manifest and navigation surface — 완료 (`docs/reports/2026-07-05-oeh3-report-manifest.md`)
- OEH4 error recovery playbook — 완료 (`docs/reports/2026-07-05-oeh4-error-recovery-playbook.md`)
- OEH5 operator experience close gate — 완료 (`docs/reports/2026-07-05-operator-experience-hardening-close-report.md`)
- E2E1 demo asset inventory and storyboard — 완료 (`docs/reports/2026-07-05-e2e1-demo-asset-inventory.md`)
- E2E2 scenario contract — 완료 (`docs/reports/2026-07-05-e2e2-scenario-contract.md`)
- E2E3 demo packet builder — 완료 (`docs/reports/end-to-end-demo/INDEX.md`)
- E2E4 demo smoke and navigation gate — 완료 (`docs/reports/2026-07-05-e2e4-demo-smoke-gate.md`)
- E2E5 end-to-end demo scenario close gate — 완료 (`docs/reports/2026-07-05-end-to-end-demo-scenario-close-report.md`)
- OGH1 objective gap horizon candidates — 완료 (`docs/reports/2026-07-05-objective-gap-horizon-candidates.md`)
- RQF1 validation corpus and acceptance contract — 완료 (`docs/reports/2026-07-05-rqf1-validation-contract.md`)
- RQF2 current retriever baseline snapshot — 완료 (`docs/reports/2026-07-05-rqf2-baseline-snapshot.md`)
- RQF3 opt-in retriever regression matrix — 완료 (`docs/reports/2026-07-05-rqf3-regression-matrix.md`)
- RQF4 promotion decision gate — 완료 (`docs/reports/2026-07-05-rqf4-promotion-decision.md`)
- RQF5 RAG quality fresh validation close gate — 완료 (`docs/reports/2026-07-05-rag-quality-fresh-validation-close-report.md`)
- PPR1 authorization-safe adapter proof plan — 완료 (`docs/reports/2026-07-05-ppr1-authorization-safe-adapter-proof.md`)
- PPR2 realistic local fixture adapter contract — 완료 (`docs/reports/2026-07-05-ppr2-fixture-adapter-contract.md`)
- PPR3 deletion and retention rehearsal — 완료 (`docs/reports/2026-07-05-ppr3-deletion-retention-rehearsal.md`)
- PPR4 parser leak and public report gate — 완료 (`docs/reports/2026-07-05-ppr4-public-report-leak-gate.md`)

## Closed Horizons

Recent closed horizons are archived in `BACKLOG.md`. This section is history only; it is not the current execution plan.

## Paused Horizons

<!-- harness:goal id="rag-optimization-resume" status="paused" --> `docs/horizons/rag-optimization-resume.md` — RO2 DoD 미확정.
<!-- harness:goal id="rag-agent-integration" status="paused" --> `docs/horizons/rag-agent-integration.md` — RGA2/RGA3 DoD 미확정.

## 성공기준 4축

| 축 | 기준 |
|---|---|
| **A. 실사용** | 매 사용 시 그 자리에서 사용성 직접 확인·수정 (정량 측정 철회) |
| **B. 시험 정확도** | 2차 기출 5~10문항 본인 채점 **80%+** → ✅ 누적 86% |
| **C. 커버리지** | ✅ 100 기준서 / 8,328 paragraphs |
| **D. 포트폴리오** | ✅ M5 블로그 발행으로 1차 충족. 추가 글/README 리포트는 새 horizon 결정 시 별도 판단 |

---

## 다음 세션 진입점

> 현재 상태·다음 할 일 상세는 **`CLAUDE.local.md`** (gitignored handoff).

**[현재 active]** `workflow-coverage-depth-expansion` / WCD3 — minimal adapter expansion.

**[Objective 재정의 2026-07-04]** 프로덕트 지향(법인 소개/PoC가 성공 모습, 로컬 도구킷) — `docs/OBJECTIVE.md`.
horizon 경로: ~~업무 지도~~ ✅ → ~~자동화 확장~~ ✅ → ~~회계법인 서비스라인 지도~~ ✅ → ~~F-ACC sequence~~ ✅ → `Accounting Intelligence Expansion` 진행 중.

**[paused horizon 후보]** RO2(멀티 쿼리 분해), RGA2/RGA3(`rag-agent-integration`).
**[완료된 integration]** `end-to-end-demo-scenario` — 위 5개 제품 약점 horizon을 통합 데모 packet으로 묶음.
**[active objective-gap queue]** `rag-quality-fresh-validation` → `private-parser-realism-hardening` → `external-source-body-connector-expansion` → `workflow-coverage-depth-expansion` → `demo-rehearsal-quality-loop`.

**[콘텐츠 축]** 1116 리스 10/10 완료, 1113(공정가치)·1019(확정급여) entry 완료.

**[옵션]** 한국 상법 인덱싱, 평가 하네스 50문항 자동 채점.

---

## 작업 원칙 (저작권·보안)

- **기준서 PDF·텍스트·임베딩·DB 덤프 절대 git commit 금지** (`.gitignore` 최상단)
- 회계사 2차 기출 dogfood 자료도 commit 금지 (`data/dogfood/`)
- 기준서 PDF·텍스트·임베딩·DB·기출 자료는 공유하지 않음
- 공개 협업 범위는 코드·검색 파이프라인·평가 하네스에 한정

## DB 테이블 채우기 일정

| 테이블 | 현재 | 시점 |
|---|---|---|
| `standard` / `paragraph` / `paragraph_fts` | ✅ 100개 / 8,328행 / trigram | Phase 1·2 완료 |
| `embedding` | ✅ bge-m3 1024d, 100% | Phase 2 완료 |
| `cross_reference` / `amendment` | 🟡 스키마만 | 실사용 마찰 trigger |
| `user_note` / `user_note_v2` | 🟡 17건 seed + v2 runtime + legacy fallback (TERM_BRIDGE dict 이관 완료) | term_bridge/retriever_policy 검색 확장 + answer-time notes |

## 메모

- KASB 메일 v3.4 초안 보류. 외부 공개 단계 진입 시 재활용
- **KICPA K-IFRS 적용 부담 순위**: 공정가치/손상/재평가 27.08% > 금융상품 14.58% > 리스 13.44% > 수익 13.33% > 연결 10.83%
  - Phase 3 첫 시나리오를 금융상품(1109)으로 잡은 근거: DB 강점(556 paragraphs) + 워크플로 결정론적(SPPI→사업모형→분류) + 골든셋 Q003·Q008 재활용. 1순위 공정가치는 DCF·옵션모델·시장데이터까지 필요 → 후속 도전
