from __future__ import annotations

from scripts.private_parser_realism_close_gate import build_close_gate, render_markdown


def test_private_parser_realism_close_gate_closes_and_hands_off() -> None:
    result = build_close_gate()

    assert result["ok"] is True
    assert result["horizon"] == "private-parser-realism-hardening"
    assert result["completed_milestone"] == "PPR5"
    assert result["close_result"] == "realism_contract_ready"
    assert result["next_horizon"] == "external-source-body-connector-expansion"
    assert all(item["exists"] for item in result["evidence"])
    assert all(item["gate_ok"] for item in result["evidence"])


def test_private_parser_realism_close_gate_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_close_gate())

    assert "Private Parser Realism Hardening Close Report" in rendered
    assert "realism_contract_ready" in rendered
    assert "external-source-body-connector-expansion" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "kifrs.db" not in rendered
    assert "source_body" not in rendered
