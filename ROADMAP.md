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

## Current Horizon — RAG 최적화 재개

<!-- harness:goal id="rag-optimization-resume" -->
목표: 잔여 miss 9건(hybrid K=20 기준)을 얕은 랭킹/깊은 랭킹으로 진단하고 recall을 재측정한다. 상세 계획: `docs/horizons/rag-optimization-resume.md`

**상태**: RGA1 완료 후 2026-07-03 논의로 재개(2026-07-03 세션 초반 park됐던 후보). 재측정 결과 baseline drift 없음(hybrid recall@20=0.907 그대로), K=100까지 넓히면 9건 중 2건(Q004/Q041) 회복 — 얕은 랭킹/깊은 랭킹(7건) 분리 확인.
**세부 계획**: `docs/plans/2026-07-03-ro1-residual-miss-diagnosis.md`

### Active Milestones
<!-- harness:milestone id="RO1" status="active" priority="P0" -->
#### RO1 — 잔여 miss 진단 + 얕은 랭킹 1차 개선
- DoD: 얕은 랭킹 2건(Q004/Q041)에 candidate pool 확대 적용 후 회복 여부 측정 + 전 지표 비퇴행 확인, 깊은 랭킹 7건은 원인 카테고리 진단 리포트 산출.
- Evidence: docs/reports/2026-07-03-ro1-deep-miss-diagnosis.md;docs/horizons/rag-optimization-resume.md
- Gap: M4 종료(2026-06-27) 이후 잔여 miss 9건의 원인이 분류된 적 없다 — 개선 여지가 있는지조차 모르는 상태.
- Status: [ ]

### Next Candidates
- RO2 — 깊은 랭킹 개선 실험 (RO1 진단 결과로 scope 확정)
- RO3 — 종합 재측정 + 문서화

## Paused Horizons

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

**[현재 active]** RO1 — 잔여 miss 진단 + 얕은 랭킹 1차 개선 (`docs/plans/2026-07-03-ro1-residual-miss-diagnosis.md`, step 트리 3개, 계획 승인 대기).

**[paused horizon 후보 — DoD/Evidence 미확정, RO1 이후 재개 시 §B0.5 Beat 3로 scope 확정]**
- RGA2/RGA3 — `rag-agent-integration` horizon paused 상태로 대기 중
- WA2/WA3 — `workflow-automation` horizon paused 상태로 대기 중

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
