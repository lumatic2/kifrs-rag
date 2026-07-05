from __future__ import annotations

from scripts.operator_command_inventory import build_operator_command_inventory, render_markdown


def test_operator_command_inventory_groups_required_goals() -> None:
    result = build_operator_command_inventory()

    assert result["ok"], result["errors"]
    assert result["horizon"] == "operator-experience-hardening"
    assert result["completed_milestone"] == "OEH1"
    goals = {item["goal"] for item in result["commands"]}
    assert {
        "quality_rag",
        "trust_surface",
        "controlled_source_lane",
        "workflow_coverage",
        "retriever_promotion",
        "progress_position",
        "operator_hardening",
    } <= goals
    assert result["checks"]["all_required_goals_present"] is True
    assert result["checks"]["safety_notes_present"] is True
    assert result["next_gate"] == "run_doctor_and_environment_checks"


def test_operator_command_inventory_report_is_public_safe() -> None:
    rendered = render_markdown(build_operator_command_inventory())

    assert "OEH1 Operator Command Inventory" in rendered
    assert "goal-based command inventory" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
