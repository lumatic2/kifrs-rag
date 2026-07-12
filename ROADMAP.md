# kifrs-rag ROADMAP

> 마지막 업데이트: 2026-07-12 (drift-watch-automation close — drift 계열 2 horizon 완료)
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
| Drift watch 자동화 | 주간 스케줄 감지 + MCP drift_warning 자동 경고 | ✅ 2026-07-12 |
| 포트폴리오 시각화 | kifrs.askewly.com — 서가·참조 그래프·eval·파이프라인 4뷰 (메타데이터 전용) | ✅ 2026-07-12 |

## Current Horizon — portfolio-viz-polish

<!-- harness:goal id="portfolio-viz-polish" status="active" -->
목표: kifrs.askewly.com 3축 polish — ① imagegen 비주얼 보강(서가/한지/인주 컨셉) ② 참조 그래프 인터랙션 심화 ③ 콘텐츠 확장(drift 스토리·수리 루프 연대기·상호 링크). 본문 비노출 gate 유지. 사용자 발제 예외 4건째(2026-07-12). (상세 → `docs/horizons/portfolio-viz-polish.md`, step 트리 → `docs/plans/2026-07-12-portfolio-viz-polish.md`)

<!-- harness:milestone id="PP1" status="active" priority="P0" -->
### PP1 — 비주얼 보강 (imagegen)
- DoD: 컨셉 톤 이미지 생성·검수·반입 + 4뷰 실브라우저 E2E + gate 재실행 PASS.
- Gap: 텍스트-only 사이트 — 오늘 확립한 imagegen 파이프라인 재사용 적기.
- Status: [ ]

<!-- harness:milestone id="PP2" status="pending" priority="P1" -->
### PP2 — 인터랙션 + 콘텐츠 + close
- DoD: 그래프 검색/포커스/필터 UX + drift·수리 루프 스토리 섹션(메타데이터 only) + 상호 링크 + 재배포·dist 재스캔 0건 + close report.
- Gap: 수리 루프 2회전 서사가 사이트에 없음 — "살아있는 엔진" 증거 미표출.
- Status: [ ]

## Closed Horizon — h10-disclosure-search-repair (2026-07-12, `h10_disclosure_search_repaired`)

<!-- harness:goal id="h10-disclosure-search-repair" status="completed" -->
목표: H10 issue-back #4 수리 — search() 에 `section` 필터 추가(공시 절 조회 정밀도 구조 결함) + 절 단위 수집 정본 경로 표면화. 정규 issue-back 입력(2회전째). (상세 → `docs/horizons/h10-disclosure-search-repair.md`, step 트리 → `docs/plans/2026-07-12-h10-disclosure-search-repair.md`)

## Closed Horizon — portfolio-viz-site

<!-- harness:goal id="portfolio-viz-site" status="completed" -->
목표: 메타데이터 전용 포트폴리오 시각화 사이트 — 기준서 지도·참조 그래프·eval 대시보드·아키텍처 스토리 4뷰, Astro + Cloudflare(`kifrs.askewly.com`). 본문 비노출 public-safe gate 필수. 사용자 발제 예외 3건째(2026-07-12). (상세 → `docs/horizons/portfolio-viz-site.md`, step 트리 → `docs/plans/2026-07-12-portfolio-viz-site.md`)

<!-- harness:milestone id="PV3" status="completed" priority="P1" evidence="changesets/20260712-pv3-deploy/README.md; https://kifrs.askewly.com" -->
### PV3 — 배포 + 공개 검증
- DoD: `kifrs.askewly.com` 라이브 4뷰 렌더 + 배포 산출물 gate 재실행 PASS.
- Evidence: changesets/20260712-pv3-deploy/README.md; https://kifrs.askewly.com
- Gap: 로컬 빌드는 포트폴리오 증거가 아님 — 공개 URL 이 최종 산출물.
- Status: [x]

- Completed at: 2026-07-12
- Summary: kifrs.askewly.com 라이브 — 4뷰 렌더 + dist 본문 전수 스캔 0건
## Closed Horizon — drift-watch-automation

<!-- harness:goal id="drift-watch-automation" status="completed" -->
목표: drift 감지의 무인화 — Windows 작업 스케줄러 주 1회 감지 + MCP 응답에 pending drift 자동 경고 (갱신은 수동 유지). 사용자 발제 예외 2건째(2026-07-12). (상세 → `docs/horizons/drift-watch-automation.md`, step 트리 → `docs/plans/2026-07-12-drift-watch-automation.md`)

<!-- harness:milestone id="DR3" status="completed" priority="P0" evidence="changesets/20260712-dr3-scheduled-drift-check/README.md; changesets/20260712-dr3-mcp-drift-warning/README.md" -->
### DR3 — 주간 감지 + 세션 자동 경고
- DoD: 스케줄 task 등록+1회 실행 관측(로그·PENDING.json) + MCP 경고 발화/미발화 양방향 검증 + 기존 tool smoke 비퇴행.
- Evidence: changesets/20260712-dr3-scheduled-drift-check/README.md; changesets/20260712-dr3-mcp-drift-warning/README.md
- Gap: 감지·갱신 도구는 있으나 트리거가 사람의 질문뿐 — 안 물으면 stale.
- Status: [x]

- Completed at: 2026-07-12
- Summary: 주간 schtasks 감지(1회 실행 관측) + PENDING 상태 + MCP drift_warning 발화/미발화 검증 — 무인 감지 루프 완성
## Closed Horizon — kasb-drift-watch

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
| D. 포트폴리오 | ✅ 공개 시각화 사이트 **kifrs.askewly.com** 라이브 (2026-07-12) + M5 블로그. 정본 경로는 ai-accounting-firm 공개 웹사이트 |

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
| `cross_reference` | ✅ 1,850행 / 655 기준서 쌍 (본문 언급 추출, 2026-07-12) | PV1 |
| `amendment` | ✅ 134행 (26-1 개정 15건 전량 갱신 diff, 2026-07-12) + standard 에 drift 메타 3컬럼 | DR2 |
| `user_note` / `user_note_v2` | 🟡 17건 seed + v2 runtime | IB1에서 term_bridge 확장 예정 |

## 메모

- KASB 메일 v3.4 초안 보류. 외부 공개 단계 진입 시 재활용
- KICPA K-IFRS 적용 부담 순위: 공정가치 27.08% > 금융상품 14.58% > 리스 13.44% > 수익 13.33% > 연결 10.83%
- retriever default promotion은 `defer` 유지 — ai-accounting-firm 실소비 증거 누적 시 재판단 (`docs/reports/2026-07-05-rqf4-promotion-decision.md`)
