from __future__ import annotations

import pytest

from kifrs.feedback import CaseIntake, ReviewerCorrection
from kifrs.feedback.transaction_poc import (
    build_transaction_poc_package,
    case_to_lease1116,
    render_anonymized_input_card,
)


def _case() -> CaseIntake:
    return CaseIntake(
        case_id="anon-lease-poc-001",
        domain_hint="KIFRS1116",
        anonymized_title="Anonymized office lease",
        fact_pattern_summary="Sanitized office lease facts prepared as a structured PoC card.",
        structured_facts={
            "party": "lessee",
            "lease_term": "4 years",
            "payment_schedule": "annual arrears",
            "lease_term_years": 4,
            "annual_payment": 1_000_000,
            "discount_rate": 0.05,
            "annuity_factor": 3.54595,
            "payment_timing": "arrears",
        },
        requested_outputs=[
            "review_pack",
            "journal_entry_draft",
            "disclosure_questions",
            "human_review_questions",
        ],
        source_boundaries=[
            "contract clauses are summarized into structured facts",
            "reviewer checks original documents outside this repo",
        ],
        reviewer_questions=["Does the lease term evidence support four years?"],
    )


def _correction() -> ReviewerCorrection:
    return ReviewerCorrection(
        case_id="anon-lease-poc-001",
        issue="Lease term evidence question should be explicit",
        severity="medium",
        suggested_fix="Add a required reviewer question for lease term evidence.",
        missing_evidence=["lease term approval evidence"],
        disposition="eval_seed_candidate",
        affected_outputs=["human_review_questions", "review_pack"],
    )


def test_case_to_lease1116_maps_public_safe_card_to_engine_input() -> None:
    lease = case_to_lease1116(_case())

    assert lease.label == "anon-lease-poc-001"
    assert lease.party == "lessee"
    assert lease.annual_payment == 1_000_000
    assert lease.lease_term_years == 4
    assert lease.annuity_factor == 3.54595


def test_build_transaction_poc_package_generates_review_pack_and_queue_record() -> None:
    package = build_transaction_poc_package(_case(), _correction())

    assert package.review_pack.status == "automated"
    assert "F-ACC Review Pack" in package.review_pack_markdown
    assert "anon-lease-poc-001" in package.input_card_markdown
    assert package.queue_record.disposition == "candidate"
    assert package.queue_record.route == "kifrs1116_review_pack"
    assert "Eval seed candidates: 1" in package.queue_report_markdown


def test_transaction_poc_rejects_missing_numeric_facts() -> None:
    case = _case()
    facts = dict(case.structured_facts)
    facts.pop("annuity_factor")
    bad = CaseIntake(**{**case.to_dict(), "structured_facts": facts})

    with pytest.raises(ValueError, match="annuity_factor"):
        case_to_lease1116(bad)


def test_transaction_poc_rejects_protected_fields_before_review_pack() -> None:
    case = _case()
    facts = dict(case.structured_facts)
    facts["raw_contract"] = "copied"
    bad = CaseIntake(**{**case.to_dict(), "structured_facts": facts})

    with pytest.raises(ValueError, match="protected-data"):
        case_to_lease1116(bad)


def test_anonymized_input_card_preserves_boundary() -> None:
    rendered = render_anonymized_input_card(_case())

    assert "Structured Facts" in rendered
    assert "copied contract text" in rendered
    assert "customer identifiers" in rendered
    assert "raw_contract" not in rendered
