from __future__ import annotations

from scripts.firm_facing_readiness_checklist import build_readiness, render_markdown


def test_firm_facing_readiness_has_install_and_run_path() -> None:
    readiness = build_readiness()

    assert readiness["ok"] is True
    assert readiness["milestone"] == "FPS3"
    assert "uv sync" in readiness["run_commands"]
    assert any("firm_facing_operator_demo_command.py" in command for command in readiness["run_commands"])
    assert readiness["missing_files"] == []


def test_firm_facing_readiness_documents_protected_boundary() -> None:
    rendered = render_markdown(build_readiness())

    assert "Protected Boundary" in rendered
    assert "structured facts only" in rendered
    assert "Accountant review" in rendered
    assert "source_body" not in rendered
    assert "api_key" not in rendered
