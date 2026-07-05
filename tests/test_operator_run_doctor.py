from __future__ import annotations

from scripts.operator_run_doctor import build_operator_run_doctor, render_markdown


def test_operator_run_doctor_checks_environment_reports_and_boundaries() -> None:
    result = build_operator_run_doctor()

    assert result["ok"], result["errors"]
    assert result["horizon"] == "operator-experience-hardening"
    assert result["completed_milestone"] == "OEH2"
    assert result["checks"]["python_available"] is True
    assert result["checks"]["uv_checked"] is True
    assert result["checks"]["required_reports_checked"] is True
    assert result["checks"]["protected_boundaries_checked"] is True
    assert result["reports"]["command_inventory"]["hint"].startswith("python scripts")
    assert result["next_gate"] == "report_manifest_and_navigation_surface"


def test_operator_run_doctor_report_is_public_safe() -> None:
    rendered = render_markdown(build_operator_run_doctor())

    assert "OEH2 Run Doctor" in rendered
    assert "without reading private payloads" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
