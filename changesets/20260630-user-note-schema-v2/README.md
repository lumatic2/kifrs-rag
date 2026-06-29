# Changeset — user_note schema v2

## Target

- ROADMAP milestone: `EQ2`
- Plan: `docs/plans/2026-06-30-engine-quality-loop-expanded.md`

## Scope

- Files: additive SQLite table schema, migration script, v2 audit path, tests.
- Reason: string-only notes are backward-compatible but weak for operation as note count grows.
- Expected effect: typed v2 rows can be used without breaking existing string notes.

## Contract

- Migration is additive and idempotent.
- Existing `user_note` rows are never deleted or mutated.
- Existing `expand_query` and `get_user_notes` behavior remains valid.

## Verification

- [x] Targeted tests: `python -m pytest tests\test_user_note_v2_migration.py tests\test_user_notes.py -q`
- [x] CLI smoke: `python scripts\migrate_user_notes_v2.py --format text`; `python scripts\migrate_user_notes_v2.py --apply --format text`; `python scripts\migrate_user_notes_v2.py --format text`
- [x] Integrated smoke: `python scripts\engine_quality_expanded_smoke.py --format text`
- [x] Dirty-tree review: migration is additive; existing `user_note` rows are not mutated.

## Result

- Status: completed.
- Evidence: dry-run planned 13 ready rows, apply inserted 13, subsequent dry-run planned 0.
- Notes: `user_note_v2` is a typed projection with `legacy_id` uniqueness and fallback-compatible legacy table retained.
