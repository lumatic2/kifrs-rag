from __future__ import annotations

from scripts.product_trust_quality_gate import build_gate, render_markdown


def test_product_trust_quality_gate_closes_horizon() -> None:
    gate = build_gate()

    assert gate["ok"] is True
    assert gate["close_status"] == "closed"
    assert gate["promotion_decision"] == "defer"
    assert gate["promote_to_default"] is False
    assert gate["checks"]["ptq1_inventory"] is True
    assert gate["checks"]["ptq2_confidence"] is True
    assert gate["checks"]["ptq3_failure_boundary"] is True
    assert gate["checks"]["ptq4_promotion_decision"] is True


def test_product_trust_quality_gate_report_is_public_safe() -> None:
    rendered = render_markdown(build_gate())

    assert "Product Trust And Quality Close Gate" in rendered
    assert "confidence labels" in rendered
    assert "promotion decision" in rendered
    assert "api_key" not in rendered
    assert "source_body" not in rendered
