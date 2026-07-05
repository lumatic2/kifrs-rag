from __future__ import annotations

from scripts.firm_facing_product_surface_inventory import build_inventory, render_markdown


def test_firm_facing_product_surface_inventory_selects_first_demo_flow() -> None:
    inventory = build_inventory()

    assert inventory["ok"] is True
    assert inventory["recommended_flow"]["id"] == "lease-review-pack-authority-private-boundary"
    paths = {surface["path"] for surface in inventory["surfaces"]}
    assert "scripts/multi_authority_runtime_gate.py" in paths
    assert "scripts/client_private_parser_runtime_gate.py" in paths
    assert "kifrs/workflows/kifrs1116/review_pack.py" in paths
    assert inventory["next_leaf"] == "FPS2_operator_demo_command"


def test_firm_facing_product_surface_inventory_classifies_gaps() -> None:
    inventory = build_inventory()
    milestones = {gap["milestone"] for gap in inventory["gaps"]}

    assert {"FPS2", "FPS3", "FPS4", "FPS5"}.issubset(milestones)


def test_firm_facing_product_surface_inventory_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_inventory())

    assert "FPS1 Product Surface Inventory" in rendered
    assert "Recommended First Demo Flow" in rendered
    assert "source_body" not in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
