# kifrs-rag ROADMAP

> 마지막 업데이트: 2026-07-05 (Real Case Feedback Loop 완료)
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

## Current Horizon — waiting for feedback eval/backlog integration

`real-case-feedback-loop`은 완료. 다음 추천 horizon은 `feedback-eval-backlog-integration`.
회계사 correction candidate를 파일/리포트 단위 backlog 또는 eval seed 후보로 누적하는 통합 단계다.

병행 사용자 액션: 회계사 1명에게 `docs/reports/field-feedback/INDEX.md` 기준으로 demo를 보여주고
질문지 답변을 받는다.

## Closed Horizons

<!-- harness:goal id="real-case-feedback-loop" status="closed" -->
`docs/horizons/real-case-feedback-loop.md` — close (2026-07-05). RC1~RC4 완료:
anonymized case intake schema, reviewer correction capture, review-pack routing stub, public-safe sample report.
Evidence: `docs/reports/2026-07-05-rc4-real-case-feedback-loop-report.md`.

<!-- harness:goal id="workflow-rebuild-on-richer-knowledge" status="closed" -->
`docs/horizons/workflow-rebuild-on-richer-knowledge.md` — close (2026-07-05). WR1~WR4 완료:
source-aware review pack analyzer, rebuild report command, 1109/1115/1116 coverage report, close gate.
Evidence: `docs/reports/2026-07-05-wr4-workflow-rebuild-close-report.md`.

<!-- harness:goal id="field-feedback-ready-demo" status="closed" -->
`docs/horizons/field-feedback-ready-demo.md` — close (2026-07-05). FF1~FF4 완료:
runtime-aware demo brief, feedback questionnaire, known limitations/human-review boundary, feedback package smoke.
Evidence: `docs/reports/2026-07-05-ff4-feedback-package-close-report.md`.

<!-- harness:goal id="multi-authority-runtime-integration" status="closed" -->
`docs/horizons/multi-authority-runtime-integration.md` — close (2026-07-05). RT1~RT5 완료:
runtime evidence loader, review-pack evidence panel, statement draft fact evidence hook, answer boundary composer,
runtime close demo. Evidence: `docs/reports/2026-07-05-rt5-runtime-close-demo.md`.

<!-- harness:goal id="multi-source-ingestion-pipeline" status="closed" -->
`docs/horizons/multi-source-ingestion-pipeline.md` — close (2026-07-05). MSI1~MSI5 완료:
connector contract, metadata-only source manifest, synthetic structured facts, evidence manifest, close gate.
Evidence: `docs/reports/2026-07-05-msi5-ingestion-gate-close-report.md`.

<!-- harness:goal id="authority-source-map" status="closed" -->
`docs/horizons/authority-source-map.md` — close (2026-07-05). AS1~AS5 완료: source taxonomy,
authority/citation policy, storage boundary, ingestion feasibility, first connector recommendation. Evidence:
`docs/reports/2026-07-05-as5-first-connector-recommendation.md`.

<!-- harness:goal id="rag-quality-refresh" status="closed" -->
`docs/horizons/rag-quality-refresh.md` — close (2026-07-05). RQ1~RQ5 완료: current quality baseline,
eval coverage, retrieval failure taxonomy, per-retriever miss reporting, quality gate report. Evidence:
`docs/reports/2026-07-05-rq5-quality-gate-report.md`, `kifrs/eval/retrieval.py`, `tests/test_eval_retrieval.py`.

<!-- harness:goal id="product-packaging-poc" status="closed" -->
`docs/horizons/product-packaging-poc.md` — close (2026-07-05). PK1~PK5 완료: demo command/output bundle/README/brief. Evidence: `scripts/demo_poc.py`, `docs/reports/demo-poc/`.

<!-- harness:goal id="f-audit-analytical-procedures" status="closed" -->
`docs/horizons/f-audit-analytical-procedures.md` — close (2026-07-05). AP1~AP5 완료: synthetic F/S metrics, anomaly memo, F-ACC linkage. Evidence: `kifrs/workflows/audit_analytics/`.

Older closed horizons are archived in `BACKLOG.md`: F-ACC statement draft, 1109 hardening, disclosure
generalization, 1115 revenue engine, 1109/1116 review packs, firm-service-map, automation-expansion,
practice-map, workflow-automation.

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

**[현재 active]** 없음. 방금 완료한 horizon은 `real-case-feedback-loop`.
다음 추천 horizon: `feedback-eval-backlog-integration`.

병행 사용자 액션: 회계사 1명에게 `docs/reports/field-feedback/INDEX.md` 기준으로 demo를 보여주고
질문지 답변을 받는다.

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
