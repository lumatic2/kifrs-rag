# Objective

> Created: 2026-07-03 · **Redefined: 2026-07-04** (프로덕트 지향 전환 — 아래 결정 이력 참조)
> Status: active

## North star

**"회계사 업무를 AI로 어디까지 자동화할 수 있는가"에 실증으로 답하고, 그 답을 회계법인에
소개 가능한 프로덕트로 만든다.**

이 레포의 출발 질문: 실제 K-IFRS·실무 지식을 AI에게 쥐어주면 회계사 업무가 얼마나 자동화되는가.
관찰된 현실(2026-07-04): 주변 회계사들은 AI를 적극 활용하지 않고, 회계법인 사내 AI도 주로
리서치·자료 정리 수준이다. 이 프로덕트의 차별점은 그 지점 너머 — **결정준비 초안**(분류판단·
분개·검토메모)까지 자동 산출하는 것. 최종 검토·서명·법적 책임은 항상 사람에게 남는다
(`/accounting` 스킬의 "의사결정을 대신하지 마라" 규칙 불변).

## 전제 (저작권 — 형태 제약)

기준서 원문·파싱 DB·임베딩은 재배포 불가(KASB·IFRS Foundation). 따라서 프로덕트는 어떤 형태든
**"파이프라인은 공유, 데이터는 사용자가 직접 인덱싱"** 구조가 고정 전제다. 1차 형태는
**로컬 도구킷**(Claude Code + kifrs MCP + /accounting 스킬 + 결정 엔진 패키지 — 설치 후
사용자가 자기 기준서 PDF를 인덱싱)으로 확정(2026-07-04 결정). 독립 앱/웹 서비스는 도구킷이
검증된 뒤 별도 판단.

## 성공 모습 (관측 가능한 최종 상태)

**회계법인에 공식 소개되어 PoC 또는 도입 논의까지 성사된 상태** (2026-07-04 결정).

중간 관문(성공 모습으로 가는 관측 가능한 계단):
1. 회계사 업무 지도 위에 "자동화 가능/조건부/불가" 경계선이 증거와 함께 그려져 있다.
2. 현업 회계사 1명 이상이 실제 업무 사례를 이 도구로 처리해보고 피드백을 남겼다.
3. 데모 자료(영상·사례집)와 반복 실행 가능한 품질 증거가 준비되어 있다.
4. → 법인 소개/PoC.

## 움직이는 축 (현재 → 목표, 측정법)

**축 1 — 업무 지도 커버리지** (신설, 2026-07-04): 회계사 실무 업무 taxonomy 중 자동화 실험이
닿아 "가능/조건부/불가" 판정이 붙은 업무의 비율. 현재 위치: 지도 자체가 없음(0). 첫 목표는
지도 작성 + 기존 자산(1109 엔진 등)의 위치 표기.

**축 2 — 시나리오 완료율** (기존 유지): 도메인별 결정 엔진이 사람 개입 없이 분류판단+분개+
검토메모를 끝까지 산출하는 비율. 현재 위치: 1109 = 6/10(60%), 나머지 도메인 = 엔진 없음(문서만).

축 1이 "어디를 자동화할가"를 고르고, 축 2가 "골라진 곳이 실제로 되는가"를 잰다.

## 경계

- **세무(세법) 영역은 sibling 레포 `tax-agent`가 담당** (2026-07-04 결정). 업무 지도에는 세무
  업무도 *표기*하되, 자동화 실험은 각 레포에서. kifrs-rag은 K-IFRS 회계 중심 유지.
- 기준서 원문·DB·임베딩·dogfood 자료 비공개 원칙 불변 (`CLAUDE.md` 금지 사항).

## 긴 arc (지나온 phase → 갈 phase)

| Phase | 산출물 | 상태 |
|---|---|---|
| 1 — 인프라 | 100 기준서 DB + MCP + `/accounting` | ✅ |
| 2 — 시험 수준 | 2차 기출 정확 인용, 누적 86% | ✅ |
| 3·4 — 시나리오 (문서 기반) | 1109/1116/1115/1113/1019 WORKFLOW.md | ✅ |
| Engine Hardening / Quality Ops | 검색 엔진 테스트·성능·MCP 통합 | ✅ (2026-07-03) |
| Workflow Automation (WA1) | 1109 결정 엔진, 완료율 첫 측정 6/10 | ✅ (2026-07-03, paused — WA2/WA3 잔여) |
| RAG-Agent Integration (RGA1) | 런타임 citation 존재 검증 | ✅ (2026-07-03, paused — RGA2/RGA3 잔여) |
| RAG Optimization (RO1) | 잔여 miss 진단(3 카테고리) | ✅ (2026-07-03, paused — RO2 잔여) |
| **업무 지도** | 회계사 업무 taxonomy + 자동화 가능성 매핑 | ✅ 조건부 close |
| **회계법인 서비스라인 지도** | 회계법인 팀/company map + 팀별 workflow + AI insertion point 재판정 | ✅ |
| **F-ACC 기술 확장 sequence** | 1116/1109/1115 review pack, 주석, 재무제표 후보, 감사분석, demo PoC | ✅ |
| **Accounting Intelligence Expansion (현재)** | K-IFRS RAG 품질 refresh -> 비IFRS 정보원 지도 -> multi-source ingestion/RAG -> 실제 feedback loop | 진행 중 |
| (다음 후보) Objective gap hardening | 성공 모습 대비 부족한 증거를 다시 계량하고 다음 실험을 고른다 | 후보 |
| (최종) 법인 소개/PoC | 성공 모습 | — |

## 결정 이력

- 2026-07-03: "결정준비 초안까지 자동" 정의 (Engine Hardening 이후 논의).
- 2026-07-04: **프로덕트 지향 재정의** — ① 성격: 개인 시스템 → 법인 소개 가능한 프로덕트
  ② 형태: 로컬 도구킷 ③ 성공 모습: 법인 소개/PoC 성사 ④ 업무 지도를 정식 트랙(다음 horizon
  후보)으로 신설 ⑤ 세무는 tax-agent 분리 유지.

## Active horizon

현재 active horizon은 없다. `end-to-end-demo-scenario`는 `demo_ready`로 완료됐고, 제품 약점 5-horizon chain을 회계법인에 설명 가능한 public-safe end-to-end demo packet으로 묶었다.

남은 horizon 순서:

1. `rag-reliability-revalidation` — 완료. K-IFRS RAG 품질 재검증과 default promotion 기준.
2. `non-ifrs-source-dataization` — 완료. KASB/FSS/법령/DART/client-private source lane을 실제 RAG 데이터화 단위로 확장.
3. `multi-authority-runtime-hardening` — 완료. K-IFRS, 법령, 질의회신, 공시, private facts를 권위별로 분리해 답변에 쓴다.
4. `client-private-parser-runtime` — 완료. 계약서/TB/회계정책서 같은 로컬 private 파일 parser와 deletion/runtime gate.
5. `firm-facing-product-surface` — 완료. 회계법인에 보여줄 demo surface, operator UX, install/readiness 패키지.
6. `product-trust-and-quality-evidence` — 완료. 품질 증거, confidence label, failure boundary, retriever promotion decision.
7. `real-local-parser-prototype` — 완료. 실제 로컬 parser prototype에 가까운 synthetic/local-safe 경로.
8. `source-body-ingestion-controlled-lane` — 완료. controlled non-IFRS source-body ingestion lane.
9. `workflow-coverage-expansion` — 완료. service map 기반 업무 coverage 확장.
10. `runtime-retriever-promotion-gate` — 완료. opt-in repair retriever의 default 승격 여부를 promote/defer/rollback gate로 판단.
11. `operator-experience-hardening` — 완료. local operator UX, run doctor, manifest, recovery.

제품 약점 기준 1~5 horizon queue: `docs/plans/2026-07-05-product-weakness-horizon-candidates.md`
완료된 통합 데모 horizon: `docs/horizons/end-to-end-demo-scenario.md`

큰 실행 순서: `docs/horizons/accounting-intelligence-expansion.md`
최근 완료 horizon 상세: `docs/horizons/rag-reliability-revalidation.md`
최근 완료 horizon 상세: `docs/horizons/non-ifrs-source-dataization.md`
최근 완료 milestone plan: `docs/plans/2026-07-05-non-ifrs-source-dataization.md`
최근 완료 horizon 상세: `docs/horizons/multi-authority-runtime-hardening.md`
최근 완료 horizon 상세: `docs/horizons/client-private-parser-runtime.md`
최근 완료 horizon 상세: `docs/horizons/firm-facing-product-surface.md`
최근 완료 milestone plan: `docs/plans/2026-07-05-firm-facing-product-surface.md`
최근 완료 horizon 상세: `docs/horizons/product-trust-and-quality-evidence.md`
최근 완료 horizon 상세: `docs/horizons/real-local-parser-prototype.md`
최근 완료 horizon 상세: `docs/horizons/source-body-ingestion-controlled-lane.md`
최근 완료 horizon 상세: `docs/horizons/workflow-coverage-expansion.md`
최근 완료 horizon 상세: `docs/horizons/runtime-retriever-promotion-gate.md`
최근 완료 horizon 상세: `docs/horizons/operator-experience-hardening.md`
최근 완료 milestone plan: `docs/plans/2026-07-05-operator-experience-hardening.md`
제품 약점 후보 queue: `docs/plans/2026-07-05-product-weakness-horizon-candidates.md`
현재 active horizon 상세: `docs/horizons/end-to-end-demo-scenario.md`
현재 active milestone plan: `docs/plans/2026-07-05-end-to-end-demo-scenario.md`
최근 완료 demo packet: `docs/reports/end-to-end-demo/INDEX.md`
최근 완료 close report: `docs/reports/2026-07-05-end-to-end-demo-scenario-close-report.md`
주의: 패키징은 현재 계획에서 제외한다. 필요하면 사용자가 별도로 지시할 때 새 horizon으로 계획한다.
최근 완료 horizon 상세: `docs/horizons/field-feedback-capture.md`
최근 완료 horizon 상세: `docs/horizons/field-feedback-runbook.md`
최근 완료 horizon 상세: `docs/horizons/accountant-feedback-incorporation.md`
최근 완료 horizon 상세: `docs/horizons/real-anonymized-transaction-poc.md`
최근 완료 horizon 상세: `docs/horizons/firm-facing-poc-brief.md`
최근 완료 horizon 상세: `docs/horizons/toolkit-packaging-readiness.md`
최근 완료 horizon 상세: `docs/horizons/feedback-eval-backlog-integration.md`
최근 완료 horizon 상세: `docs/horizons/real-case-feedback-loop.md`
최근 완료 horizon 상세: `docs/horizons/workflow-rebuild-on-richer-knowledge.md`
피드백 패키지 horizon 상세: `docs/horizons/field-feedback-ready-demo.md`
