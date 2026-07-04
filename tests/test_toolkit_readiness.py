from __future__ import annotations

import json

from scripts.toolkit_readiness import (
    load_manifest,
    render_readiness_report,
    run_readiness,
)


def test_load_default_manifest_has_public_safe_commands() -> None:
    manifest = load_manifest(__import__("pathlib").Path("docs/toolkit/readiness_manifest.json"))

    command_ids = {item["id"] for item in manifest["reproduction_commands"]}
    assert {"quality_preflight", "demo_poc", "workflow_rebuild_report", "feedback_queue_report"} <= command_ids
    assert manifest["protected_assets_policy"]["required_for_public_readiness"] is False


def test_readiness_passes_artifacts_without_running_commands() -> None:
    result = run_readiness(__import__("pathlib").Path("docs/toolkit/readiness_manifest.json"), run_commands=False)

    artifact_checks = [check for check in result.checks if check.kind == "artifact"]
    command_checks = [check for check in result.checks if check.kind == "command"]
    assert artifact_checks
    assert all(check.status == "PASS" for check in artifact_checks)
    assert all(check.status == "SKIP" for check in command_checks)
    assert result.ok


def test_readiness_fails_missing_file(tmp_path) -> None:
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps({"required_artifacts": ["missing.file"], "reproduction_commands": []}),
        encoding="utf-8",
    )

    result = run_readiness(manifest_path, run_commands=False)

    assert not result.ok
    assert result.failed[0].check_id == "missing.file"


def test_readiness_rejects_protected_required_artifact(tmp_path) -> None:
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps({"required_artifacts": ["data/kifrs.db"], "reproduction_commands": []}),
        encoding="utf-8",
    )

    result = run_readiness(manifest_path, run_commands=False)

    assert not result.ok
    assert result.failed[0].detail == "protected asset cannot be required"


def test_readiness_report_renders_next_action() -> None:
    result = run_readiness(__import__("pathlib").Path("docs/toolkit/readiness_manifest.json"), run_commands=False)
    rendered = render_readiness_report(result)

    assert "# Toolkit Readiness Report" in rendered
    assert "Overall: PASS" in rendered
    assert "Next Action" in rendered
    assert "protected K-IFRS source data" in rendered
