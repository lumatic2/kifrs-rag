"""재평가·변경 처리 (WORKFLOW.md §4A 재평가 / §5 변경).

단일-차원 변경만 자동화한다:
- 이용자 리스기간 재평가 [1116-40] (scenario_07) / 기간 연장 단독 [1116-45·46(b)] (scenario_10)
- 제공자 금융→운용 [1116-80(1)] / 운용→금융 [1116-80] / 금융→금융 [1116-80(2)]

동시 확장+축소(scenario_09)는 [1116-46(a)] 축소분 PL과 [1116-46(b)] 재측정을 2차원으로 분해해야
해 별도 결정 로직이 필요 — schema.special_case로 표시돼 runner가 NeedsHumanReview로 escalate.
각 함수는 headline 금액 dict와 근거(reasons)를 반환한다. 금액은 시나리오가 제시한 현가계수·
할인율로 결정론적으로 재현된다.
"""
from __future__ import annotations

from .amortization import carrying_after, depreciated_carrying
from .measurement import measure_lessee, measure_lessor
from .money import won
from .schema import Lease1116, LeaseEvent


def apply_term_reassessment(lease: Lease1116, event: LeaseEvent) -> tuple[dict, list[str]]:
    """이용자 리스기간 재평가 [1116-40] — 수정 할인율로 잔여 리스료 재측정, 차이는 사용권자산."""
    base = measure_lessee(lease)
    liability_after = carrying_after(
        base.lease_liability, lease.discount_rate, lease.annual_payment, event.periods_elapsed
    )
    rou_after = depreciated_carrying(
        base.rou_asset, base.depreciation_years, event.periods_elapsed
    )
    payment = event.new_annual_payment if event.new_annual_payment is not None else lease.annual_payment
    remeasured_liability = won(payment * event.new_annuity_factor)
    increase = remeasured_liability - liability_after
    remeasured_rou = rou_after + increase
    return (
        {
            "initial_liability": base.lease_liability,
            "liability_after_elapsed": liability_after,
            "rou_after_elapsed": rou_after,
            "remeasured_liability": remeasured_liability,
            "remeasurement_increase": increase,
            "remeasured_rou": remeasured_rou,
        },
        ["리스기간 재평가 — 수정 할인율로 잔여 리스료 재측정, 차이는 사용권자산 조정 [1116-40, 39]"],
    )


def apply_modification_extend(lease: Lease1116, event: LeaseEvent) -> tuple[dict, list[str]]:
    """이용자 기간 연장 단독 [1116-45·46(b)] — 새 할인율로 잔여 PV 재산정, 사용권자산 상응 조정."""
    base = measure_lessee(lease)
    liability_before = carrying_after(
        base.lease_liability, lease.discount_rate, lease.annual_payment, event.periods_elapsed
    )
    rou_before = depreciated_carrying(
        base.rou_asset, base.depreciation_years, event.periods_elapsed
    )
    payment = event.new_annual_payment if event.new_annual_payment is not None else lease.annual_payment
    remeasured_liability = won(payment * event.new_annuity_factor)
    adjustment = remeasured_liability - liability_before
    remeasured_rou = rou_before + adjustment

    y_end_liability = carrying_after(remeasured_liability, event.new_rate, payment, 1)
    y_end_rou = depreciated_carrying(remeasured_rou, event.new_remaining_term, 1)
    return (
        {
            "liability_before_change": liability_before,
            "rou_before_change": rou_before,
            "remeasured_liability": remeasured_liability,
            "remeasurement_adjustment": adjustment,
            "remeasured_rou": remeasured_rou,
            "y_end_liability": y_end_liability,
            "y_end_rou": y_end_rou,
        },
        ["별도 리스 아님(사용권 추가 X) → 새 할인율로 잔여 PV 재산정 + 사용권자산 상응 조정 [1116-45, 46]"],
    )


def apply_lessor_finance_to_operating(lease: Lease1116, event: LeaseEvent) -> tuple[dict, list[str]]:
    """제공자 금융→운용 [1116-80(1)] — 기초자산 장부 = 변경 직전 리스순투자, 변경손익 없음."""
    base = measure_lessor(lease)
    year1_interest = won(base.net_investment * lease.discount_rate)
    receivable_after = carrying_after(
        base.net_investment, lease.discount_rate, lease.annual_payment, event.periods_elapsed
    )
    return (
        {
            "net_investment": base.net_investment,
            "year1_interest_income": year1_interest,
            "operating_lease_asset": receivable_after,
            "modification_gain_loss": 0,
        },
        ["금융→운용 변경 — 변경 유효일부터 새 운용리스, 기초자산 = 리스순투자 잔액, 변경손익 없음 [1116-80]"],
    )


def apply_lessor_operating_to_finance(lease: Lease1116, event: LeaseEvent) -> tuple[dict, list[str]]:
    """제공자 운용→금융 [1116-80] — 운용리스자산 제거, 리스순투자 재측정, 차이는 PL."""
    main_dep = won(lease.asset_cost / lease.asset_useful_life_years)
    idc_dep = won(lease.lessor_initial_direct_costs / lease.lease_term_years)
    year1_depreciation = main_dep + idc_dep
    operating_asset_initial = won(lease.asset_cost) + won(lease.lessor_initial_direct_costs)
    year1_income = lease.annual_payment
    year1_pl = year1_income - year1_depreciation

    asset_carrying = (won(lease.asset_cost) - main_dep) + (
        won(lease.lessor_initial_direct_costs) - idc_dep
    )
    receivable = won(event.new_annual_payment * event.new_annuity_factor)
    if event.new_residual is not None and event.new_residual_factor is not None:
        receivable += won(event.new_residual * event.new_residual_factor)
    modification_loss = receivable - asset_carrying
    return (
        {
            "operating_asset_initial": operating_asset_initial,
            "year1_depreciation": year1_depreciation,
            "year1_pl_effect": year1_pl,
            "operating_asset_carrying_at_change": asset_carrying,
            "lease_receivable": receivable,
            "modification_loss": modification_loss,
        },
        ["운용→금융 변경 — 운용리스자산 제거·리스채권 인식, 차이는 계약조건변경손익 [1116-80, 66]"],
    )


def apply_lessor_finance_to_finance(lease: Lease1116, event: LeaseEvent) -> tuple[dict, list[str]]:
    """제공자 금융→금융(리스료 변경) [1116-80(2)] — 새 할인율로 리스순투자 재측정, 차이 PL."""
    base = measure_lessor(lease)
    receivable_before = carrying_after(
        base.net_investment, lease.discount_rate, lease.annual_payment, event.periods_elapsed
    )
    new_ni = won(event.new_annual_payment * event.new_annuity_factor)
    if event.new_residual is not None and event.new_residual_factor is not None:
        new_ni += won(event.new_residual * event.new_residual_factor)
    modification_loss = new_ni - receivable_before
    year2_interest = won(new_ni * event.new_rate)
    return (
        {
            "receivable_before_change": receivable_before,
            "net_investment_after_change": new_ni,
            "modification_loss": modification_loss,
            "year2_interest_income": year2_interest,
        },
        ["금융→금융 변경 — 새 할인율로 리스순투자 재측정, 차이는 당기손익 [1116-80] [1109-5.4.3]"],
    )


DISPATCH = {
    "term_reassessment": apply_term_reassessment,
    "modification_extend": apply_modification_extend,
    "lessor_finance_to_operating": apply_lessor_finance_to_operating,
    "lessor_operating_to_finance": apply_lessor_operating_to_finance,
    "lessor_finance_to_finance": apply_lessor_finance_to_finance,
}


def apply_event(lease: Lease1116, event: LeaseEvent) -> tuple[dict, list[str]]:
    return DISPATCH[event.kind](lease, event)
