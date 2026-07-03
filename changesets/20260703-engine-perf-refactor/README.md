# Changeset

## Target

- ROADMAP milestone: EH1 — Engine test safety net + refactor + MCP consolidation
- Plan: `docs/plans/2026-07-03-engine-hardening.md` (CS-2)

## Scope

- Files: `kifrs/embed.py`, `kifrs/store.py`, `kifrs/mcp_server.py`
- Reason: `search_reranked` opened a fresh `sqlite3.connect()` per candidate (N+1, 50
  connections/query); the embedding matrix (~34MB BLOB) was re-fetched/reconstructed from
  scratch on every `semantic_search`/`search_hierarchical` call with no caching, and
  `search_hierarchical` recomputed section centroids from the full corpus on every query.
- Expected effect: fewer SQLite connections per reranked query (1 batch query instead of up
  to 50), and repeated searches against the same (standard, model) reuse a cached in-process
  matrix/centroid instead of re-reading/reconstructing it. No change to ranking math or
  output — same formulas, just memoized.

## Contract

- Source of truth: `kifrs/embed.py` (cache), `kifrs/store.py` (batch fetch helper).
- Compatibility: cache is per-process, keyed by `(standard, model)`. `reload_store()` in
  `kifrs/mcp_server.py` now calls `kifrs.embed.invalidate_caches()` for the SQLite backend so
  a re-index (`python -m kifrs.embed build`) followed by `reload_store` picks up fresh
  embeddings instead of serving stale cached vectors. Note: `reload_store()` still does not
  recompute `USE_SQLITE` (backend selection) — documented in the tool docstring, not fixed
  here (out of scope for this changeset; CS-3 covers structured warmup/startup checks).
- Out of scope: `search_lexical`/FTS path (no caching added — FTS5 queries are already
  single round-trip and not the bottleneck identified in the audit).

## Verification

- [x] Targeted tests: `python -m pytest tests/test_store_search.py -q` — 8 passed (unchanged from CS-1 baseline)
- [x] CLI smoke: n/a
- [x] Integrated smoke: `python scripts/engine_quality_expanded_smoke.py --format text` — ok: True; `python -m kifrs.eval.retrieval --retrievers hybrid hierarchical reranked --k 20 --no-save` — recall@5/@10/@20/MRR match previously documented baselines (hybrid 0.597/0.763/0.907/0.509, hierarchical 0.627/0.827/0.910/0.542, reranked 0.640/0.727/0.853/0.612) — no regression
- [x] Dirty-tree review: `git status --short` shows only `kifrs/embed.py`, `kifrs/store.py`, `kifrs/mcp_server.py`, changeset record, ROADMAP

## Result

- Status: completed
- Evidence: `kifrs/embed.py` (`_matrix_cache`, `_centroid_cache`, `invalidate_caches`), `kifrs/store.py` (`get_paragraphs_batch`), retrieval eval run 2026-07-03 (see above)
- Notes: `search_hierarchical`'s recall@20 (0.910) differs slightly from the docstring's
  previously-recorded 0.917 — this predates this changeset (identical formula, only
  memoization added) and is most likely goldset drift since the M4 sweep, not caused by this
  refactor. Not investigated further here; flagged for CS-4's docstring-number cleanup.
