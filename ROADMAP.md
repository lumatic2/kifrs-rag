# kifrs-rag ROADMAP

> 마지막 업데이트: 2026-07-04 (FM3 service-line 후보 재판정 완료)
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

## Current Horizon — firm-service-map

<!-- harness:goal id="firm-service-map" status="active" -->
목표: 회계법인 service-line/company map을 세우고 팀별 workflow와 AI insertion point를 재매핑해,
다음 구현 후보를 "법인 팀/산출물" 기준으로 다시 고른다. 상세 plan → `docs/horizons/firm-service-map.md`.

### Completed Milestones (firm-service-map)
<!-- harness:milestone id="FM3" status="completed" priority="P0" evidence="docs/practice-map/service-line-candidates.md;docs/plans/2026-07-04-fm3-service-line-candidate-reprioritization.md" -->
#### FM3 — service-line 기반 AI 후보 재판정
- DoD: 기존 PM3 후보를 Audit용, Accounting Advisory용, Tax-agent 이관, Deal/FAS 후보, 내부자료 필요 보류로 다시 나누고, service-line 설명력·산출물 명확성·현업 피드백 가능성 기준으로 다음 구현 후보를 재정렬한다.
- Evidence: docs/practice-map/service-line-candidates.md;docs/plans/2026-07-04-fm3-service-line-candidate-reprioritization.md
- Gap: PM3 후보는 로컬 검증성 중심이라 법인 PoC에서 어느 팀의 어떤 산출물에 붙는지 설명력이 약했다.
- Status: [x]

- Completed at: 2026-07-04
- Summary: F-ACC review pack(1116 리스 검토메모+분개+주석)을 FM4 1순위 후보로 재판정. 1115 수익 계약 엔진은 2순위, A5/E2/D2/D3는 보류 또는 이관.
<!-- harness:milestone id="FM2" status="completed" priority="P0" evidence="docs/practice-map/team-workflows.md;docs/plans/2026-07-04-fm2-team-workflow-map.md" -->
#### FM2 — 팀별 회계사 workflow 문서화
- DoD: FM1 service-line map을 기준으로 Audit / Accounting Advisory / Tax / Deal / Risk / Consulting workflow를 자료수집→판단→계산/대사→문서화→리뷰 흐름으로 쓰고, 기존 33개 task를 service-line·산출물·AI insertion point에 재매핑한다.
- Evidence: docs/practice-map/team-workflows.md;docs/plans/2026-07-04-fm2-team-workflow-map.md
- Gap: 기존 taxonomy는 task 목록은 있지만 감사팀·회계자문팀·세무팀 등 실제 팀별 업무 흐름과 산출물 맥락이 약해 다음 자동화 후보가 제품/PoC 관점에서 설명력이 부족하다.
- Status: [x]

- Completed at: 2026-07-04
- Summary: 팀별 workflow 문서화 완료 — Audit/F-ACC 중심 재매핑, 33 task service-line 매핑
<!-- harness:milestone id="FM1" status="completed" priority="P0" evidence="docs/practice-map/company-map.md;docs/plans/2026-07-04-fm1-company-service-line-map.md" -->
#### FM1 — 회계법인 company/service-line map
- DoD: Big4·로컬 회계법인의 공개 서비스 구조를 기준으로 service-line v0를 만들고, 각 팀의 고객·산출물·AI insertion point·기존 자산 위치를 정리한다.
- Evidence: docs/practice-map/company-map.md;docs/plans/2026-07-04-fm1-company-service-line-map.md
- Gap: `practice-map`은 회계사 task taxonomy는 만들었지만, 회계법인의 팀/company map을 별도 evidence로 두지 않아 조직 맥락 없이 자동화 후보가 선정됐다.
- Status: [x]

- Completed at: 2026-07-04
- Summary: `company-map.md` v0 작성 — Audit, Accounting Advisory, Tax, Deal/FAS, Risk/K-SOX, Consulting/AI, ESG, Forensic service-line과 기존 자산 위치 재해석.

### Next Candidates
- FM4 — 다음 구현 horizon 선정
- PM2 — 현업 검증(회계사 인터뷰/피드백), 접촉 가능 시 재개

## Closed Horizons

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

**[현재 active 없음]** FM3 완료 — `docs/practice-map/service-line-candidates.md`에서 기존 PM3 후보를
service-line 기준으로 재판정했다. 결론은 F-ACC(Accounting Advisory / F-S support) 집중. 다음은
FM4 — 다음 구현 horizon 선정.

**[Objective 재정의 2026-07-04]** 프로덕트 지향(법인 소개/PoC가 성공 모습, 로컬 도구킷) — `docs/OBJECTIVE.md`. horizon 경로: ~~업무 지도~~ ✅ → ~~자동화 확장~~ ✅ → **회계법인 서비스라인 지도(현재)** → 지도 기반 자동화 확장 → 프로덕트 패키징.

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
