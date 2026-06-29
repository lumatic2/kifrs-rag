# Changeset — authority source pack rules

## Target

- ROADMAP milestone: `EQ3`
- Plan: `docs/plans/2026-06-30-authority-source-pack-rules.md`

## Scope

- Files:
  - `docs/authority/source_pack_rules.md`
  - `docs/authority/source_pack.json`
  - `kifrs/authority.py`
  - `scripts/validate_authority_source_pack.py`
  - `tests/test_authority_source_pack.py`
- Reason: authority source categories exist, but real collection needs document/link metadata rules and public-safe validation.
- Expected effect: source pack items can be collected and ranked without committing protected body text.

## Contract

- Source of truth: `docs/authority/sources.json` defines category-level authority sources; `docs/authority/source_pack.json` defines document-level metadata candidates.
- Compatibility: existing `search_authority()` behavior remains valid.
- Out of scope: downloading source bodies, indexing external document text, CI gating.

## Verification

- [x] Targeted tests: `python -m pytest tests\test_authority.py tests\test_authority_source_pack.py -q` → 8 passed
- [x] CLI smoke: `python scripts\validate_authority_sources.py`; `python scripts\validate_authority_source_pack.py` → both ok
- [x] Authority smoke: `python scripts\authority_index_smoke.py --query "금융감독원 질의회신 수익"` → FSS source hit
- [x] Dirty-tree review: no protected source body committed.

## Result

- Status: completed
- Evidence: `docs/authority/source_pack_rules.md`; `docs/authority/source_pack.json`; `scripts/validate_authority_source_pack.py`; `tests/test_authority_source_pack.py`
- Notes: source pack is metadata/link-only; validator rejects forbidden body fields.
