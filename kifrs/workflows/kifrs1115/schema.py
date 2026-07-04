"""Structured input schema for K-IFRS 1115 revenue scenarios."""

from dataclasses import dataclass
from typing import Literal

ScenarioType = Literal[
    "customer_option",
    "discount_right",
    "significant_financing",
    "repurchase_call_option",
]


@dataclass
class Revenue1115:
    """Minimal public facts needed for the first 1115 decision branches."""

    label: str
    scenario_type: ScenarioType
    contract_price: float = 0.0
    standalone_selling_price_main: float | None = None
    option_standalone_selling_price: float | None = None
    option_expected_exercise_probability: float | None = None
    discount_incremental_value: float | None = None
    has_customer_option: bool = False
    option_grants_material_right: bool = False
    has_significant_financing_component: bool = False
    cash_selling_price: float | None = None
    promised_consideration: float | None = None
    financing_months: int | None = None
    entity_call_option: bool = False
    original_sale_price: float | None = None
    repurchase_price: float | None = None
    repurchase_price_includes_time_value: bool = False
    special_case: str | None = None
