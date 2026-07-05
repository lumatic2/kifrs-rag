from __future__ import annotations

from scripts.external_source_body_ingestion_authorization_gate import (
    BodyIngestionAuthorization,
    check_authorization_gate,
    render_report,
)


def test_authorization_gate_defers_without_explicit_record() -> None:
    result = check_authorization_gate()

    assert result["ok"], result["errors"]
    assert result["decision"] == "defer"
    assert result["allowed_to_implement"] is False
    assert result["authorization_present"] is False
    assert result["authorization_valid"] is False
    assert "explicit authorization record is required" in " ".join(result["blockers"])
    assert "synthetic parser/chunker dry-run" in result["next_leaf"]


def test_authorization_gate_rejects_unsafe_authorization_record() -> None:
    authorization = BodyIngestionAuthorization(
        authorized_by="",
        authorization_scope="all_sources_forever",
        risk_acknowledgement=False,
        source_review_required=False,
        public_repo_body_commit_allowed=True,
        live_fetch_allowed=True,
        chunking_allowed=True,
        embedding_allowed=True,
    )

    result = check_authorization_gate(authorization=authorization)
    blockers = " ".join(result["blockers"])

    assert result["decision"] == "defer"
    assert result["allowed_to_implement"] is False
    assert "authorized_by is required" in blockers
    assert "authorization_scope must be one of" in blockers
    assert "risk_acknowledgement must be true" in blockers
    assert "source_review_required must be true" in blockers
    assert "public_repo_body_commit_allowed must be false" in blockers


def test_authorization_gate_can_proceed_with_valid_record() -> None:
    authorization = BodyIngestionAuthorization(
        authorized_by="user-explicit-approval",
        authorization_scope="source_specific_local_private_body",
        risk_acknowledgement=True,
        source_review_required=True,
        public_repo_body_commit_allowed=False,
        live_fetch_allowed=True,
        chunking_allowed=True,
        embedding_allowed=True,
    )

    result = check_authorization_gate(authorization=authorization)

    assert result["ok"], result["errors"]
    assert result["authorization_present"] is True
    assert result["authorization_valid"] is True
    assert result["decision"] == "proceed"
    assert result["allowed_to_implement"] is True
    assert result["next_leaf"] == "external source body ingestion implementation"


def test_authorization_gate_report_keeps_security_boundary_explicit() -> None:
    rendered = render_report(check_authorization_gate())

    assert "External Source Body Authorization Gate" in rendered
    assert "no explicit authorization record is present" in rendered
    assert "public_repo_body_commit_allowed" in rendered
    assert "must be false" in rendered
    assert "Still Not Implemented" in rendered
    assert "external body embeddings" in rendered
