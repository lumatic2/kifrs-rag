from __future__ import annotations

from scripts.parser_prototype_asset_inventory import build_inventory, render_markdown


def test_parser_prototype_asset_inventory_covers_required_assets() -> None:
    inventory = build_inventory()

    assert inventory["ok"] is True
    assert inventory["active_horizon"] == "real-local-parser-prototype"
    assert inventory["completed_milestone"] == "RLP1"
    assert inventory["next_milestone"] == "RLP2"
    asset_ids = {asset["asset_id"] for asset in inventory["assets"]}
    assert "local-parser-module" in asset_ids
    assert "case-intake-module" in asset_ids
    assert "adapter-contract" in asset_ids
    assert "adapter-scaffold" in asset_ids
    assert "adapter-dry-run-gate" in asset_ids
    assert "deletion-attestation-gate" in asset_ids
    assert "real-adapter-implementation-plan" in asset_ids
    assert inventory["missing_assets"] == []


def test_parser_prototype_asset_inventory_defines_rlp2_to_rlp5_gaps() -> None:
    inventory = build_inventory()

    assert set(inventory["rlp_gaps"]) == {"RLP2", "RLP3", "RLP4", "RLP5"}
    assert "structured facts" in inventory["rlp_gaps"]["RLP2"]
    assert "deletion" in inventory["rlp_gaps"]["RLP3"].lower()
    assert "leak tests" in inventory["rlp_gaps"]["RLP4"]
    assert "close gate" in inventory["rlp_gaps"]["RLP5"]


def test_parser_prototype_asset_inventory_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_inventory())

    assert "RLP1 Parser Prototype Asset Inventory" in rendered
    assert "Asset Inventory" in rendered
    assert "RLP2-RLP5 Gaps" in rendered
    assert "real client files" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
