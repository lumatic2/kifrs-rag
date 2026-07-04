"""R15-1 tests for the K-IFRS 1115 revenue engine seed inventory."""

import pytest

from kifrs.workflows.kifrs1115.classify import NeedsHumanReview, evaluate_revenue
from kifrs.workflows.kifrs1115.fixtures import FIXTURES
from kifrs.workflows.kifrs1115.journal_entry import draft_journal_entries
from kifrs.workflows.kifrs1115.measurement import measure_revenue
from kifrs.workflows.kifrs1115.review_memo import SECTION_TITLES, generate_review_memo
from kifrs.workflows.kifrs1115.schema import Revenue1115


def test_1115_fixture_inventory_has_four_seed_scenarios():
    assert [fixture.label for fixture in FIXTURES] == [
        "scenario_01_renewal_option",
        "scenario_02_discount_right",
        "scenario_03_significant_financing",
        "scenario_04_repurchase_call_option",
    ]


def test_1115_decision_matches_expected_paths_and_citations():
    for fixture in FIXTURES:
        decision = evaluate_revenue(fixture.txn)
        assert decision.status == "automated"
        assert decision.path == fixture.expected_path
        assert decision.citations == fixture.expected_citations
        assert decision.performance_obligations
        assert decision.reasons


def test_1115_decision_contains_five_step_assessment():
    for fixture in FIXTURES:
        decision = evaluate_revenue(fixture.txn)

        assert [step.step for step in decision.five_step] == [1, 2, 3, 4, 5]
        assert [step.name for step in decision.five_step] == [
            "contract_identification",
            "performance_obligations",
            "transaction_price",
            "allocate_transaction_price",
            "recognize_revenue",
        ]
        assert all(step.conclusion for step in decision.five_step)
        assert all(step.citations for step in decision.five_step)


def test_material_right_five_step_defers_option_right():
    decision = evaluate_revenue(FIXTURES[0].txn)

    assert decision.five_step[1].conclusion == "current goods or services; material right"
    assert decision.five_step[3].conclusion == "relative standalone selling price including the option right"
    assert "defer the material right" in decision.five_step[4].conclusion


def test_significant_financing_measurement_summary():
    decision = evaluate_revenue(FIXTURES[2].txn)

    assert decision.path == "significant_financing_component"
    assert decision.measurement_summary["cash_selling_price"] == 1_000_000
    assert decision.measurement_summary["promised_consideration"] == 1_100_000
    assert decision.measurement_summary["finance_effect"] == 100_000
    assert decision.measurement_summary["financing_months"] == 24
    assert "cash selling price 1,000,000" in decision.five_step[2].conclusion
    assert "24 months" in decision.five_step[4].conclusion


def test_repurchase_call_option_financing_path():
    decision = evaluate_revenue(FIXTURES[3].txn)

    assert decision.path == "repurchase_financing_arrangement"
    assert decision.measurement_summary["repurchase_spread"] == 80_000
    assert "1115-B64~B69" in decision.citations
    assert decision.five_step[3].conclusion == (
        "repurchase arrangement classification before revenue recognition"
    )
    assert "financing" in decision.five_step[4].conclusion


def test_needs_human_review_for_missing_repurchase_price():
    txn = Revenue1115(
        label="missing_repurchase_price",
        scenario_type="repurchase_call_option",
        entity_call_option=True,
        original_sale_price=1_000_000,
    )

    with pytest.raises(NeedsHumanReview):
        evaluate_revenue(txn)


def test_needs_human_review_when_contract_identification_fails():
    txn = Revenue1115(
        label="missing_contract_identification",
        scenario_type="customer_option",
        contract_identified=False,
        has_customer_option=True,
        option_grants_material_right=True,
        option_standalone_selling_price=100_000,
    )

    with pytest.raises(NeedsHumanReview):
        evaluate_revenue(txn)


def test_material_right_measurement_allocates_contract_price():
    measurement = measure_revenue(FIXTURES[0].txn)

    assert measurement.path == "material_right_renewal_option"
    assert round(measurement.recognized_revenue, 2) == 922_330.1
    assert round(measurement.deferred_revenue, 2) == 77_669.9
    assert sum(line.allocated_transaction_price for line in measurement.allocation) == pytest.approx(
        1_000_000
    )


def test_discount_right_measurement_uses_expected_incremental_discount():
    measurement = measure_revenue(FIXTURES[1].txn)

    assert measurement.path == "material_right_discount_option"
    assert measurement.deferred_revenue == pytest.approx(38_745.387, abs=0.001)
    assert measurement.recognized_revenue + measurement.deferred_revenue == pytest.approx(
        500_000
    )


def test_significant_financing_entry_balances_and_defers_financing_income():
    entries = draft_journal_entries(FIXTURES[2].txn)

    assert len(entries) == 1
    entry = entries[0]
    assert entry.total_debit == entry.total_credit
    assert entry.total_debit == 1_100_000
    assert [(line.account, line.debit, line.credit) for line in entry.lines] == [
        ("매출채권", 1_100_000, 0.0),
        ("수익", 0.0, 1_000_000),
        ("이연금융수익", 0.0, 100_000),
    ]


def test_repurchase_financing_entries_do_not_recognize_revenue():
    measurement = measure_revenue(FIXTURES[3].txn)
    entries = draft_journal_entries(FIXTURES[3].txn, measurement=measurement)

    assert measurement.recognized_revenue == 0
    assert measurement.repurchase_liability == 1_000_000
    assert measurement.financing_effect == 80_000
    assert len(entries) == 2
    assert all(entry.total_debit == entry.total_credit for entry in entries)
    assert all(
        line.account != "수익"
        for entry in entries
        for line in entry.lines
    )


def test_review_memo_contains_all_sections_and_five_step_assessment():
    memo = generate_review_memo(FIXTURES[0].txn)

    for idx, title in enumerate(SECTION_TITLES, start=1):
        assert f"## {idx}. {title}" in memo
    assert "Step 1 contract_identification" in memo
    assert "Step 5 recognize_revenue" in memo
    assert "계약부채(중요한 권리)" in memo
    assert "1115-B39~B43" in memo


def test_review_memo_renders_repurchase_without_revenue_line():
    memo = generate_review_memo(FIXTURES[3].txn)

    assert "재매입약정 초안" in memo
    assert "금융부채" in memo
    assert "재매입스프레드 초안" in memo
    assert "(대) 수익" not in memo
