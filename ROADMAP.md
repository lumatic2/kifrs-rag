# kifrs-rag ROADMAP

> 마지막 업데이트: 2026-07-05 (Non-IFRS Source Dataization 시작)
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
2. `non-ifrs-source-dataization` — 현재. KASB/FSS/법령/DART/client-private source lane을 실제 RAG 데이터화 단위로 확장.
3. `multi-authority-runtime-hardening` — K-IFRS, 법령, 질의회신, 공시, private facts를 권위별로 분리해 답변에 쓴다.
4. `client-private-parser-runtime` — 계약서/TB/회계정책서 같은 로컬 private 파일 parser와 deletion/runtime gate.
5. `firm-facing-product-surface` — 회계법인에 보여줄 demo surface, operator UX, install/readiness 패키지.

## Current Horizon — non-ifrs-source-dataization

<!-- harness:goal id="non-ifrs-source-dataization" status="active" -->
`docs/horizons/non-ifrs-source-dataization.md` — KASB/FSS/법령/DART/client-private source lane을 실제 RAG 데이터화 단위로 확장한다.

직전 horizon에서 K-IFRS RAG baseline과 promotion gate를 닫았다. 이제 IFRS 본문만으로 부족한
해석자료, 법령 locator, 공시 structured fact, client-private local fact를 public-safe record와
chunk/index 정책으로 바꾼다.

## Active Milestones

<!-- harness:milestone id="NIS4" status="active" priority="P0" -->
### NIS4 — chunking and embedding policy
- DoD: source lane별 chunking, embedding, indexing 정책을 코드가 읽을 수 있는 policy 파일로 고정한다.
- Evidence: `docs/reports/2026-07-05-nis4-chunking-embedding-policy.md`; plan `docs/plans/2026-07-05-non-ifrs-source-dataization.md`
- Gap: NIS3는 source record fixture를 만들었지만, 어떤 lane을 embed하고 어떤 lane을 locator/structured lookup으로 둘지 아직 기계 판독 정책이 없다.
- Status: [ ]

## Horizon Milestones

- NIS1 existing source asset inventory — 완료 (`docs/reports/2026-07-05-nis1-source-asset-inventory.md`)
- NIS2 source record contract — 완료 (`docs/reports/2026-07-05-nis2-source-record-contract.md`)
- NIS3 dataization fixtures and validators — 완료 (`docs/reports/2026-07-05-nis3-dataization-fixtures.md`)
- NIS4 chunking and embedding policy — active
- NIS5 dataization gate and runtime handoff

## Closed Horizons

Recent closed horizons are archived in `BACKLOG.md`: rag-reliability-revalidation, field-feedback-capture, field-feedback-runbook,
accountant-feedback-incorporation, real-anonymized-transaction-poc, firm-facing-poc-brief,
toolkit-packaging-readiness, workflow-rebuild, real-case feedback, feedback eval/backlog,
multi-authority runtime, multi-source ingestion, authority source map, rag quality refresh,
product packaging PoC, audit analytical procedures, F-ACC sequence, firm-service-map,
automation-expansion, practice-map, workflow-automation.

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

**[현재 active]** `non-ifrs-source-dataization` — KASB/FSS/법령/DART/client-private source lane 데이터화.
계획: `docs/horizons/non-ifrs-source-dataization.md` →
`docs/plans/2026-07-05-non-ifrs-source-dataization.md`.

**[Objective 재정의 2026-07-04]** 프로덕트 지향(법인 소개/PoC가 성공 모습, 로컬 도구킷) — `docs/OBJECTIVE.md`.
horizon 경로: ~~업무 지도~~ ✅ → ~~자동화 확장~~ ✅ → ~~회계법인 서비스라인 지도~~ ✅ → ~~F-ACC sequence~~ ✅ → `Accounting Intelligence Expansion` 진행 중.

**[paused horizon 후보]** RO2(멀티 쿼리 분해), RGA2/RGA3(`rag-agent-integration`).

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
