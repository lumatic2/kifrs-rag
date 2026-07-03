# Changeset

## Target

- ROADMAP milestone: EH1 — Engine test safety net + refactor + MCP consolidation
- Plan: `docs/plans/2026-07-03-engine-hardening.md` (CS-4)

## Scope

- Files (this repo): `kifrs/mcp_server.py`, `tests/test_store_search.py`, `README.md`
- Files (cross-repo, source of truth): `~/projects/custom-skills/accounting/SKILL.md`
  (deployed to `~/.claude/skills/accounting/` and `~/.codex/skills/accounting/` via
  `bash setup.sh --skill accounting`)
- Reason: `search_lexical`, `search_semantic`, `search_hybrid`, `search_hierarchical`,
  `search_reranked` were five near-identical MCP tools (same `query`/`standard`/`limit`
  signature) with mode-selection trade-off numbers duplicated by hand across their
  docstrings. This is a deliberate breaking change to the MCP surface (decision log,
  `docs/plans/2026-07-03-engine-hardening.md`): user chose consolidation over keeping all 5.
- Expected effect: one `search(query, standard, limit, mode=...)` tool with a single
  mode-selection docstring instead of five. `/accounting` (the only current consumer of
  these tool names) is updated in the same changeset so it isn't left calling tools that no
  longer exist.

## Contract

- Source of truth: `kifrs/mcp_server.py` in this repo for the tool itself; the `/accounting`
  skill's canonical source is `~/projects/custom-skills/accounting/SKILL.md` — never edit
  `~/.claude/skills/accounting/` or `~/.codex/skills/accounting/` directly, always redeploy
  via `bash setup.sh`.
- Compatibility: **breaking**. `mcp__kifrs__search_lexical` / `search_semantic` /
  `search_hybrid` / `search_hierarchical` / `search_reranked` no longer exist as MCP tools;
  any caller must switch to `mcp__kifrs__search(mode=...)`. `mode="lexical"` still works
  without `data/kifrs.db` (JSON fallback); the other four modes still require SQLite and
  raise `ToolError` otherwise (unchanged from CS-3). The JSON-fallback `case_sensitive`
  parameter that `search_lexical` exposed is dropped — no consumer used it (not addressable
  from `/accounting`), and it only affected the legacy no-DB fallback path.
- Out of scope: the recall@k/MRR docstring numbers are no longer hardcoded per-tool (now one
  copy, with a pointer to re-run `python -m kifrs.eval.retrieval` for current figures) but are
  not auto-generated from an eval report file — that would be a separate, undiscussed
  automation; flagged as a possible future changeset, not built here.

## Verification

- [x] Targeted tests: `python -m pytest tests/ -q` — 46 passed (test file updated to call `mcp_server.search(mode=...)` instead of the 5 removed tool names, plus 2 new tests: unknown-mode rejection, reranked-mode parity with `kifrs.embed.search_reranked`)
- [x] CLI smoke: `bash ~/projects/custom-skills/setup.sh --skill accounting` — deploy verification, skill-trigger-acceptance, and hardening-parity checks all passed; `grep` confirms both `~/.claude/skills/accounting/SKILL.md` and `~/.codex/skills/accounting/SKILL.md` now reference `mcp__kifrs__search` only
- [x] Integrated smoke: `python scripts/quality_preflight.py --format text` — ok: True; `python -m compileall kifrs scripts` — ok; manually confirmed `mcp_server.search(mode="reranked"|"lexical")` and unknown-mode `ToolError` behave as expected
- [x] Dirty-tree review: `git status --short` (this repo) shows only `kifrs/mcp_server.py`, `tests/test_store_search.py`, `README.md`, changeset record, ROADMAP; `custom-skills` repo change tracked separately (its own git history, not part of this repo's commit)

## Result

- Status: completed
- Evidence: `kifrs/mcp_server.py` (`search()` consolidated tool, `_SEARCH_MODES`), `tests/test_store_search.py` (46/46), `~/projects/custom-skills/accounting/SKILL.md` (updated + redeployed)
- Notes: no Codex MCP config file hardcodes the old tool names (Codex connects to the kifrs
  MCP server directly and receives whatever tools it currently exposes) — only historical
  session logs/memories reference the old names, which are point-in-time records and were
  not rewritten.
