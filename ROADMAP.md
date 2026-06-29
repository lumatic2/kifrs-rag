# kifrs-rag ROADMAP

> 마지막 업데이트: 2026-06-30 (Engine Quality Ops 현재 scope 완료)
> K-IFRS 기준서 + AI 도구체인으로 회계사 실무의 상당 부분을 본인이 수행하는 개인용 시스템. 공개 레포에는 코드·아키텍처·평가 하네스만 두고, 기준서 원문·파싱 DB·임베딩·dogfood 자료는 로컬에서만 보관.
> 완료 이력(Phase 1~4 + M1~M5) → **`BACKLOG.md`** · 다음 세션 진입점 → **`CLAUDE.local.md`**

## 배경 / 포지셔닝

K-IFRS 기준서를 프로그램적으로 조회할 공식 API/MCP 부재. 빅4 사내 AI는 비공개, 기준서 원문·파싱 텍스트·DB·임베딩·dogfood 자료는 KASB·IFRS Foundation 저작권 장벽 때문에 공개하지 않는다.
- 공개 범위: 코드, 아키텍처 설명, 평가 하네스, 메트릭, 운영 문서
- 비공개 범위: 기준서 PDF, 파싱 텍스트, SQLite DB, 임베딩, 회계사 기출 dogfood 자료
- `tax-agent` 패턴 재사용 → 신규 개발 비용 최소화

## 야망 (CLAUDE.md 동기화)

회계사가 아닌 본인이 AI 도구체인으로 **회계사 수준의 결과물**(분개·검토 메모·분류 판단·주석 초안)을 낸다. 각 단계는 이전 단계 검증 후에만 진행.

| 단계 | 목표 | 상태 |
|---|---|---|
| **Phase 1** | 인프라 — 100 기준서 DB + MCP + /accounting | ✅ (2026-04-14) |
| **Phase 2** | 시험 수준 — 2차 기출 정확 인용 + 적용 해설 | ✅ 졸업 누적 86% (2026-04-28) |
| **Phase 3** | 실무 시나리오 1개 — 금융상품 분류·측정(1109) | ✅ 10/10 (2026-04-28) |
| **Phase 4 (현재)** | 시나리오 확장 + 누적 (리스·수익·공정가치·확정급여 + user_note) | 진행 중 (P4C1~P4C5 완료) |

> 상세 이력은 `BACKLOG.md` "Phase 이력" 참조.

---

## Current Horizon — Engine Quality Ops

<!-- harness:goal id="engine-quality-ops" -->
목표: Phase 4 dogfood에서 확인한 세 축(자동 채점, 외부 권위 인덱스, user_note 운영 품질)을 구현해 RAG 답변 품질을 반복 운영 가능한 로컬 루프로 만든다. 상세 계획: `docs/horizons/engine-quality-ops.md`

**상태**: P4C1~P4C5 콘텐츠 dogfood 완료 후 EQ1/EQ2/EQ3/EQ4/EQ5 품질 운영 루프 완료.
**상위 계획/성공기준**: `docs/plans/2026-06-30-kifrs-direction-success-criteria.md`
**세부 계획**: `docs/plans/2026-06-30-engine-quality-ops.md`

### Active Milestones
<!-- harness:milestone id="EQ1" status="completed" priority="P0" evidence="changesets/20260630-user-note-quality/README.md; changesets/20260630-auto-grading/README.md; changesets/20260630-authority-index/README.md; scripts/engine_quality_smoke.py" -->
#### EQ1 — RAG 품질 운영 루프
- DoD: 자동 채점, 외부 권위 인덱스, user_note 운영 품질을 각각 최소 로컬 실행 가능한 tooling surface로 구현하고, 세 축을 함께 확인하는 integrated smoke를 남긴다.
- Evidence: `changesets/20260630-user-note-quality/README.md`; `changesets/20260630-auto-grading/README.md`; `changesets/20260630-authority-index/README.md`; `scripts/engine_quality_smoke.py`
- Gap: Phase 4는 좋은 dogfood evidence를 만들었지만, 개선 효과를 반복 측정하고 외부 권위/user_note를 운영 품질로 관리하는 루프가 없다.
- Status: [x] user_note audit, local-rag 자동 채점, metadata-only authority index, integrated smoke 완료.

<!-- harness:milestone id="EQ2" status="completed" priority="P0" evidence="changesets/20260630-auto-grading-expanded/README.md; changesets/20260630-authority-source-pack/README.md; changesets/20260630-user-note-schema-v2/README.md; scripts/engine_quality_expanded_smoke.py" -->
#### EQ2 — Engine quality loop 확대
- DoD: 자동 채점 범위를 확대하고 threshold gate를 추가하며, 외부 권위 source pack을 metadata-only로 확장하고, user_note v2 schema migration을 backward-compatible하게 설계·검증한다.
- Evidence: `changesets/20260630-auto-grading-expanded/README.md`; `changesets/20260630-authority-source-pack/README.md`; `changesets/20260630-user-note-schema-v2/README.md`; `scripts/engine_quality_expanded_smoke.py`
- Gap: EQ1은 최소 동작 루프였고, 아직 채점 gate/권위 source pack/user_note 정규화 migration이 없어 운영 확장성이 낮다.
- Status: [x] threshold gate, 6-source authority pack, additive user_note_v2 migration, expanded smoke 완료.

<!-- harness:milestone id="EQ4" status="completed" priority="P0" evidence="changesets/20260630-user-note-v2-runtime/README.md" -->
#### EQ4 — user_note v2 write path 전환
- DoD: 신규 user_note seed/write/read 경로가 `user_note_v2`를 우선 사용하고, legacy `user_note` 읽기 호환성과 비파괴 migration 경계를 유지한다.
- Evidence: `changesets/20260630-user-note-v2-runtime/README.md`; `docs/plans/2026-06-30-user-note-v2-runtime.md`; `scripts/seed_user_notes.py`; `scripts/audit_user_notes.py`
- Gap: EQ2는 `user_note_v2` projection만 만들었고, 실제 신규 작성·조회 경로는 아직 legacy string table 중심이다.
- Status: [x] v2-priority write/read path, legacy fallback, seed idempotency, v2 audit 완료.

- Completed at: 2026-06-30
- Summary: user_note_v2 runtime write/read path completed with legacy fallback

<!-- harness:milestone id="EQ3" status="completed" priority="P0" evidence="changesets/20260630-authority-source-pack-rules/README.md" -->
#### EQ3 — authority source pack 실제 수집 전략
- DoD: 외부 권위 source를 실제 문서/링크 metadata 단위로 수집·검증·랭킹하는 규칙을 만들고, 원문 body 없이 public-safe source pack validator를 통과시킨다.
- Evidence: `changesets/20260630-authority-source-pack-rules/README.md`; `docs/plans/2026-06-30-authority-source-pack-rules.md`; `docs/authority/source_pack_rules.md`; `docs/authority/source_pack.json`; `scripts/validate_authority_source_pack.py`
- Gap: EQ2는 6개 authority source category만 정의했고, 실제 문서 단위 수집 규칙·허용 필드·사용 경계·검증 CLI가 없다.
- Status: [x] metadata/link-only source pack rules, validator, FSS source-pack search smoke 완료.

- Completed at: 2026-06-30
- Summary: authority source pack rules completed with metadata-only validator

<!-- harness:milestone id="EQ5" status="completed" priority="P0" evidence="changesets/20260630-quality-preflight-ci/README.md" -->
#### EQ5 — local-rag threshold CI hook
- DoD: local-rag threshold gate와 metadata validators를 하나의 public-safe preflight 명령으로 묶고, 같은 명령을 CI workflow 템플릿에서 실행할 수 있게 한다.
- Evidence: `changesets/20260630-quality-preflight-ci/README.md`; `docs/plans/2026-06-30-quality-preflight-ci.md`; `scripts/quality_preflight.py`; `docs/ci/quality.yml`
- Gap: EQ2의 threshold gate와 EQ3/EQ4 validators는 개별 명령으로는 통과하지만, 반복 실행 가능한 preflight/CI entrypoint가 없다.
- Status: [x] public-safe preflight command, GitHub Actions workflow template, threshold/metadata/user_note gate 완료.

- Completed at: 2026-06-30
- Summary: public-safe quality preflight and CI hook completed

<!-- harness:milestone id="P4C1" status="completed" priority="P0" evidence="data/dogfood/cpa2/q/q07.md; data/eval/manual/q07_1115_revenue_trace.md; data/scenarios/1115_revenue/WORKFLOW.md" -->
#### P4C1 — 1115 수익 q07 RAG eval case
- DoD: q07을 1115 RAG 평가 케이스로 운영해 clean input, retrieval trace, 인용 검증, failure mode, user_note 후보, 1115 workflow seed까지 남긴다. 답안/채점은 평가 수단이며 목적은 RAG 품질 검증이다.
- Evidence: `data/dogfood/cpa2/q/q07.md`; `data/eval/manual/q07_1115_revenue_trace.md`; `data/scenarios/1115_revenue/WORKFLOW.md`
- Gap: 1115 수익 도메인은 아직 RAG 실전 검증이 없다. q07은 갱신선택권·할인권·유의적 금융요소·재매입약정 네 분기를 한 번에 노출해 검색/인용/판단 연결력을 측정하기 좋다.
- Status: [x] 직관 5/7, 해석 인정 6/7, 인용 정확도 13/13. q07-1은 citation 성공 but 시험 산식/표시 관습 failure로 user_note 후보화.

<!-- harness:milestone id="P4C2" status="completed" priority="P0" evidence="data/scenarios/1116_lease/WORKFLOW.md" -->
#### P4C2 — 1116 리스 잔여 closeout
- DoD: 1116 잔여 시나리오 3·4·6·7·8을 닫아 리스 도메인을 완성 사례로 만든다.
- Evidence: `data/scenarios/1116_lease/WORKFLOW.md`; 각 시나리오 `transaction.md`, `workflow_log.md`, `entries.md`, `review_memo.md`
- Gap: 1116 워크플로는 5/10 완료 상태라 잔여 5개를 닫으면 Phase 4의 첫 완성 도메인이 된다.
- Status: [x] 시나리오 1~10 완성. 신규 closeout: 3 단기·소액, 4 금융→운용, 6 금융→금융, 7 기간 재평가, 8 매수선택권.

<!-- harness:milestone id="P4C3" status="completed" priority="P0" evidence="data/user_notes/2026-06-30-p4c3-seed-preview.md; scripts/seed_user_notes.py; kifrs/store.py" -->
#### P4C3 — user_note 운영 시작
- DoD: q05/q06/q07 및 1116 closeout에서 나온 term_bridge/exam_convention/retriever_policy 후보 5~10건을 seed하고, 검색 또는 답변 작성 시 적용 규칙을 남긴다.
- Evidence: `data/scenarios/1115_revenue/user_note_candidates.md`; `data/scenarios/1116_lease/WORKFLOW.md`; `data/user_notes/2026-06-30-p4c3-seed-preview.md`
- Gap: 검색 trace와 시나리오에서 failure mode는 모였지만 아직 실제 user_note 운영 규칙/seed로 승격되지 않았다.
- Status: [x] seed 13건 SQLite insert 완료(P4C4 1113 3건 포함), idempotent seed script 추가, `term_bridge`/`retriever_policy`를 검색 전 query expansion에 연결.

<!-- harness:milestone id="P4C4" status="completed" priority="P0" evidence="docs/plans/2026-06-30-p4c4-fair-value-entry.md; data/scenarios/1113_fair_value/WORKFLOW.md" -->
#### P4C4 — 1113 공정가치 도메인 진입 설계
- DoD: 1113 공정가치 도메인의 범위를 기준서 본문 판단, 숫자 모델, 시장데이터, 1036/1016 연결 중 어디까지 다룰지 정하고 첫 eval/scenario seed를 남긴다.
- Evidence: `docs/plans/2026-06-30-p4c4-fair-value-entry.md`; `data/scenarios/1113_fair_value/WORKFLOW.md`; FV-01~FV-03 scenario folders
- Gap: 공정가치는 KICPA 적용 부담 1위지만 DCF·옵션모델·시장데이터가 얽혀 있어 경계 없이 문제풀이로 들어가면 범위가 커진다.
- Status: [x] 범위 경계 확정, 1113 citation map 검증, 수준 1/2/3 seed scenario 3개 작성, user_note 후보 3건 SQLite seed 승격.

<!-- harness:milestone id="P4C5" status="completed" priority="P0" evidence="docs/plans/2026-06-30-p4c5-employee-benefits-entry.md; data/scenarios/1019_employee_benefits/WORKFLOW.md; kifrs/store.py; kifrs/mcp_server.py" -->
#### P4C5 — 1019 확정급여 도메인 승격
- DoD: q06을 1019 확정급여와 1037 구조조정충당부채 실무 scenario workflow로 승격하고, 순이자·자산상한·해고급여 해석 분기 user_note가 답변 작성 단계에서 조회되게 한다.
- Evidence: `docs/plans/2026-06-30-p4c5-employee-benefits-entry.md`; `data/scenarios/1019_employee_benefits/WORKFLOW.md`; EB-01~EB-02 scenario folders; `kifrs/store.py`; `kifrs/mcp_server.py`
- Gap: q06은 이미 풀이·채점·failure mode가 있지만 도메인 workflow로 승격되지 않아 재사용성이 낮았다.
- Status: [x] 1019/1037 citation map 검증, scenario 2개 작성, answer-time `get_user_notes` 추가.

### Next Candidates
- 없음. Engine Quality Ops의 현재 후보(EQ1/EQ2/EQ3/EQ4/EQ5)는 모두 완료.
### Planning Rule
- 새 구현은 먼저 `docs/plans/2026-06-30-kifrs-direction-success-criteria.md`의 성공기준 A~E 중 어떤 기준을 닫는지 지정한 뒤 시작한다.
- 다음 작업은 milestone 하나만 active로 승격하고, 그 milestone의 성공기준을 만족하면 멈춘다.

## 성공기준 4축

| 축 | 기준 |
|---|---|
| **A. 실사용** | 매 사용 시 그 자리에서 사용성 직접 확인·수정 (정량 측정 철회) |
| **B. 시험 정확도** | 2차 기출 5~10문항 본인 채점 **80%+** → ✅ 누적 86% |
| **C. 커버리지** | ✅ 100 기준서 / 8,328 paragraphs |
| **D. 포트폴리오** | ✅ M5 블로그 발행으로 1차 충족. 추가 글/README 리포트는 새 horizon 결정 시 별도 판단 |

---

## 다음 세션 진입점

> 현재 상태·다음 할 일 상세는 **`CLAUDE.local.md`** (gitignored handoff). 아래는 안정적 후보 목록.

**[현재 active 없음]**

**[다음 후보]**
- 없음. EQ5 완료 후 새 horizon 또는 Phase 4 scenario expansion 여부를 다시 결정.

다음 구현 전 먼저 확인할 문서: `docs/plans/2026-06-30-kifrs-direction-success-criteria.md`

**[콘텐츠 축] Phase 4 잔여**
- 1116 리스: 10/10 완료
- 다른 도메인: 1113(공정가치) entry 완료 / 1019(확정급여) entry 완료

**[옵션, 신호 발생 시 trigger]**
- user_note 활성화 (본문 부재 키워드 매핑 — Q05 공매도 등). 마찰 누적 시 일부 당겨오기
- 한국 상법 인덱싱 (Q04 자본거래만 마찰, 빈도 낮음 → 보류)
- 평가 하네스 50문항 자동 채점 (D축 욕구 살아나면 부활)

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
| `user_note` / `user_note_v2` | 🟡 13건 seed + v2 runtime + legacy fallback | term_bridge/retriever_policy 검색 확장 + answer-time notes |

## 메모

- KASB 메일 v3.4 초안 보류. 외부 공개 단계 진입 시 재활용
- **KICPA K-IFRS 적용 부담 순위**: 공정가치/손상/재평가 27.08% > 금융상품 14.58% > 리스 13.44% > 수익 13.33% > 연결 10.83%
  - Phase 3 첫 시나리오를 금융상품(1109)으로 잡은 근거: DB 강점(556 paragraphs) + 워크플로 결정론적(SPPI→사업모형→분류) + 골든셋 Q003·Q008 재활용. 1순위 공정가치는 DCF·옵션모델·시장데이터까지 필요 → 후속 도전
