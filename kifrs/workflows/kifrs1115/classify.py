"""First-pass 1115 decision-path classifier for R15-1."""

from dataclasses import dataclass, field
from typing import Literal

from .schema import Revenue1115

DecisionStatus = Literal["automated", "needs_human_review"]


class NeedsHumanReview(Exception):
    """Raised when R15-1 does not have enough structured facts for a path."""


@dataclass
class RevenueDecision:
    label: str
    status: DecisionStatus
    path: str
    performance_obligations: list[str] = field(default_factory=list)
    allocation_basis: str = ""
    measurement_summary: dict[str, float | int | str] = field(default_factory=dict)
    reasons: list[str] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)


def evaluate_revenue(txn: Revenue1115) -> RevenueDecision:
    """Return a deterministic 1115 decision path for supported seed patterns."""

    if txn.special_case:
        raise NeedsHumanReview(f"{txn.label}: special_case={txn.special_case}")

    if txn.scenario_type == "customer_option":
        return _customer_option(txn)
    if txn.scenario_type == "discount_right":
        return _discount_right(txn)
    if txn.scenario_type == "significant_financing":
        return _significant_financing(txn)
    if txn.scenario_type == "repurchase_call_option":
        return _repurchase_call_option(txn)

    raise NeedsHumanReview(f"{txn.label}: unsupported scenario_type={txn.scenario_type!r}")


def _customer_option(txn: Revenue1115) -> RevenueDecision:
    if not (txn.has_customer_option and txn.option_grants_material_right):
        raise NeedsHumanReview(f"{txn.label}: customer option material-right facts missing")
    if txn.option_standalone_selling_price is None:
        raise NeedsHumanReview(f"{txn.label}: option standalone selling price missing")
    return RevenueDecision(
        label=txn.label,
        status="automated",
        path="material_right_renewal_option",
        performance_obligations=["current goods or services", "material right"],
        allocation_basis="relative standalone selling price including the option right",
        measurement_summary={
            "contract_price": txn.contract_price,
            "option_standalone_selling_price": txn.option_standalone_selling_price,
            "option_expected_exercise_probability": txn.option_expected_exercise_probability
            or 0.0,
        },
        reasons=[
            "Customer option grants an incremental right that is treated as a separate performance obligation.",
            "Transaction price allocation is needed between current delivery and the material right.",
        ],
        citations=["1115-B39~B43", "1115-74"],
    )


def _discount_right(txn: Revenue1115) -> RevenueDecision:
    if not txn.option_grants_material_right:
        raise NeedsHumanReview(f"{txn.label}: discount option material-right conclusion missing")
    if txn.discount_incremental_value is None:
        raise NeedsHumanReview(f"{txn.label}: incremental discount value missing")
    return RevenueDecision(
        label=txn.label,
        status="automated",
        path="material_right_discount_option",
        performance_obligations=["current sale", "discount material right"],
        allocation_basis="standalone selling price of the incremental discount right",
        measurement_summary={
            "contract_price": txn.contract_price,
            "discount_incremental_value": txn.discount_incremental_value,
            "option_expected_exercise_probability": txn.option_expected_exercise_probability
            or 0.0,
        },
        reasons=[
            "The discount exceeds a normal marketing discount and is modeled as a material right.",
            "The material right is measured from the incremental discount expected to be used.",
        ],
        citations=["1115-B40", "1115-B42", "1115-B43", "1115-77"],
    )


def _significant_financing(txn: Revenue1115) -> RevenueDecision:
    if not txn.has_significant_financing_component:
        raise NeedsHumanReview(f"{txn.label}: significant financing flag missing")
    if txn.cash_selling_price is None or txn.promised_consideration is None:
        raise NeedsHumanReview(f"{txn.label}: financing measurement facts missing")

    finance_effect = txn.promised_consideration - txn.cash_selling_price
    return RevenueDecision(
        label=txn.label,
        status="automated",
        path="significant_financing_component",
        performance_obligations=["promised goods or services"],
        allocation_basis="transaction price adjusted to cash selling price",
        measurement_summary={
            "cash_selling_price": txn.cash_selling_price,
            "promised_consideration": txn.promised_consideration,
            "finance_effect": finance_effect,
            "financing_months": txn.financing_months or 0,
        },
        reasons=[
            "Timing between payment and transfer creates a financing effect.",
            "Revenue measurement starts from the cash selling price, with financing presented separately.",
        ],
        citations=["1115-60", "1115-61", "1115-64", "1115-65", "1115-118"],
    )


def _repurchase_call_option(txn: Revenue1115) -> RevenueDecision:
    if not txn.entity_call_option:
        raise NeedsHumanReview(f"{txn.label}: entity call option fact missing")
    if txn.original_sale_price is None or txn.repurchase_price is None:
        raise NeedsHumanReview(f"{txn.label}: repurchase price facts missing")

    if txn.repurchase_price >= txn.original_sale_price:
        path = "repurchase_financing_arrangement"
        summary = "call option repurchase price equals or exceeds original selling price"
    else:
        path = "repurchase_lease_arrangement"
        summary = "call option repurchase price is below original selling price"

    return RevenueDecision(
        label=txn.label,
        status="automated",
        path=path,
        performance_obligations=["sale with repurchase right assessment"],
        allocation_basis="repurchase arrangement classification before revenue recognition",
        measurement_summary={
            "original_sale_price": txn.original_sale_price,
            "repurchase_price": txn.repurchase_price,
            "repurchase_spread": txn.repurchase_price - txn.original_sale_price,
        },
        reasons=[
            "Entity-controlled call option prevents treating the transfer as an ordinary sale without repurchase analysis.",
            summary,
        ],
        citations=["1115-B64~B69"],
    )
