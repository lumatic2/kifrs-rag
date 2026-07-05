from __future__ import annotations

from kifrs.feedback import (
    ClientPrivateDeletionAttestation,
    render_client_private_deletion_attestation,
    validate_client_private_deletion_attestation,
)
from scripts.client_private_deletion_attestation_check import (
    check_deletion_attestation,
    default_attestation,
    render_report,
)
from scripts.client_private_parser_dry_run_fixture_check import default_fixture
from scripts.client_private_upload_storage_policy_check import default_policy


def test_default_deletion_attestation_passes() -> None:
    result = check_deletion_attestation()

    assert result["ok"], result["errors"]
    assert result["attestation"]["deletion_status"] == "deleted"
    assert result["attestation"]["raw_file_present"] is False
    assert result["attestation"]["parsed_body_present"] is False
    assert result["attestation"]["ocr_text_present"] is False
    assert result["attestation"]["embedding_present"] is False


def test_deletion_attestation_rejects_raw_file_presence() -> None:
    attestation = ClientPrivateDeletionAttestation(
        **{
            **default_attestation().to_dict(),
            "raw_file_present": True,
        }
    )

    issues = validate_client_private_deletion_attestation(attestation, default_policy(), default_fixture())

    assert any(issue.path == "raw_file_present" for issue in issues)


def test_deletion_attestation_requires_deleted_before_report_write() -> None:
    attestation = ClientPrivateDeletionAttestation(
        **{
            **default_attestation().to_dict(),
            "deleted_before_report_write": False,
        }
    )

    issues = validate_client_private_deletion_attestation(attestation, default_policy(), default_fixture())

    assert any(issue.path == "deleted_before_report_write" for issue in issues)


def test_deletion_attestation_rejects_identifier_like_operator_check() -> None:
    attestation = ClientPrivateDeletionAttestation(
        **{
            **default_attestation().to_dict(),
            "operator_check": (
                "operator verified gitignored local-only paths and deleted source for client 123-45-67890"
            ),
        }
    )

    issues = validate_client_private_deletion_attestation(attestation, default_policy(), default_fixture())

    assert any(issue.path == "operator_check" and "identifier" in issue.message for issue in issues)


def test_render_deletion_attestation_states_boundary() -> None:
    rendered = render_client_private_deletion_attestation(default_attestation(), default_policy(), default_fixture())

    assert "deletion evidence only" in rendered
    assert "does not automate deletion" in rendered
    assert "OCR text" in rendered


def test_deletion_attestation_report_distinguishes_not_implemented() -> None:
    rendered = render_report(check_deletion_attestation())

    assert "Still Not Implemented" in rendered
    assert "real file deletion automation" in rendered
    assert "public-safe deletion evidence contract" in rendered
