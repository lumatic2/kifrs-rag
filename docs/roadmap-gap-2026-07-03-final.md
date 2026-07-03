# Roadmap Gap Review

Date: 2026-07-03

## North Star
목표: 검색 엔진(mcp_server.py/embed.py)을 테스트 커버·비중복·MCP 통합 상태로 만들되 검색 품질(recall/MRR)은 비퇴행. 상세 계획: `docs/horizons/engine-hardening.md` **상태**: Engine Quality Ops(EQ1~EQ5) 완료 후 코드 감사로 발견된 엔진 자체의 테스트 부재·N+1·MCP tool 중복을 다루는 새 horizon. **세부 계획**: `docs/plans/2026-07-03-engine-hardening.md` ### Active Milestones

## Current State
- EH1: EH1 (evidence: changesets/20260703-engine-test-safety-net/README.md;changesets/20260703-engine-perf-refactor/README.md;changesets/20260703-mcp-server-dedup-errors/README.md;changesets/20260703-mcp-search-tool-consolidation/README.md;changesets/20260703-term-bridge-user-note-migration/README.md)

## Gap
- Active harness milestones are exhausted.
- Compare the north star above with current evidence before starting new implementation.
- Do not infer completion without a new DoD and evidence path.

## Proposed Next Horizon
- N1 - define the next measurable gap.
- N2 - create one evidence-producing milestone.
- N3 - add the smallest validation or smoke gate.

## Recommendation
Promote one proposed item to ROADMAP.md only after the user approves the next horizon.
