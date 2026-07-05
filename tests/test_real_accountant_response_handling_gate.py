from __future__ import annotations

from scripts.real_accountant_response_handling_gate import (
    check_response_handling_gate,
    render_report,
)


def test_response_handling_gate_simulates_all_response_paths() -> None:
    result = check_response_handling_gate()

    assert result["ok"], result["errors"]
    assert set(result["response_packets"]) == {"decline", "follow_up", "schedule"}
    assert result["response_simulations"]["follow_up"]["expected_status"] == "sent"
    assert result["response_simulations"]["schedule"]["expected_status"] == "scheduled"
    assert result["response_simulations"]["decline"]["expected_status"] == "declined"
    assert result["response_simulations"]["schedule"]["counts"]["scheduled"] == 1
    assert result["response_simulations"]["decline"]["counts"]["declined"] == 1
    assert result["response_simulations"]["decline"]["row"]["invite_sent"] is True
    for packet in result["response_packets"].values():
        assert "C:/" not in packet["ledger_update_command"]
        assert "docs/reports/real-accountant-session/outreach-log.sample.jsonl" in packet["ledger_update_command"]


def test_response_handling_gate_report_states_boundary() -> None:
    rendered = render_report(check_response_handling_gate())

    assert "RS2 Response Handling Gate" in rendered
    assert "does not contact the reviewer" in rendered
    assert "schedule moves a copied ledger to `scheduled`" in rendered
    assert "source_body" not in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
