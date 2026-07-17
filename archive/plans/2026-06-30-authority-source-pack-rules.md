# Authority Source Pack Rules Plan

> Created: 2026-06-30
> Horizon: `docs/horizons/engine-quality-ops.md`
> ROADMAP target: `EQ3`
> Success criteria: D(Authority boundaries), E(Public/private boundary)
> Harness branch: tooling

## Scope

Turn authority source categories into a public-safe source pack model: document/link metadata only, no source body text, explicit ranking and usage boundaries.

## Planning gate

```yaml
planning_gate:
  team_validation_mode: manual-pass
  spec_delta: "Promote existing EQ3 candidate as the active bounded milestone under Engine Quality Ops."
  perspectives:
    product: "Answers can know when evidence is primary K-IFRS versus supporting law, regulator, KASB, tax boundary, or exam convention."
    architecture: "Keep category registry separate from document-level source pack; link metadata is validated independently from source selection."
    security: "Forbid source body fields and protected K-IFRS/dogfood payloads in the public repo."
    qa: "Validator and tests prove required fields, allowed source ids, priority/use rules, and body-field bans."
    skeptic: "Avoid pretending metadata is retrieval; this only defines safe collection and ranking boundaries."
  dod:
    - "source pack rules document"
    - "document-level metadata-only source pack"
    - "validator CLI for source pack"
    - "focused pytest + authority smoke pass"
```

## Step

- [x] CS8 — authority source pack rules
  - Verify: `python -m pytest tests\test_authority.py tests\test_authority_source_pack.py -q`
  - Verify: `python scripts\validate_authority_sources.py`
  - Verify: `python scripts\validate_authority_source_pack.py`
  - Verify: `python scripts\authority_index_smoke.py --query "금융감독원 질의회신 수익"`
  - Output: metadata/link-only source pack, usage rules, validator.

## Stop Points

- Stop before committing K-IFRS source text, external document body text, DB dumps, embeddings, or dogfood source questions.
- Stop before treating external authority as equal to K-IFRS primary standards.
- Stop if a source pack item lacks an allowed source id, use case, URL/locator, or priority.

## Results

- Source pack rules: `docs/authority/source_pack_rules.md` defines primary/supporting/boundary/convention use cases, ranking, required fields, and forbidden body fields.
- Source pack metadata: `docs/authority/source_pack.json` contains 6 document-level metadata/link-only items mapped to the 6 authority source categories.
- Validator: `scripts/validate_authority_source_pack.py` enforces known `source_id`, matching `authority_type`, allowed use cases, required locator/keywords, `body_text_committed=false`, and forbidden body-field rejection.
- Search: `search_source_pack("금융감독원 질의회신 수익")` returns `fss-accounting-inquiry-index` with `allowed_use=supporting_interpretation`.
- Verification: targeted authority pytest 8 passed; expanded focused pytest 18 passed; `validate_authority_sources.py` ok; `validate_authority_source_pack.py` ok; `engine_quality_expanded_smoke.py --format text` ok.
