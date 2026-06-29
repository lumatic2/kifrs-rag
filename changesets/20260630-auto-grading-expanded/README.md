# Changeset — automatic grading expanded

## Target

- ROADMAP milestone: `EQ2`
- Plan: `docs/plans/2026-06-30-engine-quality-loop-expanded.md`

## Scope

- Files: eval gate module/script, tests, integrated smoke.
- Reason: EQ1 local-rag can score a few items, but there is no pass/fail gate or broader target set.
- Expected effect: local grading can be used as a regression gate.

## Contract

- No network or paid API required.
- Existing `kifrs.eval.harness` remains compatible.
- Generated reports stay under ignored `data/eval/results/`.

## Verification

- [x] Targeted tests: `python -m pytest tests\test_eval_gates.py tests\test_local_rag_runner.py -q`
- [x] CLI smoke: `python scripts\eval_quality_gate.py --runner local-rag --only Q019 Q020 Q021 Q022 Q023 --min-composite 0.6 --min-cite 0.45 --format text`
- [x] Integrated smoke: `python scripts\engine_quality_expanded_smoke.py --format text`
- [x] Dirty-tree review: generated eval reports remain under ignored `data/eval/results/`.

## Result

- Status: completed.
- Evidence: gate passed with mean composite `0.921`, mean cite `0.763`, mean global rules `1.0`, failing items `0`.
- Notes: `local-rag` uses gold-anchor fallback for no-network scorer/report regression, not retrieval benchmarking.
