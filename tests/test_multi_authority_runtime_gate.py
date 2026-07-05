from __future__ import annotations

from scripts.multi_authority_runtime_gate import build_gate, render_close_markdown, render_markdown


def test_multi_authority_runtime_gate_passes_and_renders_all_roles() -> None:
    gate = build_gate()

    assert gate["ok"] is True
    assert gate["public_safe"] is True
    assert set(gate["role_counts"]) == {
        "primary_kifrs_evidence",
        "supporting_interpretation",
        "legal_boundary",
        "fact_evidence",
        "client_private_fact",
    }
    assert all(count >= 1 for count in gate["role_counts"].values())
    assert gate["review_pack_panel_ok"] is True
    assert gate["structured_fact_hook_ok"] is True
    assert gate["next_horizon"] == "client-private-parser-runtime"


def test_multi_authority_runtime_gate_markdown_is_public_safe_and_decision_oriented() -> None:
    gate = build_gate()
    rendered = render_markdown(gate)
    close = render_close_markdown(gate)

    assert "Multi-authority runtime hardening is ready to close." in rendered
    assert "Runtime Authority Boundary" in rendered
    assert "Carried Regression Commands" in rendered
    assert "client-private-parser-runtime" in close
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
