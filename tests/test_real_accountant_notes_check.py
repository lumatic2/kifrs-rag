from __future__ import annotations

from scripts.real_accountant_notes_check import check_actual_notes


def _safe_notes() -> str:
    return """# Real Accountant Session Evidence

## Session Metadata

- Date: 2026-07-05
- Reviewer role: CPA reviewer
- Reviewer service-line: F-ACC
- Reviewer experience context: reviewed accounting advisory workpapers
- Session mode: async review
- Actual feedback evidence: true

## Scores

- Workflow fit (1-5): 4
- Evidence boundary clarity (1-5): 5
- Review pack usefulness (1-5): 4
- Human-review boundary clarity (1-5): 5
- Real-case PoC willingness (1-5): 3

## Top Positive

The review pack structure is understandable.

## Top Risk

Evidence requests need sharper wording.

## Missing Inputs

- approval memo existence

## Review Question Additions

- Ask whether approval memo evidence exists.

## Safe Correction Candidates

### Candidate 1

- Case id: anon-lease-poc-001
- Issue: reviewer question should mention approval memo evidence
- Severity: medium
- Suggested fix: add approval memo evidence question
- Missing evidence: approval memo existence
- Disposition: eval_seed_candidate
- Affected outputs: human_review_questions

## Boundary Confirmation

- [x] No raw contract copied
- [x] No customer/client/company identifier copied
- [x] No private filing body copied
- [x] No K-IFRS source text copied
- [x] Notes are safe to convert into queue candidates
"""


def test_check_actual_notes_accepts_filled_public_safe_notes(tmp_path) -> None:
    path = tmp_path / "actual-feedback-notes.md"
    path.write_text(_safe_notes(), encoding="utf-8")

    ok, errors = check_actual_notes(path)

    assert ok is True
    assert errors == []


def test_check_actual_notes_rejects_template_placeholders(tmp_path) -> None:
    path = tmp_path / "actual-feedback-notes.md"
    path.write_text(
        """# Real Accountant Session Evidence Template

## Session Metadata

- Date:
- Reviewer role:
- Reviewer service-line:
- Reviewer experience context:
- Session mode: screen share / in-person / async review
- Actual feedback evidence: false until completed

## Scores

- Workflow fit (1-5):

## Top Positive
## Top Risk
## Missing Inputs
## Safe Correction Candidates
## Boundary Confirmation

- [ ] No raw contract copied
""",
        encoding="utf-8",
    )

    ok, errors = check_actual_notes(path)

    assert ok is False
    assert "empty metadata field: - Date:" in errors
    assert "actual feedback evidence marker still false" in errors
    assert any(error.startswith("boundary checkbox not confirmed") for error in errors)


def test_check_actual_notes_rejects_protected_markers(tmp_path) -> None:
    path = tmp_path / "actual-feedback-notes.md"
    path.write_text(_safe_notes() + "\ncustomer_name\n123-45-67890\n", encoding="utf-8")

    ok, errors = check_actual_notes(path)

    assert ok is False
    assert "protected marker found: customer_name" in errors
    assert "possible protected identifier found: business_registration_number" in errors
