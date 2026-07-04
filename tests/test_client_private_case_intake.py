from __future__ import annotations

from kifrs.feedback import (
    LocalPrivateCaseIntake,
    redact_local_private_case_for_public,
    render_local_private_intake_card,
    render_redacted_client_private_summary,
    route_redacted_client_private_summary,
    validate_local_private_case_intake,
)


def _case() -> LocalPrivateCaseIntake:
    return LocalPrivateCaseIntake(
        case_id="local-case-001",
        source_locator="local-private://cases/local-case-001/contract-summary",
        document_type="contract",
        redaction_status="reviewed_public_safe",
        allowed_output_level="review_pack_summary",
        structured_facts={
            "party": "lessee",
            "lease_term": "4 years",
            "payment_schedule": "annual arrears",
        },
        reviewer_original_document_check=True,
        notes=["Original contract remains outside repo."],
    )


def test_local_private_case_intake_accepts_reviewed_control_record() -> None:
    assert validate_local_private_case_intake(_case()) == []


def test_local_private_case_intake_rejects_raw_payload_field() -> None:
    case = LocalPrivateCaseIntake(
        **{
            **_case().to_dict(),
            "structured_facts": {"raw_contract": "copied private text"},
        }
    )

    issues = validate_local_private_case_intake(case)

    assert any(issue.path == "structured_facts.raw_contract" for issue in issues)


def test_local_private_case_intake_requires_reviewer_document_check() -> None:
    case = LocalPrivateCaseIntake(**{**_case().to_dict(), "reviewer_original_document_check": False})

    issues = validate_local_private_case_intake(case)

    assert any(issue.path == "reviewer_original_document_check" for issue in issues)


def test_local_private_case_intake_requires_redaction_before_review_summary() -> None:
    case = LocalPrivateCaseIntake(**{**_case().to_dict(), "redaction_status": "redacted"})

    issues = validate_local_private_case_intake(case)

    assert any(issue.path == "allowed_output_level" for issue in issues)


def test_render_local_private_intake_card_preserves_boundary() -> None:
    rendered = render_local_private_intake_card(_case())

    assert "Local-Only Client-Private Intake Card" in rendered
    assert "reviewed_public_safe" in rendered
    assert "raw_contract" not in rendered
    assert "customer identifiers" in rendered


def test_redact_local_private_case_removes_private_locator_and_notes() -> None:
    summary = redact_local_private_case_for_public(_case())
    data = summary.to_dict()

    assert data["case_id"] == "local-case-001"
    assert "source_locator" not in data
    assert "notes" not in data
    assert data["structured_facts"]["party"] == "lessee"


def test_redact_local_private_case_schema_only_omits_fact_values() -> None:
    case = LocalPrivateCaseIntake(**{**_case().to_dict(), "allowed_output_level": "schema_only"})

    summary = redact_local_private_case_for_public(case)

    assert summary.structured_fact_keys == ["lease_term", "party", "payment_schedule"]
    assert summary.structured_facts == {}


def test_redact_local_private_case_rejects_unreviewed_case() -> None:
    case = LocalPrivateCaseIntake(**{**_case().to_dict(), "reviewer_original_document_check": False})

    try:
        redact_local_private_case_for_public(case)
    except ValueError as exc:
        assert "reviewer_original_document_check" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_render_redacted_client_private_summary_preserves_public_boundary() -> None:
    rendered = render_redacted_client_private_summary(redact_local_private_case_for_public(_case()))

    assert "Redacted Client-Private Summary" in rendered
    assert "source locator" in rendered
    assert "local-private://cases" not in rendered
    assert "Original contract remains outside repo" not in rendered


def test_route_redacted_summary_to_1116_review_pack_candidate() -> None:
    summary = redact_local_private_case_for_public(_case())

    route = route_redacted_client_private_summary(summary, domain_hint="KIFRS1116")

    assert route.status == "candidate"
    assert route.route == "kifrs1116_review_pack"
    assert route.missing_facts == []


def test_route_redacted_summary_reports_missing_1109_facts() -> None:
    summary = redact_local_private_case_for_public(_case())

    route = route_redacted_client_private_summary(summary, domain_hint="KIFRS1109")

    assert route.status == "needs_more_facts"
    assert route.missing_facts == ["instrument_type", "business_model", "cash_flow_terms"]


def test_route_redacted_summary_blocks_schema_only_output_level() -> None:
    summary = redact_local_private_case_for_public(
        LocalPrivateCaseIntake(**{**_case().to_dict(), "allowed_output_level": "schema_only"})
    )

    route = route_redacted_client_private_summary(summary, domain_hint="KIFRS1116")

    assert route.status == "blocked"
    assert route.route == "redaction_gate"
