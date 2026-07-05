from __future__ import annotations

from scripts.non_ifrs_source_asset_inventory import build_inventory, render_markdown


def test_nis1_inventory_classifies_reusable_assets_by_lane() -> None:
    inventory = build_inventory()

    assert inventory["ok"], inventory["errors"]
    assert inventory["milestone"] == "NIS1"
    assert inventory["next_leaf"] == "NIS2_source_record_contract"
    assert set(inventory["lanes"]) == {
        "document_metadata",
        "law_locator",
        "structured_fact",
        "client_private",
        "policy_and_gate",
    }
    assert inventory["reusable_asset_count"] >= 20
    for lane in inventory["lanes"].values():
        assert lane["reusable_assets"]
        assert all(asset["exists"] for asset in lane["reusable_assets"])
        assert lane["build_next"]
        assert lane["excluded_from_active_implementation"]


def test_nis1_inventory_markdown_is_public_safe_and_decision_oriented() -> None:
    rendered = render_markdown(build_inventory())

    assert "NIS1 Source Asset Inventory" in rendered
    assert "document_metadata" in rendered
    assert "structured_fact" in rendered
    assert "client_private" in rendered
    assert "NIS2_source_record_contract" in rendered
    assert "api_key" not in rendered.lower()
    assert "token" not in rendered.lower()
    assert "credential" not in rendered.lower()
    assert "source_body" not in rendered.lower()
