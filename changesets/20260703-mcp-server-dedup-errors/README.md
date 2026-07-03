# Changeset

## Target

- ROADMAP milestone: EH1 — Engine test safety net + refactor + MCP consolidation
- Plan: `docs/plans/2026-07-03-engine-hardening.md` (CS-3)

## Scope

- Files: `kifrs/mcp_server.py`, `kifrs/store.py`, `tests/test_store_search.py`
- Reason: 6 of 10 MCP tools repeated an `if USE_SQLITE: ... else: ...` dispatch block with
  no shared shape; 5 embedding-backed tools returned `[{"error": ...}]` sentinel dicts on the
  JSON-fallback path instead of a typed error; an empty/corrupt `data/kifrs.db` would only
  fail deep inside a tool's SQL execution, not at server startup.
- Expected effect: one `_dispatch(sqlite_fn, json_fn)` helper replaces the 6 repeated
  branches; embedding-backed tools raise `fastmcp.exceptions.ToolError` via
  `_require_sqlite()` instead of a sentinel a caller has to pattern-match; server startup now
  fails fast with an actionable stderr message if `data/kifrs.db` exists but has zero
  `paragraph` rows.

## Contract

- Source of truth: `kifrs/mcp_server.py` (`_dispatch`, `_require_sqlite`, startup check),
  `kifrs/store.py` (`has_paragraphs`).
- Compatibility: JSON-fallback branch bodies are unchanged (moved into named `_*_json`
  helper functions, not rewritten) — same output for the same input. The 5 embedding tools'
  *behavior contract changes*: callers that previously checked for an `"error"` key in a
  returned list must now catch `ToolError` (or let the MCP client surface it) — this is a
  breaking change for any external caller of those 5 tools, tracked and updated in this
  changeset's own test (`tests/test_store_search.py`).
- Out of scope: `search_lexical`'s JSON-fallback path still lacks the SQLite path's query
  normalization/keyword extraction/term_bridge expansion (documented in the docstring, not
  fixed here — JSON fallback is a legacy no-DB path, not the primary one).

## Verification

- [x] Targeted tests: `python -m pytest tests/ -q` — 44 passed (includes updated `test_mcp_server_json_fallback_raises_tool_error` + 3 new tests for `_dispatch`/`has_paragraphs`/`get_paragraphs_batch`)
- [x] CLI smoke: manual — `reload_store()`, `list_standards()`, `get_paragraph()`, `list_sections()` via `_dispatch` all return expected shapes; `has_paragraphs()` confirmed `True` on the real DB and `False` on a throwaway empty-schema DB
- [x] Integrated smoke: `python scripts/quality_preflight.py --format text` — ok: True; `python -m compileall kifrs scripts` — ok
- [x] Dirty-tree review: `git status --short` shows only `kifrs/mcp_server.py`, `kifrs/store.py`, `tests/test_store_search.py`, changeset record, ROADMAP

## Result

- Status: completed
- Evidence: `kifrs/mcp_server.py` (`_dispatch`, `_require_sqlite`, startup `has_paragraphs()` check), `kifrs/store.py` (`has_paragraphs`), `tests/test_store_search.py` (44/44 total suite passing)
- Notes: the empty-DB startup check calls `sys.exit(1)` — a deliberate hard failure over a
  silent warning, since every SQLite-mode tool would be broken anyway with an empty
  `paragraph` table.
