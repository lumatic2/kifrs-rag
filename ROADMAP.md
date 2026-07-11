# kifrs-rag ROADMAP

> 마지막 업데이트: 2026-07-12 (h4-issue-back-repair horizon 개설 + 150줄 compact)
> 북극성: `~/projects/ai-accounting-firm`(가상 회계법인 AX)의 **K-IFRS 지식 엔진** — 고품질 검색(RAG) + 결정준비 초안 (`docs/OBJECTIVE.md`, 2026-07-12 재정렬)
> line budget: <=150
> 완료 이력 → **`BACKLOG.md`** · 다음 세션 진입점 → **`CLAUDE.local.md`**

## 배경 / 포지셔닝

K-IFRS 기준서를 프로그램적으로 조회할 공식 API/MCP 부재. 기준서 원문·파싱 텍스트·DB·임베딩·dogfood 자료는 KASB·IFRS Foundation 저작권 장벽 때문에 공개하지 않는다.
- 공개 범위: 코드, 아키텍처 설명, 평가 하네스, 메트릭, 운영 문서
- 비공개 범위: 기준서 PDF, 파싱 텍스트, SQLite DB, 임베딩, 회계사 기출 dogfood 자료
- 2026-07-12 규칙: **새 horizon은 ai-accounting-firm 사용처 결함(issue-back)만 입력으로 연다** — 내부 hardening 자체 발제 중단

## 지나온 arc (요약)

| 단계 | 목표 | 상태 |
|---|---|---|
| Phase 1 | 인프라 — 100 기준서 DB + MCP + /accounting | ✅ (2026-04-14) |
| Phase 2 | 시험 수준 — 2차 기출 정확 인용 | ✅ 누적 86% (2026-04-28) |
| Phase 3·4 | 실무 시나리오 — 1109/1116/1115/1113/1019 | ✅ |
| Engine/Quality/Workflow/Firm-facing horizons | 검색 고도화·결정 엔진·demo surface (상세: BACKLOG) | ✅ (~2026-07-06) |
| **Issue-back 루프 (현재)** | ai-accounting-firm 실소비 결함 수리 | 진행 중 |

## Current Horizon

<!-- harness:goal id="h4-issue-back-repair" status="active" -->
목표: 첫 issue-back(2026-07-12 H4 RCPS 실험) 결함 3건 수리 — 리픽싱 계열 검색 실패, 1001 BC 통짜 문단, `list_sections` 제목 깨짐. (상세 plan → `docs/horizons/h4-issue-back-repair.md`, step 트리 → `docs/plans/2026-07-12-h4-issue-back-repair.md`)

## Active Milestones

<!-- harness:milestone id="IB1" status="active" priority="P0" -->
### IB1 — 리픽싱 계열 검색 수리
- DoD: 필터 없는 기본 경로(hybrid·reranked)에서 리픽싱 계열 쿼리가 1001-한138.5 계열에 도달 + standard 필터 함정 안내가 tool/skill 표면에 존재.
- Evidence: `docs/reports/2026-07-12-ib1-repricing-search-repair.md` + changesets
- Gap: H4 실소비에서 유일한 사실상 실패(mcp-log #7/#11). f-acc-task-01 ax_possible 승격 조건.
- Status: [ ]

<!-- harness:milestone id="IB2" status="pending" priority="P1" -->
### IB2 — 파싱 수리 (BC 세분화 + 섹션 제목)
- DoD: 1001 한BC 문단 개별 조회 가능 + `list_sections` 제목 무결 + 재인제스트 후 문단 수·retrieval eval 비퇴행.
- Evidence: `docs/reports/2026-07-12-ib2-parse-repair.md` + changesets
- Gap: BC 통짜 문단 토큰 낭비(mcp-log #15) + 섹션 제목 잘림(mcp-log #1/#2).
- Status: [ ]

<!-- harness:milestone id="IB3" status="pending" priority="P1" -->
### IB3 — H4 재검증 close gate
- DoD: mcp-log 실패/부분 사례(#5/#7/#11/#15) 동일 쿼리 재현에서 기본 경로 해소 확인 + horizon close report.
- Evidence: `docs/reports/2026-07-12-h4-issue-back-repair-close-report.md`
- Gap: 수리가 실소비 조건에서 실제로 닫혔는지 재검증 없이 horizon 닫기 금지.
- Status: [ ]

## Next Candidates

- 없음 — 새 후보는 ai-accounting-firm 실소비 issue-back(`BACKLOG.md` Issue-back Queue)에서만 발생.

## Paused Horizons

<!-- harness:goal id="rag-optimization-resume" status="paused" --> `docs/horizons/rag-optimization-resume.md` — RO2 DoD 미확정.
<!-- harness:goal id="rag-agent-integration" status="paused" --> `docs/horizons/rag-agent-integration.md` — RGA2/RGA3 DoD 미확정.

## 성공기준 4축

| 축 | 기준 |
|---|---|
| A. 실사용 | ai-accounting-firm AX 실험이 실소비 (H4 첫 통과: 유효 17/21) |
| B. 시험 정확도 | 2차 기출 80%+ → ✅ 누적 86% |
| C. 커버리지 | ✅ 100 기준서 / 8,328 paragraphs |
| D. 포트폴리오 | ✅ M5 블로그 발행. 이후는 ai-accounting-firm 공개 웹사이트 경로 |

## Closed Horizons

최근 완료 horizon 상세는 `BACKLOG.md` 참조 (2026-07-04~07-06: RAG quality, multi-authority, private parser, firm-facing surface, trust evidence, demo/rehearsal 계열 등 전체 완료).

## 작업 원칙 (저작권·보안)

- **기준서 PDF·텍스트·임베딩·DB 덤프 절대 git commit 금지** (`.gitignore` 최상단)
- 회계사 2차 기출 dogfood 자료도 commit 금지 (`data/dogfood/`)
- 공개 협업 범위는 코드·검색 파이프라인·평가 하네스에 한정

## DB 테이블 채우기 일정

| 테이블 | 현재 | 시점 |
|---|---|---|
| `standard` / `paragraph` / `paragraph_fts` | ✅ 100개 / 8,328행 / trigram | Phase 1·2 완료 |
| `embedding` | ✅ bge-m3 1024d, 100% | Phase 2 완료 |
| `cross_reference` / `amendment` | 🟡 스키마만 | 실사용 마찰 trigger |
| `user_note` / `user_note_v2` | 🟡 17건 seed + v2 runtime | IB1에서 term_bridge 확장 예정 |

## 메모

- KASB 메일 v3.4 초안 보류. 외부 공개 단계 진입 시 재활용
- KICPA K-IFRS 적용 부담 순위: 공정가치 27.08% > 금융상품 14.58% > 리스 13.44% > 수익 13.33% > 연결 10.83%
- retriever default promotion은 `defer` 유지 — ai-accounting-firm 실소비 증거 누적 시 재판단 (`docs/reports/2026-07-05-rqf4-promotion-decision.md`)
