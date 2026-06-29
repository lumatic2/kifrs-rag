# Changeset — authority source pack

## Target

- ROADMAP milestone: `EQ2`
- Plan: `docs/plans/2026-06-30-engine-quality-loop-expanded.md`

## Scope

- Files: authority registry/schema validation, metadata-only source additions, tests.
- Reason: EQ1 has a sample registry; operational use needs source-pack metadata and validation.
- Expected effect: external/supporting authority candidates can be curated without source-body commits.

## Contract

- Metadata only. No legal/KASB/FSS body text is committed.
- K-IFRS paragraph DB remains primary evidence.
- External authority types must be explicit.

## Verification

- [x] Targeted tests: `python -m pytest tests\test_authority.py -q`
- [x] CLI smoke: `python scripts\validate_authority_sources.py`; `python scripts\authority_index_smoke.py --query "금융감독원 질의회신 수익"`
- [x] Integrated smoke: `python scripts\engine_quality_expanded_smoke.py --format text`
- [x] Dirty-tree review: `docs/authority/sources.json` stores metadata only.

## Result

- Status: completed.
- Evidence: registry validates with `total=6`; FSS query returns `fss-accounting-inquiry`.
- Notes: source pack includes K-IFRS primary, 상법, 금융감독원, KASB guidance, tax boundary, exam convention metadata.
