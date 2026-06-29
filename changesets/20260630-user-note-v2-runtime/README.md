# Changeset — user_note v2 runtime

## Target

- ROADMAP milestone: `EQ4`
- Plan: `docs/plans/2026-06-30-user-note-v2-runtime.md`

## Scope

- Files:
  - `kifrs/store.py`
  - `kifrs/user_notes.py`
  - `scripts/seed_user_notes.py`
  - `scripts/audit_user_notes.py`
  - `tests/test_user_note_v2_runtime.py`
- Reason: `user_note_v2` exists as a typed projection, but runtime writes/reads still prefer legacy string rows.
- Expected effect: new seed/write/read flows use typed v2 rows first while preserving legacy compatibility.

## Contract

- Source of truth: runtime user-note operations prefer `user_note_v2`; legacy `user_note` remains a compatibility mirror/fallback.
- Compatibility: existing `user_note` rows are not deleted or mutated. Legacy-only DBs still return notes.
- Out of scope: external authority source collection, CI gating, protected source body storage.

## Verification

- [x] Targeted tests: `python -m pytest tests\test_user_note_v2_runtime.py tests\test_user_notes.py tests\test_user_note_v2_migration.py -q` → 8 passed
- [x] CLI smoke: `python scripts\seed_user_notes.py --apply`; `python scripts\audit_user_notes.py --source v2 --format json` → seed idempotent, 13 v2 rows ok
- [x] Integrated smoke: `python scripts\engine_quality_expanded_smoke.py --format text` → ok
- [x] Dirty-tree review: no destructive migration, no protected source body committed.

## Result

- Status: completed
- Evidence: `tests/test_user_note_v2_runtime.py`; `scripts/seed_user_notes.py`; `scripts/audit_user_notes.py`; `scripts/engine_quality_expanded_smoke.py`
- Notes: v2 is preferred for runtime reads/writes. Legacy rows remain as a mirror/fallback.
