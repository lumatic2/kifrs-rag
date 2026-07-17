# Plan: Engine Hardening (EH1)

> Horizon: `docs/horizons/engine-hardening.md` (`engine-hardening`)
> Milestone: EH1 — Engine test safety net + refactor + MCP consolidation
> Created: 2026-07-03

## Scope boundary

This run closes EH1 in full if time allows, in changeset order CS-1 → CS-5 (each is
independently committable; CS-2/CS-3/CS-5 depend on CS-1's fixtures existing, CS-4 is
independent of CS-1). Stop points: any changeset that fails its own verification stops
before starting the next changeset. No content/scenario work, no new RAG feature (e.g. no
new search mode) — pure hardening of what already exists.

## Step tree (1 changeset = 1 step, tooling grain)

- [ ] **CS-1 — test safety net for `mcp_server.py` / `embed.py`**
  Add `tests/test_store_search.py` (or similar) using the real local `data/kifrs.db`
  (skip cleanly if `data/kifrs.db` missing, matching this being a gitignored local asset).
  Cover: RRF fusion math in `search_hybrid`, hierarchical centroid fusion, reranker
  candidate pooling/count visibility, `USE_SQLITE` dual-backend error paths.
  (verify: `python -m pytest tests/test_store_search.py -q`)

- [ ] **CS-2 — perf refactor: N+1 fix + embedding/centroid caching**
  Batch-fetch paragraphs in `search_reranked` instead of per-candidate `sqlite3.connect()`;
  add in-process cache for the embedding matrix and section centroids, invalidated by
  `reload_store()`.
  (verify: `python -m pytest tests/test_store_search.py -q` + `python scripts/engine_quality_expanded_smoke.py --format text` shows no recall/MRR regression)

- [ ] **CS-3 — `mcp_server.py` dedup + structured errors + startup DB check**
  Extract the repeated `if USE_SQLITE: ... else: ...` dispatch (6 tools) into one helper;
  replace `[{"error": ...}]` sentinel returns with raised tool errors; add a DB-row-count
  check to warmup so an empty/corrupt `data/kifrs.db` fails at startup, not mid-query; fix
  or explicitly document the `reload_store()` no-op-on-SQLite limitation.
  (verify: `python -m pytest tests/ -q` + manual MCP smoke: `mcp__kifrs__reload_store`, one search call)

- [ ] **CS-4 — MCP tool consolidation: 5 search tools → `search(query, mode=...)`**
  Replace `search_lexical/semantic/hybrid/hierarchical/reranked` with one
  `search(query, standard, limit, mode="hybrid"|"lexical"|"semantic"|"hierarchical"|"reranked")`
  tool; move the recall/MRR trade-off guidance out of the docstring numeric literals into
  one place generated from/pointing at the eval report instead of hand-copied numbers.
  Update `~/projects/custom-skills/accounting/SKILL.md` (source of truth, redeploy via its
  `setup.sh`) and this repo's `README.md` to reference the new single tool.
  (verify: `python -m pytest tests/ -q` + `/accounting` skill manual smoke query after redeploy)

- [ ] **CS-5 — RAG quality: `TERM_BRIDGE` → `user_note_v2`**
  Migrate the 5 hardcoded `TERM_BRIDGE` entries in `store.py` into `user_note_v2` seed rows
  (`type=term_bridge`) via `scripts/seed_user_notes.py`; change query expansion to read
  term bridges from `user_note_v2` instead of the hardcoded dict, keeping the same
  expansion behavior.
  (verify: `python -m pytest tests/ -q` + `python scripts/audit_user_notes.py` + `engine_quality_expanded_smoke.py` non-regression)

## Integration verification (milestone close)

- `python scripts/quality_preflight.py --format text` → `ok: True`
- `python scripts/engine_quality_expanded_smoke.py --format text` → no recall/MRR regression vs current baseline
- `python -m pytest tests/ -q` → all pass

## Decision log

- **MCP tool consolidation (CS-4): consolidate, not additive.** User chose to replace the
  5 search tools with one `search(mode=...)` tool rather than keep all 5. This is a breaking
  change to `/accounting` SKILL.md and any Codex MCP config referencing the old tool names —
  both must be updated in the same changeset, not left to drift.
- **Test strategy (CS-1): real local `data/kifrs.db`, not a synthetic fixture.** User chose
  integration-style tests against the actual local DB over a lightweight fake-embedding
  fixture. Tests must skip cleanly (not fail) in any environment where `data/kifrs.db` is
  absent (e.g. CI, a fresh clone), since the DB is gitignored per this repo's copyright
  boundary.
- No other user-owned decisions expected during CS-1~CS-5 execution (all are mechanical
  refactors/migrations of existing, already-decided behavior). If an unexpected decision
  surfaces (e.g. a real recall/MRR regression that can't be fixed without changing ranking
  behavior), stop and report rather than resolving unilaterally.
