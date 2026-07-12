# Horizon: Drift Watch Automation

> Status: active
> Created: 2026-07-12
> Previous: `docs/horizons/kasb-drift-watch.md` (closed — 감지·갱신 경로 완비)
> Objective 링크: `docs/OBJECTIVE.md` — 지식 엔진 최신성 유지의 무인화 (사용자 발제 2026-07-12, issue-back 규칙 예외 2건째)
> Plan doc: `docs/plans/2026-07-12-drift-watch-automation.md`

## Goal

사람이 "1116 최신이야?"라고 묻지 않아도 drift가 감지·표면화되게 한다:
① **주기 감지** — Windows 작업 스케줄러 주 1회 `python -m kifrs.drift` 실행, 결과를
`data/drift/PENDING.json`(pending 상태 파일)에 유지.
② **세션 내 자동 경고** — kifrs MCP의 search/get_paragraph 응답에, 인용된 기준서가
pending drift 목록에 있으면 경고 필드를 자동 포함 (로컬 파일만 읽음 — 네트워크·성능 영향 없음).
갱신은 수동 유지(`--update <id>`) — eval 비퇴행 확인 기회 보존 (사용자 확정).

## Why now

- kasb-drift-watch가 감지·갱신 도구를 만들었지만 실행 트리거가 사람의 질문뿐 — 안 물으면 stale.
- 첫 실행에서 실 drift 15건이 나온 만큼(26-1 배치), 다음 배치도 반드시 온다.

## Milestones

### DR3. 주간 감지 + 세션 자동 경고 (P0)

Status: active

- Deliverable: ① `PENDING.json` 상태 산출(전체 감지 시 항상 갱신) + Windows 작업 스케줄러
  주 1회 등록 + 실행 로그 ② MCP search/get_paragraph 응답에 drift 경고 자동 포함 +
  /accounting 안내 갱신.
- Acceptance: 스케줄 task 1회 실행 관측(로그+리포트+PENDING 생성) + synthetic pending으로
  MCP 경고 발화·실 pending(빈 상태)으로 미발화 확인 + 기존 tool smoke 비퇴행.

## Close criteria

- DR3 완료. 스케줄러는 사용자 로그온 세션에서 주 1회 실행(월 09:00) — PC 꺼져 있으면 다음 로그온 시 실행.
- 산출물 public-safe 원칙 불변 (PENDING/로그는 data/ 로컬).

## Decision Log

- 스케줄러 = **Windows 작업 스케줄러** (사용자 확정 2026-07-12) — Claude/OpenClaw 상태와 무관.
- 주기 = **주 1회** (사용자 확정) — KASB 개정 공표 빈도(연 수 회) 대비 충분.
- 자동 갱신 = **하지 않음** (사용자 확정) — 감지+경고까지만, DB 변경은 사람이 `--update`.
- 경고 표면 = search/get_paragraph 응답 필드 (구현 재량: PENDING.json mtime 캐시로 파일 읽기 최소화).
