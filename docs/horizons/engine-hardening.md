# Engine Hardening Horizon

> Created: 2026-07-03
> ROADMAP goal id: `engine-hardening`
> Status: proposed (pending user approval)

## Why now

Engine Quality Ops (EQ1~EQ5) closed out the RAG *operating loop* (auto-grading, authority
source pack, user_note_v2). With active milestones exhausted, a code-quality audit
(`docs/roadmap-gap-2026-07-03.md` decision point) surfaced that the engine underneath that
loop has accumulated correctness and maintainability risk that the operating loop itself
does not catch:

- `kifrs/mcp_server.py` and `kifrs/embed.py` — the modules that actually answer queries —
  have zero test coverage; only `store.py`'s FTS/user-note helpers are tested.
- `search_reranked` opens a fresh SQLite connection per candidate (N+1), and the embedding
  matrix (~34MB) is reloaded/reconstructed from BLOBs on every call with no caching.
- `TERM_BRIDGE` query expansion is a hardcoded dict in `store.py`, duplicating what
  `user_note_v2` (`type=term_bridge`) already exists to hold dynamically.
- The MCP surface exposes 5 near-identical search tools (`search_lexical/semantic/hybrid/
  hierarchical/reranked`) with docstrings that embed eval numbers (recall@5, MRR) that will
  silently go stale, and returns `[{"error": ...}]` sentinels instead of raising typed errors.

This horizon turns that audit into scoped tooling changesets before further content/RAG work
resumes on top of an untested, duplicated engine.

## Goal

Make the retrieval engine and its MCP surface test-covered, non-duplicated, and consistent,
without changing retrieval quality (recall/MRR must not regress) — verified by the existing
`eval_quality_gate.py` / `engine_quality_expanded_smoke.py` gates plus new tests.

## Milestone

### EH1 — Engine test safety net + refactor + MCP consolidation

Scope: see `docs/plans/2026-07-03-engine-hardening.md` for the changeset tree, decision log,
and verification plan.

Close criteria:
- `kifrs/mcp_server.py` and `kifrs/embed.py` have test coverage for the previously-untested
  fusion/error paths.
- `search_reranked` N+1 and embedding-matrix reload duplication are fixed with no eval
  regression.
- `TERM_BRIDGE` is migrated into `user_note_v2` seed rows.
- MCP search tools are consolidated into a single `search(query, mode=...)` tool, with
  `/accounting` skill and README updated to match.
- `scripts/quality_preflight.py --format text` still reports `ok: True` after all changes.
