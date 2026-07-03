# Changeset

## Target

- ROADMAP milestone: EH1 — Engine test safety net + refactor + MCP consolidation
- Plan: `docs/plans/2026-07-03-engine-hardening.md` (CS-1)

## Scope

- Files: `tests/test_store_search.py` (new)
- Reason: `kifrs/mcp_server.py` and `kifrs/embed.py` had zero test coverage — the RRF fusion,
  hierarchical-fallback, and reranker logic that actually answers queries was only exercised
  by the (slow, model-loading) goldset eval, not by the fast pytest loop.
- Expected effect: a regression in fusion ordering, hierarchical fallback, or the JSON-fallback
  error-sentinel contract now fails a targeted, fast-enough-to-run pytest file. This also pins
  the current `[{"error": ...}]` sentinel contract as a baseline so CS-3's structured-error
  refactor has something concrete to change against.

## Contract

- Source of truth: `tests/test_store_search.py` in this repo.
- Compatibility: skips cleanly (not fail) when `data/kifrs.db` is absent — the DB is gitignored
  per the K-IFRS copyright boundary, so this file never runs in a fresh clone/CI without it.
- Out of scope: not added to `scripts/quality_preflight.py`'s `focused_pytest` list — it loads
  bge-m3 + the cross-encoder reranker, which is too slow for the fast preflight gate.

## Verification

- [x] Targeted tests: `python -m pytest tests/test_store_search.py -q` — 8 passed
- [x] CLI smoke: n/a (test-only changeset)
- [x] Integrated smoke: `python scripts/quality_preflight.py --format text` — ok: True (unaffected, file not wired into preflight by design)
- [x] Dirty-tree review: `git status --short` shows only `tests/test_store_search.py` + changeset record + ROADMAP/BACKLOG/docs from horizon setup

## Result

- Status: completed
- Evidence: `tests/test_store_search.py` (8/8 passing against real local `data/kifrs.db`)
- Notes: this is the safety net for CS-2 (perf refactor) — CS-2 must keep these 8 tests green.
