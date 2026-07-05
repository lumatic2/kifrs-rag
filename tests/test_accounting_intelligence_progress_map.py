from __future__ import annotations

from scripts.accounting_intelligence_progress_map import build_progress_map, render_markdown


def test_progress_map_explains_current_position_and_results() -> None:
    progress = build_progress_map()

    assert progress["current_horizon"]["id"] == "runtime-retriever-promotion-gate"
    assert progress["current_horizon"]["status"] == "active"
    assert progress["current_horizon"]["milestones"][0]["status"] == "completed"
    assert progress["current_horizon"]["milestones"][1]["status"] == "completed"
    assert progress["current_horizon"]["milestones"][2]["status"] == "active_next"
    assert progress["current_horizon"]["milestones"][3]["status"] == "pending"
    assert progress["current_horizon"]["milestones"][4]["status"] == "pending"
    assert progress["next_leaf"] == "RPG3_failure_rollback_policy"
    assert progress["automation_snapshot"]["review_packs"] == 24
    assert progress["automation_snapshot"]["automated_packs"] >= 20
    horizon_ids = {horizon["id"] for horizon in progress["completed_horizons"]}
    assert "firm-service-map" in horizon_ids
    assert "rag-quality-refresh" in horizon_ids
    assert "multi-authority-runtime-hardening" in horizon_ids
    assert "client-private-parser-runtime" in horizon_ids
    assert "real-local-parser-prototype" in horizon_ids
    assert "source-body-ingestion-controlled-lane" in horizon_ids
    assert "workflow-coverage-expansion" in horizon_ids


def test_progress_map_markdown_is_public_safe_and_decision_oriented() -> None:
    rendered = render_markdown(build_progress_map())

    assert "Accounting Intelligence Progress Map" in rendered
    assert "Current Horizon" in rendered
    assert "Completed Capability Chain" in rendered
    assert "Open Decisions" in rendered
    assert "runtime-retriever-promotion-gate" in rendered
    assert "RPG3_failure_rollback_policy" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
    assert "external accountant feedback" not in rendered
