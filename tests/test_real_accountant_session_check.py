from __future__ import annotations

import json

from scripts.real_accountant_session_check import check_session_manifest


def test_ready_to_schedule_manifest_passes() -> None:
    ok, errors, mode = check_session_manifest(
        __import__("pathlib").Path("docs/reports/real-accountant-session/session_manifest.json")
    )

    assert ok is True
    assert errors == []
    assert mode == "ready_to_schedule"


def test_actual_manifest_requires_reviewer_metadata(tmp_path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps({"actual_feedback_evidence": True}), encoding="utf-8")

    ok, errors, mode = check_session_manifest(path, root=tmp_path)

    assert ok is False
    assert mode == "actual_feedback"
    assert any("missing actual evidence fields" in error for error in errors)
    assert any("missing reviewer metadata" in error for error in errors)


def test_actual_manifest_passes_with_capture_and_queue(tmp_path) -> None:
    notes = tmp_path / "notes.md"
    notes.write_text("# Notes\n", encoding="utf-8")
    capture = tmp_path / "capture.json"
    capture.write_text(json.dumps({"actual_feedback_evidence": True}), encoding="utf-8")
    queue = tmp_path / "queue.jsonl"
    queue.write_text("{}\n", encoding="utf-8")
    manifest = {
        "actual_feedback_evidence": True,
        "reviewer_metadata": {
            "role": "CPA",
            "service_line": "F-ACC",
            "experience_context": "Accounting advisory",
        },
        "notes_file": "notes.md",
        "capture_manifest": "capture.json",
        "queue_jsonl": "queue.jsonl",
    }
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    ok, errors, mode = check_session_manifest(path, root=tmp_path)

    assert ok is True
    assert errors == []
    assert mode == "actual_feedback"


def test_actual_manifest_rejects_capture_manifest_without_actual_flag(tmp_path) -> None:
    notes = tmp_path / "notes.md"
    notes.write_text("# Notes\n", encoding="utf-8")
    capture = tmp_path / "capture.json"
    capture.write_text(json.dumps({"actual_feedback_evidence": False}), encoding="utf-8")
    queue = tmp_path / "queue.jsonl"
    queue.write_text("{}\n", encoding="utf-8")
    manifest = {
        "actual_feedback_evidence": True,
        "reviewer_metadata": {
            "role": "CPA",
            "service_line": "F-ACC",
            "experience_context": "Accounting advisory",
        },
        "notes_file": "notes.md",
        "capture_manifest": "capture.json",
        "queue_jsonl": "queue.jsonl",
    }
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    ok, errors, _mode = check_session_manifest(path, root=tmp_path)

    assert ok is False
    assert errors == ["capture manifest is not actual_feedback_evidence true"]
