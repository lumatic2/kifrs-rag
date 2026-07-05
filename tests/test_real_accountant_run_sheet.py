from __future__ import annotations

from scripts.real_accountant_run_sheet import build_run_sheet, render_text


def test_build_run_sheet_extracts_packet_and_runbook_items() -> None:
    sheet = build_run_sheet()

    assert sheet["status_command"] == "python scripts\\real_accountant_status.py"
    assert sheet["proof_snapshot"]["total_review_packs"] == 24
    assert sheet["proof_snapshot"]["automated_packs"] >= 20
    assert sheet["decision_queue"]["recommended_next_decision"] == "send_reviewer_invite"
    assert sheet["decision_queue"]["open_decisions"] == 4
    assert "docs/reports/firm-facing-poc/2026-07-05-one-page-brief.md" in sheet["open_files"]
    assert "docs/reports/2026-07-05-accounting-intelligence-gap-audit.md" in sheet["open_files"]
    assert "docs/reports/2026-07-05-accounting-intelligence-decision-queue.md" in sheet["open_files"]
    assert "이 도구가 가장 가까운 팀은 어디인가?" in sheet["required_questions"][0]
    assert any("demo_poc.py" in command for command in sheet["preflight_commands"])
    assert any("real_accountant_invite_dispatch_gate.py" in command for command in sheet["preflight_commands"])
    assert any("real_accountant_readiness_index.py" in command for command in sheet["preflight_commands"])
    assert any("accounting_intelligence_next_action.py" in command for command in sheet["preflight_commands"])
    assert any("accounting_intelligence_decision_queue.py" in command for command in sheet["preflight_commands"])
    assert any("real_accountant_invite_packet.py" in command and "--write" in command for command in sheet["preflight_commands"])
    assert any("real_accountant_external_action_boundary_gate.py" in command for command in sheet["preflight_commands"])
    assert any("real_accountant_response_handling_gate.py" in command for command in sheet["preflight_commands"])
    assert any("real_accountant_scheduled_session_gate.py" in command for command in sheet["preflight_commands"])
    assert any("real_accountant_capture_readiness_gate.py" in command for command in sheet["preflight_commands"])
    assert any("real_accountant_operator_execution_brief.py" in command for command in sheet["preflight_commands"])
    assert any("real_accountant_pre_send_final_gate.py" in command for command in sheet["preflight_commands"])
    assert any("real_accountant_after_send_action_matrix.py" in command for command in sheet["preflight_commands"])
    assert any("real_accountant_notes_quality_gate.py" in command for command in sheet["preflight_commands"])
    assert any("real_accountant_post_session_final_gate.py" in command for command in sheet["preflight_commands"])
    assert any("real_accountant_close_state_matrix.py" in command for command in sheet["preflight_commands"])


def test_render_text_includes_session_sequence() -> None:
    rendered = render_text(build_run_sheet())

    assert "Real Accountant 30-Minute Run Sheet" in rendered
    assert "Before Invite:" in rendered
    assert "Open Files:" in rendered
    assert "Proof Snapshot:" in rendered
    assert "Decision Queue:" in rendered
    assert "send_reviewer_invite" in rendered
    assert "Automation rate" in rendered
    assert "After Session:" in rendered
    assert "real_accountant_notes_check.py" in rendered
