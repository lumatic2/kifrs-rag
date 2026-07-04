"""Measurement draft helpers for 1115 revenue decisions."""

from dataclasses import dataclass, field

from .classify import RevenueDecision, evaluate_revenue
from .schema import Revenue1115


@dataclass
class AllocationLine:
    obligation: str
    standalone_selling_price: float
    allocated_transaction_price: float


@dataclass
class RevenueMeasurement:
    label: str
    path: str
    recognized_revenue: float = 0.0
    deferred_revenue: float = 0.0
    financing_effect: float = 0.0
    repurchase_liability: float = 0.0
    allocation: list[AllocationLine] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def measure_revenue(
    txn: Revenue1115, decision: RevenueDecision | None = None
) -> RevenueMeasurement:
    decision = decision or evaluate_revenue(txn)

    if decision.path == "material_right_renewal_option":
        return _measure_customer_option(txn, decision)
    if decision.path == "material_right_discount_option":
        return _measure_discount_right(txn, decision)
    if decision.path == "significant_financing_component":
        return _measure_significant_financing(txn, decision)
    if decision.path in {"repurchase_financing_arrangement", "repurchase_lease_arrangement"}:
        return _measure_repurchase(txn, decision)

    raise ValueError(f"{txn.label}: unsupported 1115 path={decision.path!r}")


def _measure_customer_option(
    txn: Revenue1115, decision: RevenueDecision
) -> RevenueMeasurement:
    option_ssp = _expected_option_ssp(
        txn.option_standalone_selling_price or 0.0,
        txn.option_expected_exercise_probability,
    )
    main_ssp = txn.standalone_selling_price_main or max(txn.contract_price - option_ssp, 0.0)
    return _allocate_material_right(
        txn=txn,
        decision=decision,
        main_obligation="current goods or services",
        right_obligation="material right",
        main_ssp=main_ssp,
        right_ssp=option_ssp,
    )


def _measure_discount_right(
    txn: Revenue1115, decision: RevenueDecision
) -> RevenueMeasurement:
    right_ssp = _expected_option_ssp(
        txn.discount_incremental_value or 0.0,
        txn.option_expected_exercise_probability,
    )
    main_ssp = max(txn.contract_price, 0.0)
    return _allocate_material_right(
        txn=txn,
        decision=decision,
        main_obligation="current sale",
        right_obligation="discount material right",
        main_ssp=main_ssp,
        right_ssp=right_ssp,
    )


def _allocate_material_right(
    txn: Revenue1115,
    decision: RevenueDecision,
    main_obligation: str,
    right_obligation: str,
    main_ssp: float,
    right_ssp: float,
) -> RevenueMeasurement:
    total_ssp = main_ssp + right_ssp
    if total_ssp <= 0:
        raise ValueError(f"{txn.label}: material-right allocation requires positive SSP")

    main_alloc = txn.contract_price * main_ssp / total_ssp
    right_alloc = txn.contract_price - main_alloc
    return RevenueMeasurement(
        label=txn.label,
        path=decision.path,
        recognized_revenue=main_alloc,
        deferred_revenue=right_alloc,
        allocation=[
            AllocationLine(main_obligation, main_ssp, main_alloc),
            AllocationLine(right_obligation, right_ssp, right_alloc),
        ],
        notes=[
            "Relative SSP allocation separates current revenue from the material-right contract liability."
        ],
    )


def _measure_significant_financing(
    txn: Revenue1115, decision: RevenueDecision
) -> RevenueMeasurement:
    cash_price = float(decision.measurement_summary["cash_selling_price"])
    promised = float(decision.measurement_summary["promised_consideration"])
    financing_effect = promised - cash_price
    return RevenueMeasurement(
        label=txn.label,
        path=decision.path,
        recognized_revenue=cash_price,
        financing_effect=financing_effect,
        notes=[
            "Revenue is measured at the cash selling price; the difference is presented as financing."
        ],
    )


def _measure_repurchase(
    txn: Revenue1115, decision: RevenueDecision
) -> RevenueMeasurement:
    liability = txn.original_sale_price or txn.contract_price
    spread = (txn.repurchase_price or liability) - liability
    return RevenueMeasurement(
        label=txn.label,
        path=decision.path,
        recognized_revenue=0.0,
        financing_effect=max(spread, 0.0),
        repurchase_liability=liability,
        notes=[
            "Entity call option blocks ordinary sale accounting until the repurchase arrangement is resolved."
        ],
    )


def _expected_option_ssp(amount: float, probability: float | None) -> float:
    return amount * (probability if probability is not None else 1.0)
