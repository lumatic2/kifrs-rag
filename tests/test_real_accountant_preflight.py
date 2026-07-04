from __future__ import annotations

import json
from pathlib import Path

from scripts.real_accountant_preflight import check_preflight, render_text


def test_preflight_passes_current_repo_open_files() -> None:
    ok, errors, evidence = check_preflight(
        root=Path.cwd(),
        manifest=Path("docs/reports/real-accountant-session/session_manifest.json"),
    )

    assert ok is True
    assert errors == []
    assert evidence["session_mode"] == "ready_to_schedule"
    assert all(evidence["open_files"].values())


def test_preflight_rejects_non_ready_manifest(tmp_path) -> None:
    manifest = tmp_path / "session_manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "actual_feedback_evidence": True,
                "reviewer_metadata": {
                    "role": "CPA reviewer",
                    "service_line": "F-ACC",
                    "experience_context": "reviewed accounting advisory workpapers",
                },
                "notes_file": "notes.md",
                "capture_manifest": "capture.json",
                "queue_jsonl": "queue.jsonl",
            }
        ),
        encoding="utf-8",
    )

    ok, errors, _evidence = check_preflight(root=tmp_path, manifest=manifest)

    assert ok is False
    assert "session_manifest: expected ready_to_schedule before session, got actual_feedback" in errors


def test_render_text_lists_open_files() -> None:
    text = render_text(
        True,
        [],
        {"session_mode": "ready_to_schedule", "open_files": {"a.md": True}, "generator_results": []},
    )

    assert "ok: True" in text
    assert "- a.md: True" in text
