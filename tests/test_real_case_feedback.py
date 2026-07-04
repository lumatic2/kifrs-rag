from __future__ import annotations

import pytest

from kifrs.feedback import (
    CaseIntake,
    ReviewerCorrection,
    case_to_eval_seed_candidate,
    render_feedback_summary_markdown,
    route_case,
    validate_case_intake,
    validate_reviewer_correction,
)


def _case(domain: str = "KIFRS1116") -> CaseIntake:
    return CaseIntake(
        case_id="anon-case-001",
        domain_hint=domain,
        anonymized_title="Anonymized office lease modification",
        fact_pattern_summary="Sanitized lease facts with no customer identifiers or source body.",
        structured_facts={
            "party": "lessee",
            "lease_term": "4 years",
            "payment_schedule": "annual arrears",
        },
        requested_outputs=["review_pack", "journal_entry_draft", "human_review_questions"],
        source_boundaries=["contract clause references are summarized, not copied"],
        reviewer_questions=["Is the modification path supportable?"],
    )


def test_case_intake_accepts_public_safe_structured_case() -> None:
    issues = validate_case_intake(_case())

    assert issues == []


def test_case_intake_rejects_raw_payload_and_customer_identifier() -> None:
    case = CaseIntake(
        case_id="bad",
        domain_hint="KIFRS1115",
        anonymized_title="Bad case",
        fact_pattern_summary="Customer identifier 123-45-67890 is present.",
        structured_facts={"contract_body": "raw copied body"},
        requested_outputs=["review_pack"],
    )

    issues = validate_case_intake(case)

    assert any(issue.path == "structured_facts.contract_body" for issue in issues)
    assert any(issue.message == "possible customer identifier" for issue in issues)


def test_route_case_returns_supported_candidate_when_minimum_facts_exist() -> None:
    route = route_case(_case())

    assert route.status == "candidate"
    assert route.domain == "KIFRS1116"
    assert route.route == "kifrs1116_review_pack"
    assert route.missing_facts == []


def test_route_case_reports_missing_facts_without_running_judgment_engine() -> None:
    case = CaseIntake(
        case_id="anon-case-002",
        domain_hint="KIFRS1109",
        anonymized_title="Anonymized debt instrument",
        fact_pattern_summary="Sanitized financial instrument facts.",
        structured_facts={"instrument_type": "debt"},
        requested_outputs=["review_pack"],
    )

    route = route_case(case)

    assert route.status == "needs_more_facts"
    assert route.route == "kifrs1109_review_pack"
    assert route.missing_facts == ["business_model", "cash_flow_terms"]


def test_route_case_keeps_tax_out_of_scope() -> None:
    case = _case(domain="TAX")

    route = route_case(case)

    assert route.status == "unsupported"
    assert route.route == "out_of_scope"


def test_reviewer_correction_validates_and_converts_to_eval_seed_candidate() -> None:
    correction = ReviewerCorrection(
        case_id="anon-case-001",
        issue="Lease term reassessment question is underspecified",
        severity="medium",
        suggested_fix="Add a review question about reasonably certain renewal evidence.",
        missing_evidence=["management renewal assessment"],
        disposition="eval_seed_candidate",
        affected_outputs=["human_review_questions"],
    )

    assert validate_reviewer_correction(correction) == []
    seed = case_to_eval_seed_candidate(_case(), correction)

    assert seed["case_id"] == "anon-case-001"
    assert seed["status"] == "candidate"
    assert seed["route"] == "kifrs1116_review_pack"


def test_reviewer_correction_rejects_raw_source_body() -> None:
    correction = ReviewerCorrection(
        case_id="anon-case-001",
        issue="bad",
        severity="high",
        suggested_fix="Remove copied source.",
        missing_evidence=["source_body"],
        disposition="backlog_candidate",
    )

    issues = validate_reviewer_correction(correction)

    assert any(issue.path == "missing_evidence[0]" for issue in issues)


def test_feedback_summary_markdown_preserves_boundaries() -> None:
    correction = ReviewerCorrection(
        case_id="anon-case-001",
        issue="Add missing disclosure question",
        severity="low",
        suggested_fix="Ask reviewer to confirm variable lease payment disclosure.",
        disposition="backlog_candidate",
    )

    rendered = render_feedback_summary_markdown(_case(), correction)

    assert "Real Case Feedback Summary" in rendered
    assert "kifrs1116_review_pack" in rendered
    assert "does not store raw contracts" in rendered
    assert "source_body" not in rendered


def test_eval_seed_candidate_requires_matching_case_id() -> None:
    correction = ReviewerCorrection(
        case_id="other-case",
        issue="Mismatch",
        severity="low",
        suggested_fix="Use same case id.",
    )

    with pytest.raises(ValueError, match="same case_id"):
        case_to_eval_seed_candidate(_case(), correction)
