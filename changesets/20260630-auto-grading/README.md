# Changeset — automatic grading

## Target

- ROADMAP milestone: `EQ1`
- Plan: `docs/plans/2026-06-30-engine-quality-ops.md`

## Scope

- Files:
  - `kifrs/eval/runners.py`
  - `kifrs/eval/harness.py`
  - tests for deterministic local grading
  - optional smoke script under `scripts/`
- Reason: current manual dogfood needs a repeatable no-network scoring path.
- Expected effect: a local command can score selected goldset items for citation/keyword/global-rule quality.

## Contract

- Source of truth: existing `data/eval/goldset.json` and scorer code.
- Compatibility: existing API-backed runners stay unchanged.
- Out of scope: judging free-form numeric accounting answers with a paid LLM.

## Verification

- [x] Targeted tests: `python -m pytest tests\test_local_rag_runner.py tests\test_scorers.py -q`
- [x] CLI smoke: `python -m kifrs.eval.harness --runner local-rag --only Q019 Q020 Q021 --quiet`
- [x] Integrated smoke: `python scripts\engine_quality_smoke.py --format text`
- [x] Dirty-tree review: generated eval reports are under ignored `data/eval/results/`.

## Result

- Status: completed.
- Evidence: local-rag Q019-Q021 smoke completed with composite average `0.783`.
- Notes: `local-rag` is deterministic and no-network; it is a grading/smoke runner, not a production answer model.
