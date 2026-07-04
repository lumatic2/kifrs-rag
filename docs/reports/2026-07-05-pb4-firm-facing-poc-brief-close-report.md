# PB4 Close Report: Firm-Facing PoC Brief

> Date: 2026-07-05
> Horizon: `firm-facing-poc-brief`
> Status: closed

## What Changed

This horizon converted the previous "next recommended horizon" into a concrete accounting-firm-facing PoC package.
The package explains what the product is, which accounting-firm team it targets first, what can be demonstrated today,
what remains under human review, and what a first PoC should ask from a firm or reviewer.

## Deliverables

| Milestone | Deliverable | Status |
|---|---|---|
| PB1 | `docs/horizons/firm-facing-poc-brief.md`, `phases/firm-facing-poc-brief/*` | completed |
| PB2 | `docs/reports/firm-facing-poc/2026-07-05-poc-brief.md` | completed |
| PB3 | `docs/reports/firm-facing-poc/2026-07-05-one-page-brief.md`, `docs/reports/firm-facing-poc/INDEX.md` | completed |
| PB4 | close report and ROADMAP/OBJECTIVE sync | completed |

## Product Position

The package positions the toolkit as a local accounting intelligence system for K-IFRS decision-prep drafts.
The first target is F-ACC(Accounting Advisory / F-S support): review memo, journal entry candidate, statement candidate,
and disclosure candidate preparation. F-AUD is a secondary support surface for accounting issue review and disclosure
requirement tie-out. Tax remains out of scope for this repo and belongs to `tax-agent`.

## Verification

```powershell
python scripts\toolkit_readiness.py --manifest docs\toolkit\readiness_manifest.json --out docs\reports\2026-07-05-tk3-toolkit-readiness-report.md
```

Result: `ok: True`

```powershell
python scripts\quality_preflight.py --format text
```

Result:

- `ok: True`
- `public_safe: True`
- `protected_assets_required: False`

```powershell
git diff --check
```

Result: exit 0. Output only reported LF to CRLF working-copy warnings for `ROADMAP.md`, `docs/OBJECTIVE.md`,
and `phases/index.json`.

```powershell
rg -n "F-ACC|F-AUD|PoC Ask|Risk Boundary|PoC 요청사항|30분 데모|10분 소개" docs\reports\firm-facing-poc -S
```

Result: required sections found in the firm-facing PoC package.

## Boundary Check

The firm-facing PoC package states that protected assets are excluded:

- K-IFRS source text
- parsed DB
- embeddings
- dogfood questions
- customer/client data
- raw filing body

The package requests only an anonymized transaction card, one accountant reviewer, and three evaluation criteria.

## Next Recommended Horizon

`real-anonymized-transaction-poc`

Reason: the firm-facing brief is now present, but the strongest next proof is not more packaging. The next proof is
one anonymized F-ACC transaction turned into a review pack with reviewer corrections feeding the eval/backlog queue.
