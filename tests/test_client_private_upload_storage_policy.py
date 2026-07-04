from __future__ import annotations

from kifrs.feedback import (
    ClientPrivateUploadStoragePolicy,
    render_client_private_upload_storage_policy,
    validate_client_private_upload_storage_policy,
)
from scripts.client_private_upload_storage_policy_check import check_upload_storage_policy, render_report


def test_default_upload_storage_policy_passes() -> None:
    result = check_upload_storage_policy()

    assert result["ok"], result["errors"]
    assert result["policy"]["raw_file_persistence_allowed"] is False
    assert result["policy"]["commit_allowed"] is False


def test_upload_storage_policy_rejects_private_persistence() -> None:
    policy = ClientPrivateUploadStoragePolicy(
        policy_id="bad",
        upload_storage_mode="local_ephemeral_quarantine",
        parser_mode="structured_facts_only",
        deletion_mode="manual_before_commit",
        allowed_public_artifacts=["redacted structured facts", "deletion attestation"],
        forbidden_public_artifacts=["raw private file", "parsed private body", "private embedding"],
        local_only_paths=["data/private_uploads/"],
        required_operator_checks=["verify local-only paths are gitignored", "delete quarantined raw files"],
        raw_file_persistence_allowed=True,
        parsed_body_persistence_allowed=True,
        embedding_allowed=True,
        commit_allowed=True,
    )

    issues = validate_client_private_upload_storage_policy(policy)

    assert any(issue.path == "raw_file_persistence_allowed" for issue in issues)
    assert any(issue.path == "parsed_body_persistence_allowed" for issue in issues)
    assert any(issue.path == "embedding_allowed" for issue in issues)
    assert any(issue.path == "commit_allowed" for issue in issues)


def test_render_upload_storage_policy_states_boundary() -> None:
    result = check_upload_storage_policy()
    policy = ClientPrivateUploadStoragePolicy(**result["policy"])
    rendered = render_client_private_upload_storage_policy(policy)

    assert "does not implement upload, OCR, or private document parsing" in rendered
    assert "deletion attestation" in rendered
    assert "private embedding" in rendered


def test_upload_storage_policy_report_distinguishes_not_implemented() -> None:
    rendered = render_report(check_upload_storage_policy())

    assert "Still Not Implemented" in rendered
    assert "file upload UI" in rendered
    assert "local ephemeral quarantine" in rendered
