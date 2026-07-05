from __future__ import annotations

from scripts.real_local_parser_prototype_close_gate import build_close_gate, render_markdown


def test_real_local_parser_prototype_close_gate_passes() -> None:
    gate = build_close_gate()

    assert gate["ok"] is True
    assert gate["close_status"] == "closed"
    assert gate["completed_milestone"] == "RLP5"
    assert gate["next_horizon"] == "source-body-ingestion-controlled-lane"
    assert gate["checks"]["rlp1_asset_inventory"] is True
    assert gate["checks"]["rlp2_fixture_adapter"] is True
    assert gate["checks"]["rlp3_deletion_simulation"] is True
    assert gate["checks"]["rlp4_leak_tests"] is True
    assert gate["checks"]["product_trust_close"] is True
    assert gate["checks"]["client_private_runtime_close"] is True


def test_real_local_parser_prototype_close_gate_report_is_public_safe() -> None:
    rendered = render_markdown(build_close_gate())

    assert "Real Local Parser Prototype Close Gate" in rendered
    assert "local-safe fixture parser path" in rendered
    assert "Still Not Implemented" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
