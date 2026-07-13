# Objective

> Created: 2026-07-03 · Redefined: 2026-07-04 (프로덕트 지향) · **Redefined: 2026-07-12**
> (지식 엔진 재정렬 — 비전 전체는 sibling `~/projects/ai-accounting-firm`으로 이관, 아래 결정 이력 참조)
> Status: active

## North star

**가상 회계법인 AX 프로젝트(`~/projects/ai-accounting-firm`)의 K-IFRS 지식 엔진으로서, 실무자 단위 AX
실험이 요구하는 수준의 고품질·고신뢰 검색과 결정준비 초안 산출을 제공한다.**

"회계사 업무를 AI로 어디까지 자동화할 수 있는가"라는 출발 질문과 그 답의 공개 시각화(웹사이트),
법인 모델링, AX 실험은 2026-07-12부터 umbrella 레포 `ai-accounting-firm`의 Objective가 담당한다. 이 레포는
그 시스템의 K-IFRS 축을 맡는다: 기준서 검색(RAG), 결정 엔진(1109/1116 등), review pack 어댑터.
**결정준비 초안**(분류판단·분개·검토메모)까지 자동 산출하되, 최종 검토·서명·법적 책임은 항상
사람에게 남는다(`/accounting` 스킬의 "의사결정을 대신하지 마라" 규칙 불변).

## 전제 (저작권 — 형태 제약)

기준서 원문·파싱 DB·임베딩은 재배포 불가(KASB·IFRS Foundation). 따라서 프로덕트는 어떤 형태든
**"파이프라인은 공유, 데이터는 사용자가 직접 인덱싱"** 구조가 고정 전제다. 1차 형태는
**로컬 도구킷**(Claude Code + kifrs MCP + /accounting 스킬 + 결정 엔진 모듈 — 설치 후
사용자가 자기 기준서 PDF를 인덱싱)으로 확정(2026-07-04 결정). 독립 앱/웹 서비스는 도구킷이
검증된 뒤 별도 판단.

## 성공 모습 (관측 가능한 최종 상태)

**ai-accounting-firm의 실무자 단위 AX 사례들이 이 엔진을 실소비하며, 사용처에서 드러난 결함이
issue-back → 수리 루프로 닫히는 상태** (2026-07-12 재정의).

중간 관문:
1. ai-accounting-firm 첫 실무자 AX(H4)가 kifrs MCP를 실제 입력으로 통과하고, 결함 목록이 이 레포 backlog로 돌아온다.
2. 그 결함 기준으로 retriever promotion(defer 상태)·user_note 확장 등 품질 결정이 재판단된다.
3. 여러 팀/업무의 AX가 반복 소비해도 품질·성능 회귀가 없다.

(구 성공 모습 "법인 소개/PoC 성사"는 2026-07-12에 ai-accounting-firm의 "공개 웹사이트 포트폴리오" 경로로
대체 — 외부 접촉이 현실적으로 곤란하다는 판단. 결정 이력 참조.)

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
- 2026-07-12: **지식 엔진 재정렬** — 외부 접촉(현업 피드백·법인 소개)이 현실적으로 곤란하여
  검증·포트폴리오 경로를 "가상 회계법인 모델링 + 실무자 단위 AX + 공개 웹사이트"로 재정의.
  그 비전 전체는 신규 umbrella 레포 `~/projects/ai-accounting-firm`이 담당(삼일 기반 리서치, 실명은 입력까지만).
  이 레포는 ai-accounting-firm이 소비하는 K-IFRS 지식 엔진으로 역할을 좁힘. practice-map 자산은
  `ai-accounting-firm/docs/seed/practice-map/`으로 승격(사본, 원본은 이 시점 이후 동결). 다음 horizon은
  내부 hardening 반복 대신 **ai-accounting-firm 사용처에서 돌아온 결함(issue-back)** 기준으로 연다.

- 2026-07-12 (2차): **issue-back 규칙 예외 승인** — 사용자 명시 승인으로 자체 발제 horizon
  `kasb-drift-watch`(KASB 제·개정 drift 감지 + 단위 갱신 경로) 개설. 지식 엔진의 최신성 유지는
  실소비 신뢰성의 전제라는 판단. 규칙 자체는 유지 — 이후 자체 발제도 건별 사용자 승인 필요.

## Active horizon

**2026-07-12 이후 규칙**: 새 horizon은 이 레포 내부 판단이 아니라 `ai-accounting-firm`의 AX 실험에서 돌아온
결함/요구(issue-back)를 입력으로 연다. 내부 hardening horizon 자체 발제는 중단. (retriever
promotion defer 등 열린 결정도 ai-accounting-firm 실소비 증거가 생겼을 때 재판단한다.)

현재 objective-gap queue는 닫혔다. `rag-quality-fresh-validation`은 `defer`로 완료됐고 default retriever 변경은 금지 상태로 유지한다. `private-parser-realism-hardening`은 `realism_contract_ready`, `external-source-body-connector-expansion`은 `connector_body_lane_ready`, `workflow-coverage-depth-expansion`은 `coverage_depth_expanded`, `demo-rehearsal-quality-loop`은 `demo_rehearsal_quality_loop_closed`로 닫혔다.

남은 horizon 순서:

1. `rag-reliability-revalidation` — 완료. K-IFRS RAG 품질 재검증과 default promotion 기준.
2. `non-ifrs-source-dataization` — 완료. KASB/FSS/법령/DART/client-private source lane을 실제 RAG 데이터화 단위로 확장.
3. `multi-authority-runtime-hardening` — 완료. K-IFRS, 법령, 질의회신, 공시, private facts를 권위별로 분리해 답변에 쓴다.
4. `client-private-parser-runtime` — 완료. 계약서/TB/회계정책서 같은 로컬 private 파일 parser와 deletion/runtime gate.
5. `firm-facing-product-surface` — 완료. 회계법인에 보여줄 demo surface와 operator UX.
6. `product-trust-and-quality-evidence` — 완료. 품질 증거, confidence label, failure boundary, retriever promotion decision.
7. `real-local-parser-prototype` — 완료. 실제 로컬 parser prototype에 가까운 synthetic/local-safe 경로.
8. `source-body-ingestion-controlled-lane` — 완료. controlled non-IFRS source-body ingestion lane.
9. `workflow-coverage-expansion` — 완료. service map 기반 업무 coverage 확장.
10. `runtime-retriever-promotion-gate` — 완료. opt-in repair retriever의 default 승격 여부를 promote/defer/rollback gate로 판단.
11. `operator-experience-hardening` — 완료. local operator UX, run doctor, manifest, recovery.

제품 약점 기준 1~5 horizon queue: `docs/plans/2026-07-05-product-weakness-horizon-candidates.md`
완료된 통합 데모 horizon: `docs/horizons/end-to-end-demo-scenario.md`
현재 objective gap queue: `docs/reports/2026-07-05-objective-gap-horizon-candidates.md`
최근 완료 RAG 품질 horizon: `docs/horizons/rag-quality-fresh-validation.md`
최근 완료 horizon: `docs/horizons/demo-rehearsal-quality-loop.md`
현재 active milestone plan: `docs/plans/2026-07-05-demo-rehearsal-quality-loop.md`

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
최근 완료 horizon 상세: `docs/horizons/field-feedback-capture.md`
최근 완료 horizon 상세: `docs/horizons/field-feedback-runbook.md`
최근 완료 horizon 상세: `docs/horizons/accountant-feedback-incorporation.md`
최근 완료 horizon 상세: `docs/horizons/real-anonymized-transaction-poc.md`
최근 완료 horizon 상세: `docs/horizons/firm-facing-poc-brief.md`
최근 완료 horizon 상세: `docs/horizons/feedback-eval-backlog-integration.md`
최근 완료 horizon 상세: `docs/horizons/real-case-feedback-loop.md`
최근 완료 horizon 상세: `docs/horizons/workflow-rebuild-on-richer-knowledge.md`
이전 field-feedback 관련 상세: `docs/horizons/field-feedback-ready-demo.md`
