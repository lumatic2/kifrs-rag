# user_note v2 Runtime Plan

> Created: 2026-06-30
> Horizon: `docs/horizons/engine-quality-ops.md`
> ROADMAP target: `EQ4`
> Success criteria: C(Runtime learning), E(Public/private boundary)
> Harness branch: tooling

## Scope

Make `user_note_v2` the preferred runtime layer for new note writes and reads while preserving legacy `user_note` compatibility.

## Planning gate

```yaml
planning_gate:
  team_validation_mode: manual-pass
  spec_delta: "Promote existing EQ4 candidate as the active bounded milestone under Engine Quality Ops."
  perspectives:
    product: "Recurring RAG failures become typed runtime data instead of legacy string-only patches."
    architecture: "Prefer v2 for writes/reads, keep legacy fallback and legacy mirror for compatibility."
    security: "No protected standard text, DB dump, embedding, PDF, or dogfood source body is committed."
    qa: "Focused tests cover v2 write/read, legacy fallback, seed idempotency, and audit behavior."
    skeptic: "Avoid destructive migration; do not remove legacy reads until compatibility smoke passes."
  dod:
    - "new seed/write path stores typed v2 rows"
    - "query expansion and get_user_notes prefer v2 but fallback to legacy"
    - "audit can validate v2 source rows"
    - "focused pytest + CLI smoke pass"
```

## Step

- [x] CS7 — `user_note_v2` runtime layer
  - Verify: `python -m pytest tests\test_user_note_v2_runtime.py tests\test_user_notes.py tests\test_user_note_v2_migration.py -q`
  - Verify: `python scripts\seed_user_notes.py --apply`
  - Verify: `python scripts\audit_user_notes.py --source v2 --format json`
  - Verify: `python scripts\engine_quality_expanded_smoke.py --format text`
  - Output: v2-priority write/read path with legacy fallback and compatibility evidence.

## Stop Points

- Stop before deleting or mutating existing `user_note` rows.
- Stop if v2 reads break legacy fallback.
- Stop if protected source body text would need to be committed.

## Results

- Runtime write path: `store.add_user_note_v2()` writes typed v2 rows and mirrors to legacy rows without mutating existing legacy records.
- Runtime read path: query expansion and `get_user_notes()` prefer active v2 rows and fallback to legacy rows when v2 is empty.
- Seed path: `scripts/seed_user_notes.py --apply` is v2-idempotent; current DB reports 13 existing rows, 0 new rows.
- Audit path: `scripts/audit_user_notes.py --source v2 --format json` returns 13 rows, `ok=true`.
- Verification: focused pytest 8 passed; expanded focused pytest 16 passed; `engine_quality_expanded_smoke.py --format text` returned `ok: True`.
