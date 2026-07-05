from __future__ import annotations

from scripts.multi_authority_runtime_boundary_audit import build_boundary_audit, render_markdown


def test_boundary_audit_inventory_and_gap_map() -> None:
    audit = build_boundary_audit()

    assert audit["ok"] is True
    surface_paths = {row["path"] for row in audit["runtime_surfaces"]}
    assert "kifrs/runtime/evidence.py" in surface_paths
    assert "kifrs/runtime/evidence_panel.py" in surface_paths
    assert "kifrs/runtime/answer_boundary.py" in surface_paths
    assert "kifrs/workflows/statement_draft/schema.py" in surface_paths

    assert "primary_kifrs_evidence" in audit["runtime_supported_roles"]
    assert "supporting_interpretation" in audit["runtime_supported_roles"]
    assert "legal_boundary" in audit["runtime_supported_roles"]
    assert "fact_evidence" in audit["runtime_supported_roles"]
    assert audit["source_record_roles"]["client_private_fact"]["runtime_role_supported"] is False
    assert audit["next_leaf"] == "MAH2_runtime_evidence_contract_hardening"


def test_boundary_audit_classifies_remaining_milestones() -> None:
    audit = build_boundary_audit()
    gap_milestones = {row["milestone"] for row in audit["gaps"]}
    gap_text = " ".join(row["gap"] for row in audit["gaps"])

    assert {"MAH2", "MAH3", "MAH4", "MAH5"}.issubset(gap_milestones)
    assert "Client-private" in gap_text
    assert "five-group authority panel" in gap_text


def test_boundary_audit_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_boundary_audit())

    assert "MAH1 Runtime Evidence Boundary Audit" in rendered
    assert "NIS Handoff Compared To Runtime" in rendered
    assert "Hardening Gaps" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
    assert "raw filing payload" not in rendered
