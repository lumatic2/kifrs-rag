# Engine Quality Ops Plan

> Created: 2026-06-30
> Horizon: `docs/horizons/engine-quality-ops.md`
> ROADMAP target: `EQ1`
> Harness branch: tooling

## Scope

Implement the three next engine-quality candidates as three tooling changesets:

- automatic grading
- external authority index
- user_note operating quality

The run closes when each changeset has its own targeted verification and the combined smoke shows the three surfaces working together.

## Planning gate

```yaml
planning_gate:
  team_validation_mode: manual-pass
  spec_delta: "Add new ROADMAP horizon engine-quality-ops and active milestone EQ1 with three tooling changesets."
  perspectives:
    product: "Turns Phase 4 dogfood artifacts into a repeatable quality loop for the personal AI accountant."
    architecture: "Keep K-IFRS primary DB separate from external authority and user-authored notes; expose each through explicit local APIs/scripts."
    security: "No source PDF/text/DB dump/dogfood content is committed. No external credential is required for the first smoke."
    qa: "Each changeset gets focused CLI/tests plus one integrated smoke command."
    skeptic: "The risk is overbuilding; keep each changeset to a local minimum viable loop and defer full automation."
  dod:
    - "pytest tests focused on new scoring/user_note/authority behavior"
    - "CLI smoke for each changeset"
    - "integrated local smoke proving grading + authority + user_note surfaces"
```

## Step tree

- [x] CS1 — user_note operating quality
  - Verify: `python scripts/audit_user_notes.py --format json` and focused tests.
  - Output: typed note parsing/audit, dead-anchor/conflict checks, answer-time note smoke.

- [x] CS2 — automatic grading
  - Verify: `python -m kifrs.eval.harness --runner local-rag --only Q019 Q020 Q021 --quiet` or equivalent no-network runner smoke.
  - Output: deterministic local runner or grading command that scores citations/keywords/global rules without requiring Claude API.

- [x] CS3 — external authority index
  - Verify: `python scripts/authority_index_smoke.py --query "상법 자본거래"` and focused tests.
  - Output: minimal local authority source registry/index with authority type, priority, citation id, and no copyrighted source body committed.

- [x] Integrated smoke
  - Verify: one command or script runs user_note audit, local grading sample, and authority query sample together.
  - Output: result JSON/markdown under `data/eval/results/` or a git-safe docs/evidence file without protected source text.

## Changesets

| Changeset | Scope | Status |
|---|---|---|
| `20260630-user-note-quality` | user_note parser/audit/smoke | completed |
| `20260630-auto-grading` | deterministic local grading loop | completed |
| `20260630-authority-index` | external authority registry/index | completed |

## Results

- user_note audit: 13 rows, `ok=true`, no missing required fields, invalid types, dead anchors, or conflicts.
- automatic grading: `local-rag` no-network runner over Q019-Q021 completed, composite average `0.783`.
- authority index: metadata-only registry returns `commercial-act-capital` for `상법 자본거래 무상증자`.
- integrated smoke: `python scripts/engine_quality_smoke.py --format text` returned `ok: True`.

## Stop points

- Stop if a step requires committing protected standards/dogfood text.
- Stop if authority source ingestion requires unclear copyright treatment.
- Stop if automatic grading requires paid API credentials for the baseline smoke.
