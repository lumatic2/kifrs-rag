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
