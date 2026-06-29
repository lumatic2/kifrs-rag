# Changeset — external authority index

## Target

- ROADMAP milestone: `EQ1`
- Plan: `docs/plans/2026-06-30-engine-quality-ops.md`

## Scope

- Files:
  - new authority registry/index module or data file with metadata only
  - new smoke script
  - tests for authority lookup/priority behavior
- Reason: some accounting answers need a clear boundary between K-IFRS primary evidence and external/supporting authority.
- Expected effect: the system can say "K-IFRS primary source did not cover this; supporting authority candidate is X" without mixing evidence tiers.

## Contract

- Source of truth: git-safe metadata registry only; no copyrighted source body.
- Compatibility: K-IFRS paragraph DB remains primary.
- Out of scope: full external document ingestion, web crawling, or legal advice.

## Verification

- [x] Targeted tests: `python -m pytest tests\test_authority.py -q`
- [x] CLI smoke: `python scripts\authority_index_smoke.py --query "상법 자본거래 무상증자"`
- [x] Integrated smoke: `python scripts\engine_quality_smoke.py --format text`
- [x] Dirty-tree review: registry stores metadata only, no third-party source body.

## Result

- Status: completed.
- Evidence: query `상법 자본거래 무상증자` returned `commercial-act-capital` as `external_law`.
- Notes: K-IFRS DB remains primary evidence; external authority is supporting metadata.
