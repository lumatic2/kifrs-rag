# H4 Issue-back Repair — Horizon Close Report (IB3)

> Date: 2026-07-12
> Horizon: `docs/horizons/h4-issue-back-repair.md` (IB1 ✅ → IB2 ✅ → IB3 이 보고서)
> Input: ai-accounting-firm H4 RCPS 실험 mcp-log (2026-07-12, 21회 호출, 유효 17/부분 3/사실상 실패 1)
> Public-safe: 문단 번호·순위·점수만. 산출물: 이 report (close gate는 기록형 — 별도 script 없음, 재현 커맨드 명시)

## 재검증 — mcp-log 실패/부분 사례 동일 쿼리 재실행

재현 환경: 수리 후 코드(`kifrs.embed` 직접 호출 — MCP tool과 동일 함수), 재인제스트 DB(17,896 문단).

| 사례 | 원 결과 | 재실행 결과 | 판정 |
|---|---|---|---|
| #5 `고정 대 고정…` (reranked, std=1032) | 부분 유효 (용어 본문 부재) | 1032-29 (0.796), 1032-16 (0.781) top-2 | **해소** (term_bridge) |
| #7 `…리픽셔닝…` (hybrid, std=1032) | 사실상 실패 | 필터 유지 시 여전히 1001 미도달(설계상 필터가 차단) → **필터 함정 안내 2표면 추가** + 필터 해제 시 1001-한138.5 **rank 1** | **해소** (안내+브리지) |
| #11 `전환가액이 시가 변동에 따라…` (hybrid, 필터 없음) | 핵심 문단 상위권 없음 | hybrid 한138.5 rank 3 / **reranked 한BC104.1 rank 1 (0.928)**, 한138.5 rank 4 | **해소** |
| #15 `get_context(1001, BC)` 수만 자 blob | 토큰 낭비 | BC 246문단 개별화, 한BC104.1 단독 658자, get_context 정상 크기 | **해소** |
| #1/#2 `list_sections` 제목 잘림 | "는 금융상품"·"택권" 등 | 잘린 제목 0 + BC 섹션 구조 노출 | **해소** |

## 품질 게이트 (horizon close 기준)

- `quality_preflight.py` ok (focused pytest / local-rag threshold / authority / user_note audit 전부 통과)
- focused pytest 20 passed (`test_parse_bc_sections.py` 신규 7 포함)
- retrieval eval (goldset 50, hybrid): recall@10 0.713→**0.747**, recall@20 0.887→**0.910**,
  MRR 0.464→**0.490** — BC 세분화에 따른 퇴행을 `_BC_DEMOTE` + 풀 확대로 회복, 전 지표 개선
- 상세: `docs/reports/2026-07-12-ib1-repricing-search-repair.md`, `2026-07-12-ib2-parse-repair.md`

## Close 판정

`h4_issue_back_repaired` — issue-back 3건 전부 수리·재검증 완료. 첫 issue-back → 수리 루프가
Objective 성공 모습대로 1회전 닫힘.

## ai-accounting-firm handoff (그쪽 레포에서 수행)

H4 RCPS 시나리오(`docs/plans/2026-07-12-h4-first-ax-experiment.md`)를 동일 조건으로 재실행해
기본 경로(hybrid/reranked)에서 1001-한138.5/한BC104.1 도달을 확인하면 f-acc-task-01을
`ax_conditional` → `ax_possible`로 승격. **주의: kifrs MCP 서버 재시작(세션 재접속) 후 실행**
(BC 감점 로직은 서버 프로세스 재기동 시 반영).

## 잔여 기록 (다음 issue-back 입력 후보)

- 30자 초과 단일 줄 섹션 제목 미검출(기존 한계), 상위+하위 제목 join 노이즈 드묾, 표 조각 제목 오탐
- 1109 부록 B 대형 문단(B7.2.4, 49k자)
- reranked 같은 조건 직전 baseline 미확보 — 다음 실소비에서 체감 비교
- stale `kifrs.mcp_server` 프로세스 다수 누적(Windows) — RAM 정리 필요 시 수동 kill
