from __future__ import annotations

from scripts.product_trust_evidence_inventory import build_inventory, render_markdown


def test_product_trust_evidence_inventory_classifies_sources() -> None:
    inventory = build_inventory()

    assert inventory["ok"] is True
    assert inventory["horizon"] == "product-trust-and-quality-evidence"
    assert inventory["milestone"] == "PTQ1"
    assert inventory["missing"] == []
    assert "quality preflight" in inventory["categories"]["fast_public_safe"]
    assert "RAG quality final gate" in inventory["categories"]["heavy_regression"]
    assert "default retriever guard" in {source["name"] for source in inventory["sources"]}


def test_product_trust_evidence_inventory_points_to_next_gaps() -> None:
    inventory = build_inventory()
    milestones = {gap["milestone"] for gap in inventory["gaps"]}

    assert {"PTQ2", "PTQ3", "PTQ4", "PTQ5"}.issubset(milestones)
    assert inventory["next_leaf"] == "PTQ2_review_pack_confidence_contract"


def test_product_trust_evidence_inventory_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_inventory())

    assert "PTQ1 Trust Evidence Inventory" in rendered
    assert "Protected Data Required" in rendered
    assert "api_key" not in rendered
    assert "source_body" not in rendered
