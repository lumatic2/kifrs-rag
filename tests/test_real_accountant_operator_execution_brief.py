from __future__ import annotations

from pathlib import Path

from scripts.real_accountant_operator_execution_brief import build_execution_brief, render_markdown


def test_execution_brief_orders_invite_schedule_capture_and_close() -> None:
    brief = build_execution_brief(root=Path.cwd())

    assert brief["session_mode"] == "ready_to_schedule"
    assert brief["next_action"] == "Send reviewer invite and update outreach ledger to sent."
    assert len(brief["run_order"]) == 6
    joined_commands = "\n".join(command for step in brief["run_order"] for command in step["commands"])
    assert "real_accountant_invite_dispatch_gate.py" in joined_commands
    assert "real_accountant_response_handling_gate.py" in joined_commands
    assert "real_accountant_scheduled_session_gate.py" in joined_commands
    assert "real_accountant_capture_readiness_gate.py" in joined_commands
    assert "real_accountant_manifest_build.py" in joined_commands
    assert "real_accountant_close_check.py" in joined_commands


def test_execution_brief_names_user_owned_decisions_and_public_safe_boundary() -> None:
    rendered = render_markdown(build_execution_brief(root=Path.cwd()))

    assert "reviewer identity, real sending, scheduling, and actual feedback content are user/operator-owned" in rendered
    assert "Do not mark actual_feedback_evidence true" in rendered
    assert "source_body" not in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
