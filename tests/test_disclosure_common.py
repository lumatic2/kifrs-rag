"""DG2 tests for common disclosure checklist adapters."""

from kifrs.workflows.disclosure import (
    from_1109_review_pack,
    from_1115_review_pack,
    from_1116_requirements,
)
from kifrs.workflows.kifrs1109.fixtures import FIXTURES as FIXTURES_1109
from kifrs.workflows.kifrs1109.review_pack import generate_review_pack as pack_1109
from kifrs.workflows.kifrs1115.fixtures import FIXTURES as FIXTURES_1115
from kifrs.workflows.kifrs1115.review_pack import generate_review_pack as pack_1115


def test_1116_requirements_adapt_to_common_disclosure_items():
    items = from_1116_requirements()

    assert len(items) == 11
    assert sum(item.fill_status == "auto" for item in items) == 8
    assert sum(item.fill_status == "needs_human_review" for item in items) == 3
    assert any(item.item_id == "58" and item.source_field == "maturity" for item in items)


def test_1115_review_pack_adapts_decision_measurement_and_human_items():
    pack = pack_1115(FIXTURES_1115[0])
    items = from_1115_review_pack(pack)

    assert any(item.source_field == "path" and item.fill_status == "auto" for item in items)
    assert any(item.source_field == "measurement" and "deferred=" in item.draft_value for item in items if item.draft_value)
    assert any(item.source_kind == "human_input" for item in items)


def test_1109_review_pack_adapts_classification_and_review_questions():
    pack = pack_1109(FIXTURES_1109[0])
    items = from_1109_review_pack(pack)

    assert any(item.source_field == "classification" and item.draft_value == "AC" for item in items)
    human_items = [item for item in items if item.source_kind == "human_input"]
    assert human_items
    assert any("보유 목적" in required for item in human_items for required in item.required_inputs)
