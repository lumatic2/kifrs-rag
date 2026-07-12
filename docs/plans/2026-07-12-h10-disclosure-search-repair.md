# Plan: h10-disclosure-search-repair

> Created: 2026-07-12
> Horizon: `docs/horizons/h10-disclosure-search-repair.md` (active)
> Objective: `docs/OBJECTIVE.md` — issue-back → 수리 루프 2회전
> 산출물: 전부 changeset

## Step 트리

### DS1 — search `section` 필터 (P0)

- [x] DS1-S1: search tool `section`/`exclude_bc` 필터 + docstring (verify 3/3: 필터 결과 전부 해당 절 + 미지정 시 기존 동작 바이트 동일 + 미존재 section 빈 결과). **편차**: store/embed 관통 대신 MCP 레이어 후처리 필터 + 오버샘플(×5, 100~500) — 5개 모드 한 곳 커버, eval 경로 불변으로 비퇴행 구조 보장 (changeset `20260712-ds1-section-filter` Contract 참조)
- [x] DS1-S2: mcp-log 재현 4쿼리 before/after — 공시절 top-20 회수 5→20 / 4→14 / 3→8 / 2→16, 1016 73~79 노출 3→8 (acceptance 6+ 초과) + hybrid eval 0.747/0.910/0.488 baseline 정확 일치

### DS2 — 정본 경로 표면화 + close gate (P1)

- [ ] DS2-S1: /accounting SKILL.md 절 단위 수집 안내(전략 A 정본 + section 필터 보조) + setup.sh 배포 + close report (verify: 배포본 grep + focused pytest + in-memory MCP smoke)

## 중단점

- DS1-S2 에서 개선이 관측되지 않으면(공시 문단 회수 증가 없음) 정지·원인 진단 — 필터 위치(후보 풀 전/후) 재설계.

## 결정 로그

- 필터 방식 = section 부분일치(horizon Decision Log 참조). 잔여 사용자 소유 결정 **없음**.

## planning_gate

```yaml
planning_gate:
  team_validation_mode: manual-pass
  scope_posture: selective
  delegation_decision:
    remote_background_agents: skip
    reason: "단일 레포 검색 파라미터 관통 — 재현 쿼리·eval 검증 명확"
    target_roles: []
    execution_path: local_manual
  spec_delta: "issue-back #4 수리 horizon (정규 입력 2회전) — horizon/plan doc + ROADMAP marker"
  dod:
    - "DS1: 재현 4쿼리 section 필터 개선 + 미사용 경로 eval 비퇴행"
    - "DS2: 표면 배포 + close report + smoke 비퇴행"
```
