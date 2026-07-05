from __future__ import annotations

from scripts.e2e_demo_asset_inventory import build_demo_asset_inventory, render_markdown


def test_e2e_demo_asset_inventory_orders_required_public_reports() -> None:
    inventory = build_demo_asset_inventory()

    assert inventory["ok"] is True
    assert inventory["horizon"] == "end-to-end-demo-scenario"
    assert inventory["completed_milestone"] == "E2E1"
    assert inventory["next_leaf"] == "E2E2_scenario_contract"
    assert [stage["stage_id"] for stage in inventory["stages"]] == [
        "parser",
        "source_lane",
        "workflow",
        "retriever",
        "operator",
    ]
    assert all(stage["evidence_exists"] for stage in inventory["stages"])


def test_e2e_demo_asset_inventory_markdown_is_public_safe_and_story_driven() -> None:
    rendered = render_markdown(build_demo_asset_inventory())

    assert "E2E1 Demo Asset Inventory" in rendered
    assert "Demo Storyboard" in rendered
    assert "Local Parser Prototype" in rendered
    assert "Controlled Source Lane" in rendered
    assert "Runtime Retriever Promotion Gate" in rendered
    assert "Operator Experience Hardening" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "secret" not in rendered
    assert "kifrs.db" not in rendered
