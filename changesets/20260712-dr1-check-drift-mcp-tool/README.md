# Changeset: DR1-S2 — MCP tool `check_drift` + /accounting 표면

## Target

- ROADMAP milestone: DR1 — Drift 감지 코어 + MCP tool (`kasb-drift-watch` horizon)
- Plan: `docs/plans/2026-07-12-kasb-drift-watch.md` DR1-S2

## Scope

- Files: `kifrs/mcp_server.py` (check_drift tool), `~/projects/custom-skills/accounting/SKILL.md`
  (allowed-tools + 최신성 안내 — source of truth, setup.sh로 배포)
- Reason: 감지 코어를 Claude 세션 안에서 바로 쓸 수 있게 MCP 표면으로 노출 (사용자 확정 형태).
- Expected effect: `mcp__kifrs__check_drift(category, only)` 호출로 drift 요약 반환. /accounting이
  최신 개정 질문에서 check_drift를 쓰도록 안내.

## Contract

- Source of truth: tool=`kifrs/mcp_server.py`, 스킬=`~/projects/custom-skills/accounting/SKILL.md`
  (배포본 `~/.claude/skills/accounting/`은 setup.sh 산출물 — 직접 수정 금지).
- Compatibility: 기존 8 tool 시그니처 불변. drift import는 tool 내부 lazy(경량 requests만 — 한계 #6
  C-확장 아님, startup 영향 없음).
- Out of scope: 갱신 경로(DR2), 스케줄.

## Verification

- [x] Targeted tests: fastmcp in-memory Client로 check_drift 실호출(only=1115) — matched 1, drift 0, MCP 프로토콜 E2E PASS
- [x] CLI smoke: tool 목록 9개(check_drift 등재) + 기존 search 호출 비퇴행(1116 리스부채 top-3 정상)
- [x] Sync/deploy: `setup.sh` 실행 → 배포본 `~/.claude/skills/accounting/SKILL.md` grep 2 hits + trigger acceptance 통과
- [x] Failure mode: category='bogus' → ToolError 반환 + 서버 생존(직후 list_standards 100건 정상)

## Result

- Status: completed (2026-07-12)
- Evidence: MCP in-memory E2E 실행 로그 (위 checklist), 배포본 grep
- Notes: 현 세션 kifrs MCP 서버는 구버전 프로세스 — 새 tool은 서버 재기동 후 세션에 노출됨.
