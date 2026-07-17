# Engine Quality Loop Expanded Plan

> Created: 2026-06-30
> Horizon: `docs/horizons/engine-quality-ops.md`
> ROADMAP target: `EQ2`
> Harness branch: tooling

## Scope

Expand the initial EQ1 quality loop into a more operational loop:

- EQ2a: automatic grading threshold gate
- EQ2b: metadata-only authority source pack
- EQ2c: backward-compatible user_note schema v2 migration

## Planning gate

```yaml
planning_gate:
  team_validation_mode: manual-pass
  spec_delta: "Promote EQ2 as active milestone under engine-quality-ops and implement three tooling changesets."
  perspectives:
    product: "Makes RAG quality measurable, authority-aware, and maintainable as notes/sources grow."
    architecture: "Keep compatibility with existing user_note strings and EQ1 local-rag runner while adding structured gates/source metadata."
    security: "No protected DB/PDF/dogfood/source body committed; authority source pack remains metadata-only."
    qa: "Each changeset has focused tests and CLI smoke; final integrated smoke covers all three."
    skeptic: "Avoid irreversible DB migration; implement v2 as additive table/projection with rollback-safe dry-run/apply."
  dod:
    - "threshold gate CLI for local-rag"
    - "authority source validation CLI"
    - "user_note v2 migration dry-run/apply/idempotency smoke"
    - "focused pytest + integrated smoke"
```

## Step tree

- [x] CS4 — automatic grading expanded
  - Verify: `python scripts/eval_quality_gate.py --runner local-rag --only Q019 Q020 Q021 Q022 Q023 --min-composite 0.6 --min-cite 0.45`
  - Output: threshold gate JSON with pass/fail and report paths.

- [x] CS5 — authority source pack
  - Verify: `python scripts/validate_authority_sources.py` and `python scripts/authority_index_smoke.py --query "금융감독원 질의회신 수익"`
  - Output: expanded metadata-only source registry with schema validation.

- [x] CS6 — user_note schema v2
  - Verify: `python scripts/migrate_user_notes_v2.py --dry-run`, `--apply`, then dry-run idempotency.
  - Output: additive `user_note_v2` table/projection, migration script, v2 audit path.

- [x] Integrated smoke
  - Verify: `python scripts/engine_quality_expanded_smoke.py --format text`
  - Output: combined pass over threshold gate, source validation, v2 migration dry-run.

## Stop points

- Stop if migration would delete or mutate existing `user_note` rows.
- Stop if authority source expansion needs committed third-party body text.
- Stop if threshold gate requires paid model/API credentials.

## Results

- Automatic grading gate: passed over Q019-Q023 with mean composite `0.921`, mean cite `0.763`, mean global rules `1.0`.
- Authority source pack: registry validates with 6 metadata-only sources; `금융감독원 질의회신 수익` returns `fss-accounting-inquiry`.
- user_note schema v2: dry-run 13 ready rows, apply inserted 13, idempotent dry-run planned 0.
- Integrated smoke: `python scripts/engine_quality_expanded_smoke.py --format text` returned `ok: True`.
