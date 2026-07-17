# Engine Quality Ops Horizon

> Created: 2026-06-30
> ROADMAP goal id: `engine-quality-ops`
> Status: completed through EQ1/EQ2/EQ3/EQ4/EQ5

## Why now

Phase 4 completed content dogfooding across 1115 revenue, 1116 leases, 1113 fair value, and 1019 employee benefits. The repeated pattern is now clear:

- answers need automated regression checks, not only manual review;
- K-IFRS sometimes needs non-standard external authority boundaries;
- `user_note` is becoming a runtime quality layer, not just ad hoc memory.

This horizon turns those three lessons into operating infrastructure.

## Goal

Build an operating loop where RAG answers can be evaluated, supplemented by authority-aware evidence, and improved by typed user notes with measurable quality checks.

## Direction and success criteria

The high-level direction and stop criteria are maintained in:

- `docs/plans/2026-06-30-kifrs-direction-success-criteria.md`

New work under this horizon should name which success criterion it is closing before implementation starts.

## Milestone

### EQ1 — RAG quality operating loop

Scope:

1. Automatic grading
2. External authority index
3. user_note operating quality

Close criteria:

- [x] a local command can run a targeted answer-quality evaluation without requiring new source data to be committed;
- [x] a local authority index can distinguish K-IFRS primary evidence from external/supporting authority;
- [x] user notes can be audited, surfaced, and checked for conflicts or dead anchors;
- [x] an integrated smoke proves all three surfaces can be used together.

### EQ2 — Expanded quality loop

Scope:

1. Automatic grading threshold gate
2. Metadata-only authority source pack
3. Backward-compatible user_note schema v2 migration

Close criteria:

- [x] a local quality gate can fail/pass selected goldset items by threshold;
- [x] authority registry validates required fields and forbids source-body fields;
- [x] user_note v2 projection can be dry-run, applied, and re-run idempotently;
- [x] expanded integrated smoke proves all three surfaces together.

### EQ4 — user_note v2 runtime layer

Scope:

1. v2-priority user note write path
2. v2-priority query expansion and answer-time lookup
3. Legacy fallback and non-destructive compatibility

Close criteria:

- [x] new seed/write path stores typed v2 rows with a legacy mirror;
- [x] query expansion and `get_user_notes()` prefer v2 rows and fallback to legacy when v2 is empty;
- [x] v2 audit validates active typed rows;
- [x] focused pytest and integrated smoke pass.

### EQ3 — authority source pack rules

Scope:

1. document-level authority metadata model
2. source-pack collection and usage rules
3. public-safe validator for source-pack items

Close criteria:

- [x] source pack rules define primary/supporting/boundary/convention use cases;
- [x] source pack stores metadata and locators only;
- [x] validator rejects unknown sources, invalid use cases, and forbidden body fields;
- [x] focused pytest and expanded integrated smoke pass.

### EQ5 — quality preflight and CI hook

Scope:

1. public-safe local quality preflight command
2. local-rag threshold gate inside preflight
3. GitHub Actions workflow template using the same command

Close criteria:

- [x] one local command runs focused tests, threshold gate, authority validators, and v2 user-note audit;
- [x] CI workflow template invokes the same command;
- [x] preflight does not require protected local assets, source bodies, API keys, or network access;
- [x] focused pytest, preflight smoke, and expanded integrated smoke pass.

## Candidate order

No candidate is active now. Engine Quality Ops is complete at the current scope.

Next work should be a new bounded horizon or a deliberate return to Phase 4 scenario expansion.

## Out of scope

- Uploading or committing K-IFRS source text, dogfood source questions, PDFs, DB dumps, or embeddings.
- Building a full legal search product.
- Depending on external API credentials for the core smoke.
- Treating external authority as equal to K-IFRS primary standards without explicit type/priority metadata.
