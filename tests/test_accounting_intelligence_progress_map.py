from __future__ import annotations

from scripts.accounting_intelligence_progress_map import build_progress_map, render_markdown


def test_progress_map_explains_current_position_and_results() -> None:
    progress = build_progress_map()

    assert progress["current_horizon"]["id"] == "end-to-end-demo-scenario"
    assert progress["current_horizon"]["status"] == "closed"
    assert progress["current_horizon"]["milestones"][0]["status"] == "completed"
    assert progress["current_horizon"]["milestones"][1]["status"] == "completed"
    assert progress["current_horizon"]["milestones"][2]["status"] == "completed"
    assert progress["current_horizon"]["milestones"][3]["status"] == "completed"
    assert progress["current_horizon"]["milestones"][4]["status"] == "completed"
    assert progress["next_leaf"] == "none_end_to_end_demo_scenario_closed"
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
    assert "runtime-retriever-promotion-gate" in horizon_ids
    assert "operator-experience-hardening" in horizon_ids


def test_progress_map_markdown_is_public_safe_and_decision_oriented() -> None:
    rendered = render_markdown(build_progress_map())

    assert "Accounting Intelligence Progress Map" in rendered
    assert "Current Horizon" in rendered
    assert "Completed Capability Chain" in rendered
    assert "Open Decisions" in rendered
    assert "end-to-end-demo-scenario" in rendered
    assert "none_end_to_end_demo_scenario_closed" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
    assert "external accountant feedback" not in rendered
