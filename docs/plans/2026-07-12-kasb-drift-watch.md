# Plan: kasb-drift-watch

> Created: 2026-07-12
> Horizon: `docs/horizons/kasb-drift-watch.md` (active)
> Objective: `docs/OBJECTIVE.md` — 지식 엔진 정확성·최신성 유지
> 산출물: 전부 changeset

## Step 트리

### DR1 — Drift 감지 코어 + MCP tool (P0)

- [ ] DR1-S1: `kifrs/drift.py` 감지 코어 — KASB 파일 목록 fetch(download.py 재사용) → 로컬 `standard.source`+스냅샷(`data/drift/snapshot.json`) 대조 → drift report 생성 + CLI entry (verify: `.venv/Scripts/python -m kifrs.drift` 실 KASB E2E 리포트 관측 + 네트워크 차단 시 graceful 에러)
- [ ] DR1-S2: kifrs MCP tool `check_drift` 노출(얇은 wrapper) + tool docstring·/accounting 표면 안내 (verify: MCP tool 실호출로 대조 결과 관측 + 기존 8 tool smoke 비퇴행)

### DR2 — 단위 갱신 경로 + 개정 이력 (P1)

- [ ] DR2-S1: `standard` 메타 확장(KASB 파일 식별자·감지일) + 기준서 1개 단위 갱신 경로(재다운로드→재파싱→재인제스트→임베딩 재색인, ingest.py 재사용) + `amendment` 이력 기록 (verify: synthetic drift 1건 갱신 E2E — 문단 수·hybrid eval 비퇴행 + amendment 행 확인)
- [ ] DR2-S2: drift 리포트 ↔ 갱신 경로 연결(리포트의 drift 항목에 갱신 커맨드 안내) + horizon close 검증 (verify: 감지→갱신 전체 흐름 1회 통주 + 품질 게이트 비퇴행)

## 중단점

- 각 step 검증 PASS 시 커밋 checkpoint. blocked(KASB 게시판 구조 변경으로 fetch 불가 등) 시 정지.
- eval 퇴행 발견 시 갱신 경로 진행 금지 — 원인 진단 먼저.

## 결정 로그

- 사용자 확정(2026-07-12): 실행 형태=MCP tool, 범위=감지+갱신 경로. 그 외 예상되는 사용자 소유 결정 **없음**
  — 구현 재량(스냅샷 포맷, 리포트 필드, 공표 게시판 부가 신호 포함 여부)은 무중단 진행.

## planning_gate

```yaml
planning_gate:
  team_validation_mode: manual-pass
  scope_posture: selective
  delegation_decision:
    remote_background_agents: skip
    reason: "단일 레포 2 milestone·기존 fetch/ingest 파이프라인 재사용·검증 커맨드 명확 — role lane 자체검토로 충분"
    target_roles: []
    execution_path: local_manual
  spec_delta: "새 horizon kasb-drift-watch (issue-back 규칙 사용자 승인 예외) — OBJECTIVE 결정 이력 + ROADMAP marker + horizon/plan doc"
  perspectives:
    product: "stale 기준서 = 틀린 인용 방지, ai-accounting-firm 실소비 신뢰성 전제"
    architecture: "코어 모듈 + 얇은 MCP wrapper (한계 #6 stdio 규약), download/ingest 재사용으로 신규 표면 최소"
    security: "외부 fetch는 KASB 공개 게시판만, secret 불요. 원문·DB 비공개 원칙 불변 — 리포트는 메타만"
    qa: "실 KASB E2E + 네트워크 실패 모드 + synthetic drift 갱신 E2E + eval 비퇴행"
    skeptic: "KASB 게시판 HTML 구조 변경 시 감지 자체가 깨짐 — 포맷 변경을 에러로 표면화하는 게 감지의 일부"
  dod:
    - "DR1: 실 KASB 대조 리포트 + MCP tool 실호출 + 실패 모드 graceful"
    - "DR2: synthetic drift 갱신 E2E + 문단 수·eval 비퇴행 + amendment 기록"
```
