from __future__ import annotations

from scripts.client_private_parser_runtime_gate import build_gate, render_close_markdown, render_markdown


def test_client_private_parser_runtime_gate_passes() -> None:
    gate = build_gate()

    assert gate["ok"] is True
    assert gate["public_safe"] is True
    assert gate["checks"]["cp1_boundary_audit"] is True
    assert gate["checks"]["cp2_runtime_contract"] is True
    assert gate["checks"]["cp3_evidence_adapter"] is True
    assert gate["checks"]["cp4_deletion_gate"] is True
    assert gate["checks"]["multi_authority_runtime_gate"] is True
    assert gate["next_horizon"] == "firm-facing-product-surface"


def test_client_private_parser_runtime_gate_markdown_is_public_safe() -> None:
    gate = build_gate()
    rendered = render_markdown(gate)
    close = render_close_markdown(gate)

    assert "Client-private parser runtime is ready to close." in rendered
    assert "runtime parser contract" in rendered
    assert "firm-facing-product-surface" in close
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
