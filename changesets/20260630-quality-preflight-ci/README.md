# Changeset — quality preflight CI

## Target

- ROADMAP milestone: `EQ5`
- Plan: `docs/plans/2026-06-30-quality-preflight-ci.md`

## Scope

- Files:
  - `scripts/quality_preflight.py`
  - `docs/ci/quality.yml`
  - `tests/test_quality_preflight.py`
  - `scripts/engine_quality_expanded_smoke.py`
  - `README.md`
- Reason: quality gates and validators exist, but there is no single repeatable local/CI entrypoint.
- Expected effect: local users can run the public-safe quality preflight, and CI users can copy the included GitHub Actions template.

## Contract

- Source of truth: `scripts/quality_preflight.py` is the command-level gate; `docs/ci/quality.yml` is a GitHub Actions template that calls it directly.
- Compatibility: no protected source text, PDFs, DB dumps, embeddings, dogfood source questions, API credentials, or network access required for the core preflight.
- Out of scope: full 50-item eval, paid model judging, production deployment.

## Verification

- [x] Targeted tests: `python -m pytest tests\test_quality_preflight.py tests\test_eval_gates.py tests\test_authority_source_pack.py -q` → 8 passed
- [x] CLI smoke: `python scripts\quality_preflight.py --format text` → ok
- [x] Integrated smoke: `python scripts\engine_quality_expanded_smoke.py --format text` → ok
- [x] Dirty-tree review: CI/preflight does not require protected local assets.

## Result

- Status: completed
- Evidence: `scripts/quality_preflight.py`; `docs/ci/quality.yml`; `tests/test_quality_preflight.py`; `README.md`
- Notes: preflight is public-safe and the GitHub Actions template uses the same entrypoint.
