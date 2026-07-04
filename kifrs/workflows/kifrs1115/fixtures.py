"""Public 1115 seed fixtures derived from local-only workflow facts.

The private `data/scenarios/1115_revenue/WORKFLOW.md` stays gitignored. These
fixtures keep only invented numbers, branch labels, expected paths, and citation
ids needed for deterministic regression tests.
"""

from dataclasses import dataclass

from .schema import Revenue1115


@dataclass
class ScenarioFixture:
    label: str
    txn: Revenue1115
    expected_path: str
    expected_citations: list[str]


FIXTURES = [
    ScenarioFixture(
        label="scenario_01_renewal_option",
        txn=Revenue1115(
            label="scenario_01_renewal_option",
            scenario_type="customer_option",
            contract_price=1_000_000,
            standalone_selling_price_main=950_000,
            option_standalone_selling_price=100_000,
            option_expected_exercise_probability=0.8,
            has_customer_option=True,
            option_grants_material_right=True,
        ),
        expected_path="material_right_renewal_option",
        expected_citations=["1115-B39~B43", "1115-74"],
    ),
    ScenarioFixture(
        label="scenario_02_discount_right",
        txn=Revenue1115(
            label="scenario_02_discount_right",
            scenario_type="discount_right",
            contract_price=500_000,
            discount_incremental_value=60_000,
            option_expected_exercise_probability=0.7,
            option_grants_material_right=True,
        ),
        expected_path="material_right_discount_option",
        expected_citations=["1115-B40", "1115-B42", "1115-B43", "1115-77"],
    ),
    ScenarioFixture(
        label="scenario_03_significant_financing",
        txn=Revenue1115(
            label="scenario_03_significant_financing",
            scenario_type="significant_financing",
            contract_price=1_100_000,
            has_significant_financing_component=True,
            cash_selling_price=1_000_000,
            promised_consideration=1_100_000,
            financing_months=24,
        ),
        expected_path="significant_financing_component",
        expected_citations=["1115-60", "1115-61", "1115-64", "1115-65", "1115-118"],
    ),
    ScenarioFixture(
        label="scenario_04_repurchase_call_option",
        txn=Revenue1115(
            label="scenario_04_repurchase_call_option",
            scenario_type="repurchase_call_option",
            contract_price=1_000_000,
            entity_call_option=True,
            original_sale_price=1_000_000,
            repurchase_price=1_080_000,
            repurchase_price_includes_time_value=True,
        ),
        expected_path="repurchase_financing_arrangement",
        expected_citations=["1115-B64~B69"],
    ),
]
