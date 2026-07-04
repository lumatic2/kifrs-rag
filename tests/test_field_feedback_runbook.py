from __future__ import annotations

import json

from scripts.field_feedback_runbook_check import check_manifest


def test_field_feedback_runbook_manifest_passes() -> None:
    ok, errors = check_manifest_path()

    assert ok is True
    assert errors == []


def test_field_feedback_runbook_checker_reports_missing_artifact(tmp_path) -> None:
    manifest = {
        "required_artifacts": ["missing.md"],
        "required_sections": {},
    }
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    ok, errors = check_manifest(path, root=tmp_path)

    assert ok is False
    assert errors == ["missing artifact: missing.md"]


def test_field_feedback_runbook_checker_rejects_protected_required_artifact(tmp_path) -> None:
    manifest = {
        "required_artifacts": ["data/raw.pdf"],
        "required_sections": {},
    }
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    ok, errors = check_manifest(path, root=tmp_path)

    assert ok is False
    assert errors == ["protected required artifact: data/raw.pdf"]


def test_field_feedback_runbook_checker_reports_missing_section(tmp_path) -> None:
    doc = tmp_path / "doc.md"
    doc.write_text("# Doc\n\n## Present\n", encoding="utf-8")
    manifest = {
        "required_artifacts": ["doc.md"],
        "required_sections": {"doc.md": ["## Present", "## Missing"]},
    }
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    ok, errors = check_manifest(path, root=tmp_path)

    assert ok is False
    assert errors == ["missing section in doc.md: ## Missing"]


def check_manifest_path():
    return check_manifest(
        __import__("pathlib").Path("docs/reports/field-feedback-runbook/runbook_manifest.json")
    )
