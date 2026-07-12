# kifrs-rag ROADMAP

> 마지막 업데이트: 2026-07-12 (kasb-drift-watch horizon 개설, h4 완료 블록 BACKLOG 이관)
> 북극성: `~/projects/ai-accounting-firm`(가상 회계법인 AX)의 **K-IFRS 지식 엔진** — 고품질 검색(RAG) + 결정준비 초안 (`docs/OBJECTIVE.md`, 2026-07-12 재정렬)
> line budget: <=150
> 완료 이력 → **`BACKLOG.md`** · 다음 세션 진입점 → **`CLAUDE.local.md`**

## 배경 / 포지셔닝

K-IFRS 기준서를 프로그램적으로 조회할 공식 API/MCP 부재. 기준서 원문·파싱 텍스트·DB·임베딩·dogfood 자료는 KASB·IFRS Foundation 저작권 장벽 때문에 공개하지 않는다.
- 공개 범위: 코드, 아키텍처 설명, 평가 하네스, 메트릭, 운영 문서
- 비공개 범위: 기준서 PDF, 파싱 텍스트, SQLite DB, 임베딩, 회계사 기출 dogfood 자료
- 2026-07-12 규칙: **새 horizon은 ai-accounting-firm 사용처 결함(issue-back)만 입력으로 연다** — 내부 hardening 자체 발제 중단 (예외: 사용자 명시 승인 시 — `kasb-drift-watch`가 첫 예외, 2026-07-12)

## 지나온 arc (요약)

| 단계 | 목표 | 상태 |
|---|---|---|
| Phase 1 | 인프라 — 100 기준서 DB + MCP + /accounting | ✅ (2026-04-14) |
| Phase 2 | 시험 수준 — 2차 기출 정확 인용 | ✅ 누적 86% (2026-04-28) |
| Phase 3·4 | 실무 시나리오 — 1109/1116/1115/1113/1019 | ✅ |
| Engine/Quality/Workflow/Firm-facing horizons | 검색 고도화·결정 엔진·demo surface (상세: BACKLOG) | ✅ (~2026-07-06) |
| Issue-back 루프 1회전 (H4) | ai-accounting-firm 실소비 결함 3건 수리 (IB1~IB3) | ✅ 2026-07-12 |
| Drift watch | KASB 제·개정 감지 + 단위 갱신 경로 (실 drift 15건 검출·전량 갱신, drift 0) | ✅ 2026-07-12 |

## Current Horizon — kasb-drift-watch closed

<!-- harness:goal id="kasb-drift-watch" status="completed" -->
목표: KASB 제·개정 공표와 로컬 DB 사이 drift 감지(MCP tool `check_drift` + `kifrs/drift.py` 코어) + 감지된 기준서 단위 갱신 경로(재다운로드→재인제스트→amendment 기록). 자체 발제 — 사용자 승인 예외(2026-07-12). (상세 plan → `docs/horizons/kasb-drift-watch.md`, step 트리 → `docs/plans/2026-07-12-kasb-drift-watch.md`)

## Active Milestones

<!-- harness:milestone id="DR1" status="completed" priority="P0" evidence="changesets/20260712-dr1-drift-detection-core/README.md; changesets/20260712-dr1-check-drift-mcp-tool/README.md" -->
### DR1 — Drift 감지 코어 + MCP tool
- DoD: 실 KASB 대상 E2E 대조 리포트 생성 + MCP tool `check_drift` 실호출 관측 + 네트워크 실패/포맷 변경 시 graceful 에러.
- Evidence: changesets/20260712-dr1-drift-detection-core/README.md; changesets/20260712-dr1-check-drift-mcp-tool/README.md
- Gap: stale 기준서 = 틀린 근거 인용. ai-accounting-firm 실소비 신뢰성 전제인데 감지 수단이 전무.
- Status: [x]

- Completed at: 2026-07-12
- Summary: drift.py 코어+CLI+MCP check_drift — 실 KASB 대조 100/100 매칭, 실 drift 15건(수정목록 26-1) 검출, 실패모드 graceful
<!-- harness:milestone id="DR2" status="completed" priority="P1" evidence="changesets/20260712-dr2-unit-update-path/README.md; changesets/20260712-dr2-report-update-link/README.md" -->
### DR2 — 단위 갱신 경로 + 개정 이력
- DoD: drift 1건(synthetic 가능) 단위 갱신 E2E(재다운로드→재파싱→재인제스트→재임베딩) + 문단 수·retrieval eval 비퇴행 + `amendment` 행 기록.
- Evidence: changesets/20260712-dr2-unit-update-path/README.md; changesets/20260712-dr2-report-update-link/README.md
- Gap: 감지만 하고 갱신 경로가 없으면 반쪽 — `amendment` 테이블 첫 실사용.
- Status: [x]

- Completed at: 2026-07-12
- Summary: 단위 갱신 경로 --update + amendment diff — 실 drift 2건(1024/2101) 갱신 E2E, eval 비퇴행, amendment 첫 실사용 3행
## Next Candidates

- 없음 — 새 후보는 ai-accounting-firm 실소비 issue-back(`BACKLOG.md` Issue-back Queue) 또는 사용자 승인 예외에서만 발생.

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
| `standard` / `paragraph` / `paragraph_fts` | ✅ 100개 / 17,899행 (수정목록 26-1 갱신 반영, 2026-07-12) / trigram | Phase 1·2 + IB2 + DR2 |
| `embedding` | ✅ bge-m3 1024d, 17,899 (100%) | Phase 2 + IB2 + DR2 |
| `cross_reference` | 🟡 스키마만 | 실사용 마찰 trigger |
| `amendment` | ✅ 134행 (26-1 개정 15건 전량 갱신 diff, 2026-07-12) + standard 에 drift 메타 3컬럼 | DR2 |
| `user_note` / `user_note_v2` | 🟡 17건 seed + v2 runtime | IB1에서 term_bridge 확장 예정 |

## 메모

- KASB 메일 v3.4 초안 보류. 외부 공개 단계 진입 시 재활용
- KICPA K-IFRS 적용 부담 순위: 공정가치 27.08% > 금융상품 14.58% > 리스 13.44% > 수익 13.33% > 연결 10.83%
- retriever default promotion은 `defer` 유지 — ai-accounting-firm 실소비 증거 누적 시 재판단 (`docs/reports/2026-07-05-rqf4-promotion-decision.md`)
