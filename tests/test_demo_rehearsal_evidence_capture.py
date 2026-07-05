from __future__ import annotations

from scripts.demo_rehearsal_evidence_capture import build_evidence_capture, render_markdown


def test_demo_rehearsal_evidence_capture_records_stage_results_and_timing() -> None:
    result = build_evidence_capture()

    assert result["ok"] is True
    assert result["horizon"] == "demo-rehearsal-quality-loop"
    assert result["completed_milestone"] == "DRQ3"
    assert len(result["stage_results"]) >= 8
    assert result["timing"]["total_elapsed_seconds"] > 0
    assert all("generated_at" in item for item in result["stage_results"])
    assert result["checks"]["variance_threshold_applied"] is True
    assert result["checks"]["freshness_metadata_present"] is True
    assert result["checks"]["stage_outputs_fresh"] is True
    assert result["checks"]["no_private_participant_data"] is True
    assert result["next_leaf"] == "DRQ4_demo_improvement_backlog"


def test_demo_rehearsal_evidence_capture_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_evidence_capture())

    assert "DRQ3 Rehearsal Evidence Capture" in rendered
    assert "Timing Metadata" in rendered
    assert "Freshness Metadata" in rendered
    assert "api_key" not in rendered
    assert "secret" not in rendered
    assert "source_body" not in rendered
    assert "packaging" not in rendered.lower()
    assert "external accountant feedback" not in rendered.lower()
