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

## Current Horizon — Workflow Automation

<!-- harness:goal id="workflow-automation" -->
목표: 문서 기반 워크플로(WORKFLOW.md)를 실행 가능한 결정 엔진으로 승격해 "시나리오 완료율"을 측정 가능하게 만든다. 상세 계획: `docs/horizons/workflow-automation.md`

**상태**: Engine Hardening(EH1) 완료 후, 2026-07-03 논의로 Objective를 "결정준비 초안까지 자동"으로 재정의(`docs/OBJECTIVE.md`). 1109를 파일럿 도메인으로 결정 엔진 구축 시작.
**세부 계획**: `docs/plans/2026-07-03-wa1-1109-pilot-engine.md`

### Active Milestones
<!-- harness:milestone id="WA1" status="active" priority="P0" -->
#### WA1 — 1109 파일럿 결정 엔진 + 완료율 측정
- DoD: 구조화 거래 입력 → SPPI/사업모형 분류 → 최초인식 분개 → 상각표 포함 후속측정 → 검토메모까지 코드로 실행되고, 기존 10개 1109 시나리오를 회귀 fixture로 재현해 완료율을 측정·기록한다.
- Evidence: (진행 중 — step 완료 시 갱신) `docs/plans/2026-07-03-wa1-1109-pilot-engine.md`
- Gap: WORKFLOW.md 결정트리는 지금 사람(Claude)이 매번 수동으로 따라가야 하는 문서다 — 재현성·결정론성을 코드로 보장하지 못해 "시나리오 완료율" 자체를 측정할 수 없다.
- Status: [ ] Step1 스키마 / [ ] Step2 fixture 인코딩 / [ ] Step3 SPPI / [ ] Step4 사업모형 / [ ] Step5 최초인식 / [ ] Step6 상각표·후속측정 / [ ] Step7 검토메모 / [ ] Step8 회귀 하네스+리포트

### Next Candidates
- WA2 — 완료율 결과 기반 확장 결정 (WA1 완료율·failure mode를 보고 도메인 결정, 아직 scope 미확정)
- WA3 — 사람-개입 필요 케이스 명시 인터페이스 (WA1에서 결정 불가 케이스가 유의미하게 나오면 승격)
### Planning Rule
- WA1은 `docs/plans/2026-07-03-wa1-1109-pilot-engine.md`의 Step1→Step8 순서를 따른다.
- Step6(상각표·후속측정) 이후 각 step은 회귀 fixture 비교로 검증한 뒤에만 다음으로 넘어간다.

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

**[현재 active]** WA1 — 1109 파일럿 결정 엔진 + 완료율 측정 (`docs/plans/2026-07-03-wa1-1109-pilot-engine.md`)

**[다음 후보]**
- WA2/WA3 (`docs/horizons/workflow-automation.md` 참조) — WA1 완료율 결과를 보고 결정.

다음 구현 전 먼저 확인할 문서: `docs/OBJECTIVE.md` → `docs/horizons/workflow-automation.md` → `docs/plans/2026-07-03-wa1-1109-pilot-engine.md`

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
