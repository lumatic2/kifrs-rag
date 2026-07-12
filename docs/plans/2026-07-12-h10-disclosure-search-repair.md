# Plan: h10-disclosure-search-repair

> Created: 2026-07-12
> Horizon: `docs/horizons/h10-disclosure-search-repair.md` (active)
> Objective: `docs/OBJECTIVE.md` — issue-back → 수리 루프 2회전
> 산출물: 전부 changeset

## Step 트리

### DS1 — search `section` 필터 (P0)

- [ ] DS1-S1: store(search_fts)·embed(semantic/hybrid/hierarchical/reranked) 검색 함수에 `section` LIKE 필터 관통 + mcp_server search tool 파라미터·docstring (verify: 오프라인 단위 — section 필터 결과 전부 해당 절 + 미지정 시 기존 동작 + 존재하지 않는 section 빈 결과)
- [ ] DS1-S2: mcp-log 재현 4쿼리(§7 1116 reranked / §15 1107 reranked / §17 1016 reranked / §22 1116 hierarchical) before/after — `section="공시"` 회수 개선 관측 + 필터 미사용 hybrid eval 비퇴행 (verify: 재현 기록 + eval)

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
