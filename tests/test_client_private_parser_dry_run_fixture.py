from __future__ import annotations

from kifrs.feedback import (
    ClientPrivateParserDryRunFixture,
    render_client_private_parser_dry_run_fixture,
    validate_client_private_parser_dry_run_fixture,
)
from scripts.client_private_parser_dry_run_fixture_check import (
    check_parser_dry_run_fixture,
    default_fixture,
    render_report,
)
from scripts.client_private_upload_storage_policy_check import default_policy


def test_default_parser_dry_run_fixture_passes_and_routes() -> None:
    result = check_parser_dry_run_fixture()

    assert result["ok"], result["errors"]
    assert result["route"]["status"] == "candidate"
    assert result["route"]["route"] == "kifrs1116_review_pack"
    assert "source_locator" not in result["redacted_summary"]


def test_parser_dry_run_fixture_rejects_source_body_fields() -> None:
    fixture = ClientPrivateParserDryRunFixture(
        **{
            **default_fixture().to_dict(),
            "structured_facts": {"raw_contract": "copied private text"},
        }
    )

    issues = validate_client_private_parser_dry_run_fixture(fixture, default_policy())

    assert any("raw_contract" in issue.path for issue in issues)


def test_parser_dry_run_fixture_requires_deletion_attestation() -> None:
    fixture = ClientPrivateParserDryRunFixture(**{**default_fixture().to_dict(), "deletion_attestation": ""})

    issues = validate_client_private_parser_dry_run_fixture(fixture, default_policy())

    assert any(issue.path == "deletion_attestation" for issue in issues)


def test_render_parser_dry_run_fixture_states_boundary() -> None:
    rendered = render_client_private_parser_dry_run_fixture(default_fixture(), default_policy())

    assert "does not contain raw file content" in rendered
    assert "synthetic" in rendered
    assert "OCR text" in rendered


def test_parser_dry_run_report_distinguishes_not_implemented() -> None:
    rendered = render_report(check_parser_dry_run_fixture())

    assert "Still Not Implemented" in rendered
    assert "real private document parser" in rendered
    assert "redacted structured facts" in rendered
