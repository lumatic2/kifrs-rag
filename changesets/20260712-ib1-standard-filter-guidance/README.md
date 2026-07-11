# Changeset: 20260712-ib1-standard-filter-guidance

## Target

- ROADMAP milestone: IB1 — 리픽싱 계열 검색 수리 (`docs/horizons/h4-issue-back-repair.md`)
- Plan: `docs/plans/2026-07-12-h4-issue-back-repair.md` IB1-b

## Scope

- Files: `kifrs/mcp_server.py` (search tool docstring), `~/projects/custom-skills/accounting/SKILL.md` §2 (cross-repo)
- Reason: H4 실소비 mcp-log #7 — 정확한 고유명사("리픽싱")를 알고 있어도 standard 필터를
  잘못 좁히면(1032) 다른 기준서(1001)에 있는 정답이 검색 대상에서 제외됨. 필터 해제
  재검색이 필수라는 사실이 어느 표면에도 문서화돼 있지 않았음.
- Expected effect: MCP 클라이언트(도구 설명)와 /accounting 스킬(조회 전략) 두 표면 모두에서
  낮은 신뢰도 시 필터 해제 재검색 규칙이 노출됨.

## Contract

- Source of truth: 스킬은 `~/projects/custom-skills/accounting/SKILL.md` (배포본 `~/.claude/skills/`는
  `setup.sh`로만 sync). MCP 도구 설명은 `kifrs/mcp_server.py` docstring.
- Compatibility: 문서/설명만 변경 — 검색 동작·API 불변.
- Out of scope: 낮은 신뢰도 자동 감지·자동 필터 해제 재검색(코드 동작 변경은 이번 issue-back
  범위 밖 — 안내 우선, 자동화는 재발 시 재판단).

## Verification

- [x] Targeted tests: `python -m compileall kifrs/mcp_server.py` 통과, `pytest -k "mcp or search"` 16 passed
- [x] Sync/deploy: `cd ~/projects/custom-skills && bash setup.sh` — hardening parity check 통과
- [x] Deployed grep: `grep -c "필터 함정" ~/.claude/skills/accounting/SKILL.md` → 1
- [x] Dirty-tree review: kifrs-rag는 mcp_server.py + changeset만, custom-skills는 SKILL.md만 변경

## Result

- Status: completed
- Evidence: 두 표면 diff (이 커밋 + custom-skills 커밋), 배포본 grep
- Notes: MCP 도구 설명은 서버 재시작 시 클라이언트에 반영됨(docstring이 tool description).
