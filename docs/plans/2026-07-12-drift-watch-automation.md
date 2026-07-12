# Plan: drift-watch-automation

> Created: 2026-07-12
> Horizon: `docs/horizons/drift-watch-automation.md` (active)
> Objective: `docs/OBJECTIVE.md` — 지식 엔진 최신성 유지 무인화
> 산출물: 전부 changeset

## Step 트리

### DR3 — 주간 감지 + 세션 자동 경고 (P0)

- [ ] DR3-S1: `drift.py` PENDING.json 상태 산출(전체 감지 시 항상 기록, drift 0이면 빈 상태) + Windows 작업 스케줄러 주 1회(월 09:00) 등록 + cron.log (verify: `schtasks /run` 1회 실행 관측 — 로그·리포트·PENDING 생성 + `schtasks /query` 등록 확인)
- [ ] DR3-S2: MCP search/get_paragraph 응답에 pending drift 경고 필드(mtime 캐시) + /accounting 안내 (verify: synthetic PENDING → in-memory MCP 경고 발화 / 빈 PENDING → 미발화 + 기존 tool smoke 비퇴행)

## 중단점

- 각 step 검증 PASS 시 커밋. schtasks 권한 실패 등 blocked 시 정지.

## 결정 로그

- 사용자 확정(2026-07-12): Windows 작업 스케줄러 / 주 1회 / 감지만(갱신 수동). 잔여 사용자 소유
  결정 **없음** — 실행 시각(월 09:00)·경고 필드명·캐시 방식은 구현 재량.

## planning_gate

```yaml
planning_gate:
  team_validation_mode: not_required_lightweight
  scope_posture: selective
  delegation_decision:
    remote_background_agents: skip
    reason: "2 changeset·기존 drift 모듈 확장·검증 커맨드 명확 — 자체검토 충분"
    target_roles: []
    execution_path: local_manual
  spec_delta: "새 horizon drift-watch-automation (사용자 발제 예외 2건째) — ROADMAP marker + horizon/plan doc"
  dod:
    - "DR3-S1: schtasks 등록 + 1회 실행 E2E (로그·PENDING 관측)"
    - "DR3-S2: 경고 발화/미발화 양방향 + 기존 tool 비퇴행"
```
