from __future__ import annotations

import pytest

from scripts.real_accountant_invite_packet import build_invite_packet, render_markdown, render_text, write_report


def test_build_invite_packet_uses_public_safe_alias_and_update_command() -> None:
    packet = build_invite_packet()

    assert packet["reviewer_alias"] == "reviewer-001"
    assert packet["subject"] == "회계 AI PoC 30분 피드백 요청 초안"
    assert "고객자료, 계약 원문, 회사명, 사업자번호" in packet["body"]
    assert "--status sent" in packet["post_send_update_command"]
    assert "--reviewer-alias reviewer-001" in packet["post_send_update_command"]


def test_build_invite_packet_rejects_non_alias() -> None:
    with pytest.raises(ValueError, match="public-safe alias"):
        build_invite_packet(reviewer_alias="actual-name")


def test_render_text_includes_message_and_after_send_command() -> None:
    rendered = render_text(build_invite_packet())

    assert "Real Accountant Invite Packet" in rendered
    assert "Message:" in rendered
    assert "After sending, run:" in rendered
    assert "real_accountant_outreach_update.py" in rendered


def test_write_report_creates_copy_ready_action_packet(tmp_path) -> None:
    out = tmp_path / "invite-action.md"
    packet = write_report(build_invite_packet(), out)

    report = out.read_text(encoding="utf-8")
    assert packet["report_path"] == out.as_posix()
    assert "Reviewer Invite Action Packet" in report
    assert "Copy Message" in report
    assert "After Manual Send" in report
    assert "does not send the message" in report
    assert "real_accountant_outreach_update.py" in report
    assert "api_key" not in report
    assert "token" not in report


def test_render_markdown_states_manual_send_boundary() -> None:
    rendered = render_markdown(build_invite_packet())

    assert "Run the ledger update only after the invite was actually sent" in rendered
    assert "```text" in rendered
