from __future__ import annotations

from kifrs.feedback import (
    LocalPrivateCaseIntake,
    render_local_private_intake_card,
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
