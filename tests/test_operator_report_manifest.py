from __future__ import annotations

from scripts.operator_report_manifest import build_operator_report_manifest, render_markdown


def test_operator_report_manifest_orders_navigation_entries() -> None:
    result = build_operator_report_manifest()

    assert result["ok"], result["errors"]
    assert result["horizon"] == "operator-experience-hardening"
    assert result["completed_milestone"] == "OEH3"
    assert [item["order"] for item in result["entries"]] == sorted(item["order"] for item in result["entries"])
    goals = {item["goal"] for item in result["entries"]}
    assert {"position", "queue", "commands", "doctor", "retriever"} <= goals
    assert result["checks"]["protected_paths_absent"] is True
    assert result["next_gate"] == "error_recovery_playbook"


def test_operator_report_manifest_report_is_public_safe() -> None:
    rendered = render_markdown(build_operator_report_manifest())

    assert "OEH3 Report Manifest" in rendered
    assert "without reading ROADMAP internals" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
