from __future__ import annotations

from scripts.private_parser_authorization_safe_adapter_proof import (
    build_authorization_safe_adapter_proof,
    render_markdown,
)


def test_private_parser_authorization_safe_adapter_proof_sets_required_gates() -> None:
    proof = build_authorization_safe_adapter_proof()

    assert proof["ok"] is True
    assert proof["horizon"] == "private-parser-realism-hardening"
    assert proof["completed_milestone"] == "PPR1"
    assert proof["next_leaf"] == "PPR2_realistic_local_fixture_adapter_contract"
    assert all(item["exists"] for item in proof["evidence"])
    gate_names = {gate["gate"] for gate in proof["gates"]}
    assert {"explicit_authorization", "local_only_processing", "deletion_attestation"} <= gate_names
    assert "real protected file has been ingested" in proof["forbidden_claims"]


def test_private_parser_authorization_safe_adapter_proof_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_authorization_safe_adapter_proof())

    assert "PPR1 Authorization-Safe Adapter Proof Plan" in rendered
    assert "structured-facts-only public evidence" in rendered
    assert "real protected file has been ingested" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "kifrs.db" not in rendered
    assert "source_body" not in rendered
