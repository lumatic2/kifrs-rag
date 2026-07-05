from __future__ import annotations

from scripts.accounting_intelligence_progress_map import build_progress_map, render_markdown


def test_progress_map_explains_current_position_and_results() -> None:
    progress = build_progress_map()

    assert progress["current_horizon"]["id"] == "internal-capability-hardening"
    assert progress["current_horizon"]["milestones"][0]["status"] == "completed"
    assert progress["current_horizon"]["milestones"][1]["status"] == "candidate_next"
    assert progress["next_leaf"] == "select_internal_capability_horizon"
    assert progress["automation_snapshot"]["review_packs"] == 24
    assert progress["automation_snapshot"]["automated_packs"] >= 20
    horizon_ids = {horizon["id"] for horizon in progress["completed_horizons"]}
    assert "firm-service-map" in horizon_ids
    assert "rag-quality-refresh" in horizon_ids
    assert "field-feedback runbook/capture" in horizon_ids


def test_progress_map_markdown_is_public_safe_and_decision_oriented() -> None:
    rendered = render_markdown(build_progress_map())

    assert "Accounting Intelligence Progress Map" in rendered
    assert "Current Horizon" in rendered
    assert "Completed Capability Chain" in rendered
    assert "Open Decisions" in rendered
    assert "internal-capability-hardening" in rendered
    assert "select_internal_capability_horizon" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
