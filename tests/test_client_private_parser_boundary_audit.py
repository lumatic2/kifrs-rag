from __future__ import annotations

from scripts.client_private_parser_boundary_audit import build_boundary_audit, render_markdown


def test_client_private_parser_boundary_audit_passes_and_inventories_surfaces() -> None:
    audit = build_boundary_audit()

    assert audit["ok"] is True
    paths = {row["path"] for row in audit["surfaces"]}
    assert "kifrs/feedback/case_intake.py" in paths
    assert "kifrs/feedback/local_parser.py" in paths
    assert "kifrs/runtime/authority_boundary.py" in paths
    assert "docs/ingestion/non_ifrs_source_records.example.json" in paths
    assert audit["checks"]["upload_storage_policy"]["ok"] is True
    assert audit["checks"]["parser_dry_run_fixture"]["ok"] is True
    assert audit["checks"]["deletion_attestation"]["ok"] is True
    assert audit["checks"]["adapter_contract"]["ok"] is True


def test_client_private_parser_boundary_audit_classifies_remaining_gaps() -> None:
    audit = build_boundary_audit()
    milestones = {row["milestone"] for row in audit["gaps"]}
    gap_text = " ".join(row["gap"] for row in audit["gaps"])

    assert {"CP2", "CP3", "CP4", "CP5"}.issubset(milestones)
    assert "runtime parser contract" in gap_text
    assert "client_private_fact" in gap_text
    assert "deletion" in gap_text


def test_client_private_parser_boundary_audit_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_boundary_audit())

    assert "CP1 Private Parser Boundary Audit" in rendered
    assert "Existing Surfaces" in rendered
    assert "Implementation Gaps" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
