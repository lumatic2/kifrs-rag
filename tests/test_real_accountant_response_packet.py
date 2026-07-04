from __future__ import annotations

import pytest

from scripts.real_accountant_response_packet import build_response_packet, render_text


def test_schedule_response_packet_outputs_scheduled_update_command() -> None:
    packet = build_response_packet(response="schedule")

    assert packet["reviewer_alias"] == "reviewer-001"
    assert "--status scheduled" in packet["ledger_update_command"]
    assert "고객자료나 계약 원문은 받지 않겠습니다" in packet["message"]


def test_follow_up_response_packet_outputs_sent_update_command() -> None:
    packet = build_response_packet(response="follow_up")

    assert "--status sent" in packet["ledger_update_command"]
    assert "follow-up sent" in packet["ledger_update_command"]


def test_decline_response_packet_outputs_declined_update_command() -> None:
    packet = build_response_packet(response="decline")

    assert "--status declined" in packet["ledger_update_command"]
    assert "reviewer declined" in packet["ledger_update_command"]


def test_response_packet_rejects_non_alias() -> None:
    with pytest.raises(ValueError, match="public-safe alias"):
        build_response_packet(response="schedule", reviewer_alias="actual-name")


def test_render_text_includes_boundary_and_command() -> None:
    rendered = render_text(build_response_packet(response="schedule"))

    assert "Real Accountant Outreach Response Packet" in rendered
    assert "Boundary:" in rendered
    assert "real_accountant_outreach_update.py" in rendered
