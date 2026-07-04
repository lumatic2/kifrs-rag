# kifrs-rag ROADMAP

> 마지막 업데이트: 2026-07-04 (Objective 프로덕트 지향 재정의 + PM1 완료)
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

## Current Horizon — 업무 지도 (Practice Map)

<!-- harness:goal id="practice-map" -->
목표: 회계사 실무 업무 taxonomy를 작성하고 자동화 가능성을 매핑해, 다음 자동화 대상을 실무 가치 기준으로 고를 수 있게 한다. 상세 계획: `docs/horizons/practice-map.md`

**상태**: 2026-07-04 Objective 프로덕트 지향 재정의와 함께 신설. 지금까지 도메인 선택이 기준서 구조 기준이었던 것을 실무 가치 기준으로 전환하는 기반 작업.
**세부 계획**: `docs/plans/2026-07-04-pm1-practice-taxonomy.md`

### Active Milestones
<!-- harness:milestone id="PM1" status="completed" priority="P0" evidence="docs/practice-map/taxonomy.md;docs/practice-map/sources.md" -->
#### PM1 — 회계사 업무 taxonomy 초안
- DoD: 공개 자료 기반 업무 분해 문서(`docs/practice-map/taxonomy.md`) — 세부 task ≥30개, 각 task에 빈도·판단강도·입출력·현 AI활용 메타, 기존 자산 위치 표기, 커버리지 축 0차 측정값.
- Evidence: docs/practice-map/taxonomy.md;docs/practice-map/sources.md
- Gap: "어디까지 자동화 가능한가"에 답할 업무 전체 지도가 없다 — 도메인 선택이 실무 가치가 아니라 기준서 구조 기준이었다.
- Status: [x]

- Completed at: 2026-07-04
- Summary: 회계사 업무 taxonomy v0 -- 33 task 5대분류, 커버리지 0차 측정 2/33(6%)
<!-- harness:milestone id="PM3" status="completed" priority="P0" evidence="docs/practice-map/taxonomy.md;docs/practice-map/candidates.md;docs/horizons/practice-map.md" -->
#### PM3 — 자동화 가능성 매핑 + 다음 자동화 대상 선정
- DoD: 33개 task 전수에 판정(가능/조건부/불가/미실험-유망·보류)+근거, 유망 후보 3~5개 심층 분석(`candidates.md`), 다음 자동화 대상 1~2개 추천(최종 선택은 사용자), 커버리지 축 1차 측정.
- Evidence: docs/practice-map/taxonomy.md;docs/practice-map/candidates.md;docs/horizons/practice-map.md
- Gap: taxonomy는 있으나 판정이 2/33뿐 — "어디까지 자동화 가능한가"의 경계선이 아직 안 그려짐. 다음 자동화 대상을 고를 근거 부재.
- Status: [x]

- Completed at: 2026-07-04
- Summary: 33 task 전수 판정 + 후보 5개 심층분석, 추천: 1116 엔진 이식 먼저 + 주석 초안 다음
### Next Candidates
- PM2 — 현업 검증 (회계사 인터뷰/피드백) — **보류(2026-07-04 사용자 결정: 당장 현업 접촉 어려움)**, 로컬 작업 우선. horizon close 시 이월.

## Paused Horizons

<!-- harness:goal id="rag-optimization-resume" status="paused" -->
`docs/horizons/rag-optimization-resume.md`. RO1 완료(얕은 랭킹 2건 이미 해결, 깊은 랭킹 7건 3-카테고리 진단). RO2(멀티쿼리 분해, 카테고리 C만)는 DoD 미확정 — 재개 시 §B0.5 Beat 3.

<!-- harness:goal id="rag-agent-integration" status="paused" -->
`docs/horizons/rag-agent-integration.md`. RGA1 완료(런타임 citation 존재 검증, 완료율 6/10 유지). RGA2(grounding 신뢰성/성능)·RGA3(신규 도메인 표준화)는 DoD 미확정 — 다음 재개 시 §B0.5 Beat 3.

<!-- harness:goal id="workflow-automation" status="paused" -->
`docs/horizons/workflow-automation.md`. WA1 완료(6/10=60%, `docs/reports/2026-07-03-wa1-completion-rate.md`). WA2/WA3는 RGA1 결과를 보고 이 horizon과 합쳐 재개할지 판단.
- WA2 — 완료율 결과 기반 확장 결정 (IFRIC19/SPPI재설정불일치/재분류/외화이중트랙 4건 처리 또는 도메인 이식)
- WA3 — 사람-개입 필요 케이스 명시 인터페이스 (`NeedsHumanReview` MCP/스킬 노출 여부)

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

**[현재 active 없음]** practice-map horizon **조건부 close**(PM1+PM3 완료, PM2 이월 — `docs/horizons/practice-map.md` Close 판정). PM3 추천: 다음 "자동화 확장" horizon에 **1116 엔진 이식(먼저) + 주석 초안 생성(다음)** — 근거 `docs/practice-map/candidates.md`. 사용자 확정 후 §B0.5 Beat 2로 새 horizon 작성.

**[Objective 재정의 2026-07-04]** 프로덕트 지향(법인 소개/PoC가 성공 모습, 로컬 도구킷) — `docs/OBJECTIVE.md` 결정 이력 참조. 후속 horizon 예정 경로: ~~업무 지도~~ ✅ → 자동화 확장(WA2/WA3 흡수 검토) → 프로덕트 패키징.

**[paused horizon 후보 — 재개 시 §B0.5 Beat 3]**
- RO2 — 멀티 쿼리 분해(카테고리 C, Q039/Q048)
- RGA2/RGA3 — `rag-agent-integration` horizon
- WA2/WA3 — `workflow-automation` horizon (자동화 확장 horizon에 흡수 검토)

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
