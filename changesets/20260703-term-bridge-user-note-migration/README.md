# Changeset

## Target

- ROADMAP milestone: EH1 — Engine test safety net + refactor + MCP consolidation
- Plan: `docs/plans/2026-07-03-engine-hardening.md` (CS-5)

## Scope

- Files: `kifrs/store.py`, `scripts/seed_user_notes.py`
- Reason: `TERM_BRIDGE` was a hardcoded 5-entry dict in `store.py` duplicating what
  `user_note_v2` (`type=term_bridge`) already exists to hold dynamically — expanding it
  required a code change + redeploy instead of a DB insert, and its logic was a parallel
  code path alongside `_user_note_expansions()`'s DB-backed lookup.
- Expected effect: `expand_query()` now reads term bridges exclusively from
  `user_note_v2`/legacy `user_note` (via `_user_note_expansions()`); adding a new exam-term
  bridge is now `scripts/seed_user_notes.py` + `--apply`, no source change.

## Contract

- Source of truth: `scripts/seed_user_notes.py` `SEEDS` list (idempotent, `--apply` to insert).
- Compatibility: `공매도` was NOT re-seeded — it was already covered by an existing
  `1109-4.2.1` seed with a superset of expansion terms (4 terms vs `TERM_BRIDGE`'s 2), so the
  hardcoded entry was strictly redundant once `user_note_v2` seeding began (both fired and
  deduped, same effective output). The other 4 triggers (`할부판매`, `현재가치 할인`,
  `측정기준일`, `재측정요소`) were migrated 1:1 to new seed rows anchored at a representative
  paragraph (1115-60/61, 1102-16, 1019-8) with identical `expansion` term lists.
- Out of scope: no change to the trigger/expansion *content* — this is a mechanical
  storage-location migration, not a re-evaluation of whether these bridges are still correct.

## Verification

- [x] Targeted tests: `python -m pytest tests/ -q` — 46 passed (no test depended on `TERM_BRIDGE` directly)
- [x] CLI smoke: `python scripts/seed_user_notes.py` (dry-run) confirmed exactly the 4 expected new rows before `--apply`; `python scripts/seed_user_notes.py --apply` inserted 4; `python scripts/audit_user_notes.py` — ok: True, 17 rows, 0 issues
- [x] Integrated smoke: `python scripts/engine_quality_expanded_smoke.py --format text` — ok: True; `python scripts/quality_preflight.py --format text` — ok: True; manually confirmed `expand_query()` output for all 5 former `TERM_BRIDGE` triggers matches (byte-for-byte on 4, superset on `공매도`) pre-migration output
- [x] Dirty-tree review: `git status --short` shows only `kifrs/store.py`, `scripts/seed_user_notes.py`, changeset record, ROADMAP — `data/kifrs.db` (where the 4 rows actually live) is gitignored per the K-IFRS copyright boundary, correctly untracked

## Result

- Status: completed
- Evidence: `kifrs/store.py` (`expand_query()` now delegates fully to `_user_note_expansions()`), `scripts/seed_user_notes.py` (4 new `SEEDS` entries), `python scripts/audit_user_notes.py` (17 rows, 0 issues)
- Notes: this closes CS-5, the last step in EH1 (`docs/plans/2026-07-03-engine-hardening.md`).
