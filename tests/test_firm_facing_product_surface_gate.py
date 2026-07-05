from __future__ import annotations

from scripts.firm_facing_product_surface_gate import build_gate, render_markdown


def test_firm_facing_product_surface_gate_closes_horizon() -> None:
    gate = build_gate()

    assert gate["ok"] is True
    assert gate["close_status"] == "closed"
    assert gate["milestone"] == "FPS5"
    assert gate["checks"]["fps2_operator_demo"] is True
    assert gate["checks"]["fps3_readiness"] is True
    assert gate["checks"]["fps4_narrative"] is True
    assert gate["missing_reports"] == []


def test_firm_facing_product_surface_gate_report_is_public_safe() -> None:
    rendered = render_markdown(build_gate())

    assert "Firm-Facing Product Surface Close Gate" in rendered
    assert "demo command, readiness checklist, README narrative" in rendered
    assert "quality_preflight.py" in rendered
    assert "rag_quality_final_gate.py" in rendered
    assert "source_body" not in rendered
    assert "api_key" not in rendered
