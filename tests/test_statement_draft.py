"""FS2 tests for common financial-statement draft adapters."""

from kifrs.workflows.kifrs1109.fixtures import FIXTURES as FIXTURES_1109
from kifrs.workflows.kifrs1109.review_pack import generate_review_pack as pack_1109
from kifrs.workflows.kifrs1115.fixtures import FIXTURES as FIXTURES_1115
from kifrs.workflows.kifrs1115.review_pack import generate_review_pack as pack_1115
from kifrs.workflows.kifrs1116.fixtures import FIXTURES as FIXTURES_1116
from kifrs.workflows.kifrs1116.review_pack import generate_review_pack as pack_1116
from kifrs.workflows.statement_draft import (
    from_1109_review_pack,
    from_1115_review_pack,
    from_1116_review_pack,
)


def _fixture_1109(label: str):
    return next(f for f in FIXTURES_1109 if f.txn.label == label)


def _fixture_1116(label: str):
    return next(f for f in FIXTURES_1116 if f.txn.label == label)


def test_1109_review_pack_adapts_journal_lines_and_classification_note():
    pack = pack_1109(_fixture_1109("scenario_01_corporate_bond_ac"))
    items = from_1109_review_pack(pack)

    assert any(item.statement == "balance_sheet" and item.line_item == "금융자산(상각후원가)" for item in items)
    assert any(item.line_item == "현금및현금성자산" and item.debit_credit == "credit" for item in items)
    assert any(item.statement == "note" and item.source_field == "classification" for item in items)
    assert all(item.presentation_status == "draft" for item in items)


def test_1109_statement_draft_pilot_includes_subsequent_pl_and_oci_lines():
    ac_pack = pack_1109(_fixture_1109("scenario_01_corporate_bond_ac"))
    ac_items = from_1109_review_pack(ac_pack)

    assert any(item.source_field.startswith("subsequent_entries") for item in ac_items)
    assert any(item.statement == "income_statement" and item.line_item == "이자수익" for item in ac_items)

    fvoci_pack = pack_1109(_fixture_1109("scenario_02_corporate_bond_fvoci"))
    fvoci_items = from_1109_review_pack(fvoci_pack)

    assert any(item.statement == "oci" and "금융자산평가이익" in item.line_item for item in fvoci_items)
    assert any(item.statement == "oci" and "금융자산평가손실" in item.line_item for item in fvoci_items)


def test_1115_review_pack_adapts_revenue_contract_liability_and_measurement_note():
    pack = pack_1115(FIXTURES_1115[0])
    items = from_1115_review_pack(pack)

    assert any(item.statement == "income_statement" and item.line_item == "수익" for item in items)
    assert any(item.statement == "balance_sheet" and item.line_item == "계약부채" for item in items)
    assert any(
        item.statement == "note" and item.source_field == "measurement" and "deferred=" in item.line_item
        for item in items
    )
    assert any(item.review_questions for item in items)


def test_1115_statement_draft_pilot_covers_financing_component_lines():
    pack = pack_1115(FIXTURES_1115[2])
    items = from_1115_review_pack(pack)

    assert any(item.line_item == "매출채권" and item.statement == "balance_sheet" for item in items)
    assert any(item.line_item == "수익" and item.statement == "income_statement" for item in items)
    assert any(item.line_item == "이연금융수익" and item.statement == "balance_sheet" for item in items)
    assert any(item.source_field == "measurement" and "financing=100,000" in item.line_item for item in items)


def test_1115_statement_draft_pilot_covers_repurchase_financing_lines():
    pack = pack_1115(FIXTURES_1115[3])
    items = from_1115_review_pack(pack)

    assert any(item.line_item == "금융부채" and item.statement == "balance_sheet" for item in items)
    assert any(item.line_item == "금융비용" and item.statement == "income_statement" for item in items)
    assert any(
        item.source_field == "measurement" and "repurchase_liability=1,000,000" in item.line_item
        for item in items
    )


def test_1116_review_pack_adapts_lease_asset_liability_and_disclosure_note():
    pack = pack_1116(_fixture_1116("scenario_01_simple_office_lease").txn)
    items = from_1116_review_pack(pack)

    assert any(item.line_item == "사용권자산" and item.statement == "balance_sheet" for item in items)
    assert any(item.line_item == "리스부채" and item.statement == "balance_sheet" for item in items)
    assert any(item.statement == "note" and item.source_field == "disclosure_draft" for item in items)


def test_needs_human_review_pack_generates_needs_review_note_candidate():
    pack = pack_1116(_fixture_1116("scenario_09_lessee_modification_expand_shrink").txn)
    items = from_1116_review_pack(pack)

    assert items
    assert all(item.presentation_status == "needs_human_review" for item in items)
    assert any(item.source_field == "needs_human_review" for item in items)
