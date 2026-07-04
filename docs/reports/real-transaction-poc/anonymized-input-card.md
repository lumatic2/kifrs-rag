# Anonymized Transaction Input Card - anon-lease-poc-001

- Domain: KIFRS1116
- Route: kifrs1116_review_pack
- Route status: candidate
- Title: Anonymized office lease
- Summary: Sanitized office lease facts prepared as a structured PoC card.

## Structured Facts

| Field | Value |
|---|---|
| annual_payment | 1000000 |
| annuity_factor | 3.54595 |
| discount_rate | 0.05 |
| lease_term | 4 years |
| lease_term_years | 4 |
| party | lessee |
| payment_schedule | annual arrears |
| payment_timing | arrears |

## Requested Outputs

- review_pack
- journal_entry_draft
- disclosure_questions
- human_review_questions

## Source Boundary

- contract clauses are summarized into structured facts
- reviewer checks original documents outside this repo

## Reviewer Questions

- Does the lease term evidence support four years?
- Are there variable lease payments or extension options outside the structured card?

## Boundary

- This card stores structured facts only.
- It does not store copied contract text, customer identifiers, private filings, parsed standards, embeddings, or workpaper payloads.
