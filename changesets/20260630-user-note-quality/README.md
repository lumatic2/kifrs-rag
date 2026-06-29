# Changeset — user_note operating quality

## Target

- ROADMAP milestone: `EQ1`
- Plan: `docs/plans/2026-06-30-engine-quality-ops.md`

## Scope

- Files:
  - `kifrs/store.py`
  - new `kifrs/user_notes.py` or equivalent helper
  - new `scripts/audit_user_notes.py`
  - tests for parsing/audit behavior
- Reason: `user_note` is now used at search time and answer time. It needs typed parsing, anchor validation, and conflict/dead-note checks.
- Expected effect: user notes become inspectable operating data instead of opaque strings.

## Contract

- Source of truth: SQLite `user_note` table plus git-safe seed script/preview docs.
- Compatibility: existing `type=...; trigger=...; expansion=...` note strings remain valid.
- Out of scope: changing DB schema unless strictly necessary.

## Verification

- [x] Targeted tests: `python -m pytest tests\test_user_notes.py -q`
- [x] CLI smoke: `python scripts\audit_user_notes.py --format json`
- [x] Integrated smoke: `python scripts\engine_quality_smoke.py --format text`
- [x] Dirty-tree review: protected data remains under ignored `data/`; new committed surfaces are code/metadata/docs only.

## Result

- Status: completed.
- Evidence: audit returned `total=13`, `ok=true`, with no missing required fields, invalid types, dead anchors, or conflicts.
- Notes: parser remains backward-compatible with existing semicolon-delimited note strings.
