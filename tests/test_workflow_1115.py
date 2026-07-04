"""R15-1 tests for the K-IFRS 1115 revenue engine seed inventory."""

import pytest

from kifrs.workflows.kifrs1115.classify import NeedsHumanReview, evaluate_revenue
from kifrs.workflows.kifrs1115.fixtures import FIXTURES
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


def test_significant_financing_measurement_summary():
    decision = evaluate_revenue(FIXTURES[2].txn)

    assert decision.path == "significant_financing_component"
    assert decision.measurement_summary["cash_selling_price"] == 1_000_000
    assert decision.measurement_summary["promised_consideration"] == 1_100_000
    assert decision.measurement_summary["finance_effect"] == 100_000
    assert decision.measurement_summary["financing_months"] == 24


def test_repurchase_call_option_financing_path():
    decision = evaluate_revenue(FIXTURES[3].txn)

    assert decision.path == "repurchase_financing_arrangement"
    assert decision.measurement_summary["repurchase_spread"] == 80_000
    assert "1115-B64~B69" in decision.citations


def test_needs_human_review_for_missing_repurchase_price():
    txn = Revenue1115(
        label="missing_repurchase_price",
        scenario_type="repurchase_call_option",
        entity_call_option=True,
        original_sale_price=1_000_000,
    )

    with pytest.raises(NeedsHumanReview):
        evaluate_revenue(txn)
