# kifrs-rag ROADMAP

> 마지막 업데이트: 2026-07-04 (F-ACC review pack horizon 시작)
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

## Current Horizon — f-acc-review-pack

<!-- harness:goal id="f-acc-review-pack" status="active" -->
목표: 1116 리스 엔진과 주석 초안을 회계자문팀(F-ACC) workpaper pack으로 묶어, 법인 PoC에서
"이 팀의 이 산출물을 줄인다"가 보이는 제품 표면을 만든다. 상세 plan → `docs/horizons/f-acc-review-pack.md`.

### Completed Milestones (f-acc-review-pack)
<!-- harness:milestone id="RP1" status="completed" priority="P0" evidence="kifrs/workflows/kifrs1116/review_pack.py;tests/test_1116_review_pack.py;docs/reports/2026-07-04-rp1-1116-review-pack-sample.md" -->
#### RP1 — 1116 review pack contract + renderer
- DoD: 기존 1116 runner/review memo/disclosure output을 하나의 structured review pack과 markdown workpaper 초안으로 묶고, fixture 기반 테스트와 sample report를 남긴다.
- Evidence: kifrs/workflows/kifrs1116/review_pack.py;tests/test_1116_review_pack.py;docs/reports/2026-07-04-rp1-1116-review-pack-sample.md
- Gap: 1116 엔진과 주석 초안은 있지만 회계자문팀이 실제로 받을 수 있는 검토메모+분개+주석+리뷰 checklist 패키지 산출물이 없다.
- Status: [x]

- Completed at: 2026-07-04
- Summary: 1116 F-ACC review pack contract+renderer 구현, 신규/기존 1116 테스트 20개 통과
<!-- harness:milestone id="RP2" status="completed" priority="P0" evidence="tests/test_1116_review_pack.py;docs/reports/2026-07-04-rp2-1116-review-pack-fixture-summary.md" -->
#### RP2 — fixture regression + sample pack 확장
- DoD: 기존 1116 fixture 전체에서 review pack 생성 상태를 검증하고, automated / needs_human_review 경계가 AE1 완료율과 일치하는지 요약 리포트로 남긴다.
- Evidence: tests/test_1116_review_pack.py;docs/reports/2026-07-04-rp2-1116-review-pack-fixture-summary.md
- Gap: RP1은 대표 fixture 산출물은 만들었지만, 전체 1116 fixture에 review pack contract가 안정적으로 적용되는지 별도 evidence가 없었다.
- Status: [x]

- Completed at: 2026-07-04
- Summary: 1116 fixture 10개 review pack 생성 검증 완료 — automated 9, needs_human_review 1, 신규/기존 1116 테스트 20개 통과
### Next Candidates
- RP3 — NeedsHumanReview checklist hardening
- RP4 — PoC demo brief
- PM2 — 현업 검증(회계사 인터뷰/피드백), 접촉 가능 시 재개

## Closed Horizons

<!-- harness:goal id="firm-service-map" status="closed" -->
`docs/horizons/firm-service-map.md` — close (2026-07-04). FM1(company/service-line map) + FM2(team workflow map) + FM3(service-line 후보 재판정) 완료. FM4 결정: 다음 구현 horizon은 F-ACC review pack(1116 리스 검토메모+분개+주석)으로 확정. 상세 evidence: `docs/practice-map/company-map.md`, `docs/practice-map/team-workflows.md`, `docs/practice-map/service-line-candidates.md`.

<!-- harness:goal id="automation-expansion" status="closed" -->
`docs/horizons/automation-expansion.md` — close (2026-07-04). AE1(1116 엔진 9/10) + AE2(1116 주석 8/11 자동, DART 3사 대사) 완료. 완료율 축 2-도메인화 + 커버리지 축 3→4/33. AE3(NeedsHumanReview 인터페이스)는 신호 종속으로 이월. Objective 임팩트: 두 축 동시 전진, 차별점 가설 2차 지지.

<!-- harness:goal id="practice-map" status="closed" -->
`docs/horizons/practice-map.md` — 조건부 close (2026-07-04). PM1(taxonomy 33 task) + PM3(전수 판정 + 추천: 1116 먼저 + 주석 다음) 완료, PM2는 위 Next Candidates로 이월. 상세 marker 이력 → `BACKLOG.md`.

<!-- harness:goal id="workflow-automation" status="closed" -->
`docs/horizons/workflow-automation.md` — close (2026-07-04). WA1 완료(6/10, `docs/reports/2026-07-03-wa1-completion-rate.md`), WA2→AE1 흡수, WA3→AE3 이관.

## Paused Horizons

<!-- harness:goal id="rag-optimization-resume" status="paused" -->
`docs/horizons/rag-optimization-resume.md`. RO1 완료(얕은 랭킹 2건 이미 해결, 깊은 랭킹 7건 3-카테고리 진단). RO2(멀티쿼리 분해, 카테고리 C만)는 DoD 미확정 — 재개 시 §B0.5 Beat 3.

<!-- harness:goal id="rag-agent-integration" status="paused" -->
`docs/horizons/rag-agent-integration.md`. RGA1 완료(런타임 citation 존재 검증, 완료율 6/10 유지). RGA2(grounding 신뢰성/성능)·RGA3(신규 도메인 표준화)는 DoD 미확정 — 다음 재개 시 §B0.5 Beat 3.

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

**[현재 active 없음]** RP1/RP2 완료 — 기존 1116 엔진과 주석 초안을 회계자문팀 workpaper pack으로
묶었고, 1116 fixture 10개 전체에서 review pack 생성 상태를 검증했다. 다음은 RP3 또는 RP4.

**[Objective 재정의 2026-07-04]** 프로덕트 지향(법인 소개/PoC가 성공 모습, 로컬 도구킷) — `docs/OBJECTIVE.md`. horizon 경로: ~~업무 지도~~ ✅ → ~~자동화 확장~~ ✅ → ~~회계법인 서비스라인 지도~~ ✅ → **F-ACC review pack(현재)** → 프로덕트 패키징.

**[paused horizon 후보 — 재개 시 §B0.5 Beat 3]**
- RO2 — 멀티 쿼리 분해(카테고리 C, Q039/Q048)
- RGA2/RGA3 — `rag-agent-integration` horizon

**[콘텐츠 축] Phase 4 잔여**
- 1116 리스: 10/10 완료
- 다른 도메인: 1113(공정가치) entry 완료 / 1019(확정급여) entry 완료

**[옵션, 신호 발생 시 trigger]**
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
| `user_note` / `user_note_v2` | 🟡 17건 seed + v2 runtime + legacy fallback (TERM_BRIDGE dict 이관 완료) | term_bridge/retriever_policy 검색 확장 + answer-time notes |

## 메모

- KASB 메일 v3.4 초안 보류. 외부 공개 단계 진입 시 재활용
- **KICPA K-IFRS 적용 부담 순위**: 공정가치/손상/재평가 27.08% > 금융상품 14.58% > 리스 13.44% > 수익 13.33% > 연결 10.83%
  - Phase 3 첫 시나리오를 금융상품(1109)으로 잡은 근거: DB 강점(556 paragraphs) + 워크플로 결정론적(SPPI→사업모형→분류) + 골든셋 Q003·Q008 재활용. 1순위 공정가치는 DCF·옵션모델·시장데이터까지 필요 → 후속 도전
