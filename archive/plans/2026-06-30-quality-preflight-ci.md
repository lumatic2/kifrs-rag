# Quality Preflight CI Plan

> Created: 2026-06-30
> Horizon: `docs/horizons/engine-quality-ops.md`
> ROADMAP target: `EQ5`
> Success criteria: B(Repeatable evaluation), E(Public/private boundary)
> Harness branch: tooling

## Scope

Create one public-safe quality preflight entrypoint and wire it to CI. The gate must not require protected K-IFRS PDFs, parsed text, embeddings, DB dumps, dogfood source questions, or external API credentials.

## Planning gate

```yaml
planning_gate:
  team_validation_mode: manual-pass
  spec_delta: "Promote existing EQ5 candidate as the active bounded milestone under Engine Quality Ops."
  perspectives:
    product: "Quality can be checked by one command before continuing scenario or engine work."
    architecture: "Reuse existing focused tests, local-rag threshold gate, authority validators, and user_note audit instead of creating another scoring layer."
    security: "CI/preflight must remain public-safe and must not depend on ignored protected source data."
    qa: "Preflight exits non-zero on failing thresholds or validators and is covered by a smoke test."
    skeptic: "Avoid broad noisy CI; keep the initial hook focused on stable no-network checks."
  dod:
    - "one local preflight command"
    - "CI workflow template invokes the same command"
    - "preflight includes threshold gate and metadata validators"
    - "focused pytest + preflight smoke pass"
```

## Step

- [x] CS9 — quality preflight and CI hook
  - Verify: `python -m pytest tests\test_quality_preflight.py tests\test_eval_gates.py tests\test_authority_source_pack.py -q`
  - Verify: `python scripts\quality_preflight.py --format text`
  - Verify: `python scripts\engine_quality_expanded_smoke.py --format text`
  - Output: local preflight entrypoint and CI workflow template with public-safe quality gate.

## Stop Points

- Stop before adding a CI step that needs local protected data.
- Stop before requiring API keys or network access for the core gate.
- Stop if threshold values are changed without recording them in this plan or changeset.

## Results

- Preflight command: `scripts/quality_preflight.py --format text` runs focused tests, `local-rag` threshold gate, authority registry validation, authority source-pack validation, and v2 user-note audit.
- CI template: `docs/ci/quality.yml` installs `.[eval]` and runs the same preflight command on push/PR when copied into `.github/workflows/`.
- Public boundary: preflight reports `public_safe=True` and `protected_assets_required=False`; it does not require protected PDFs, parsed text, embeddings, DB dumps, dogfood source questions, API keys, or network access.
- Verification: targeted pytest 8 passed; `quality_preflight.py --format text` returned ok; `engine_quality_expanded_smoke.py --format text` returned ok.
