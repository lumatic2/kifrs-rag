from __future__ import annotations

from scripts.firm_facing_operator_demo_command import build_demo_packet, render_markdown


def test_operator_demo_packet_contains_required_surfaces() -> None:
    packet = build_demo_packet()

    assert packet["ok"] is True
    assert packet["milestone"] == "FPS2"
    assert packet["workflow_result"]["standard"] == "KIFRS1116"
    assert packet["workflow_result"]["case_id"] == "scenario_01_simple_office_lease"
    assert packet["workflow_result"]["status"] == "automated"
    assert packet["authority_boundary"]["all_roles_present"] is True
    assert packet["private_runtime_boundary"]["ok"] is True
    assert packet["verification_status"]["multi_authority_runtime_close_report"] is True
    assert packet["verification_status"]["client_private_parser_runtime_close_report"] is True


def test_operator_demo_markdown_is_public_safe_and_actionable() -> None:
    rendered = render_markdown(build_demo_packet())

    assert "FPS2 Operator Demo Command" in rendered
    assert "1116 lease review-pack walkthrough" in rendered
    assert "## Review Pack Walkthrough" in rendered
    assert "## Runtime Authority Boundary" in rendered
    assert "Client-private fact" in rendered
    assert "source_body" not in rendered
    assert "api_key" not in rendered
    assert "secret" not in rendered.lower()
