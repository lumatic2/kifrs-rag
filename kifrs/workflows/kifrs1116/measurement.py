"""최초 측정 (WORKFLOW.md §3A 이용자 / §3B 제공자).

이용자: 리스부채 PV = 정기리스료 현가(+ 상당히 확실한 매수선택권 행사가 현가) [1116-26/27].
사용권자산 원가 = 리스부채 + 선급 − 인센티브 + 개설직접원가 + 복구원가 PV [1116-24].
제공자 금융: 리스순투자 = 리스료 현가 + 잔존가치 현가 [1116-67]. 제공자 운용: 자산 원가 + 개설직접원가.
"""
from __future__ import annotations

from dataclasses import dataclass

from .money import won
from .schema import Lease1116


@dataclass
class LesseeMeasurement:
    lease_liability: int
    rou_asset: int
    restoration_provision: int
    depreciation_years: int
    annual_depreciation: int
    reasons: list[str]


@dataclass
class LessorMeasurement:
    kind: str  # "finance" | "operating"
    net_investment: int | None = None            # 금융리스
    operating_asset: int | None = None           # 운용리스
    annual_operating_depreciation: int | None = None
    reasons: list[str] = None  # type: ignore[assignment]


def measure_lessee(lease: Lease1116) -> LesseeMeasurement:
    if lease.annual_payment is None or lease.annuity_factor is None:
        raise ValueError(f"{lease.label}: 이용자 최초측정은 annual_payment·annuity_factor 필요")

    liability = won(lease.annual_payment * lease.annuity_factor)
    reasons = ["리스부채 = 정기리스료 현가 [1116-26]"]

    if lease.purchase_option_reasonably_certain and lease.purchase_option_price is not None:
        if lease.purchase_option_factor is None:
            raise ValueError(f"{lease.label}: 매수선택권 반영은 purchase_option_factor 필요")
        liability += won(lease.purchase_option_price * lease.purchase_option_factor)
        reasons.append("상당히 확실한 매수선택권 행사가 현가 리스부채 포함 [1116-27]")

    restoration_pv = 0
    if lease.restoration_future_estimate is not None and lease.restoration_factor is not None:
        restoration_pv = won(lease.restoration_future_estimate * lease.restoration_factor)

    rou = (
        liability
        + won(lease.prepaid_lease_payment)
        - won(lease.lease_incentive_received)
        + won(lease.initial_direct_costs)
        + restoration_pv
    )
    reasons.append("사용권자산 = 리스부채 + 선급 − 인센티브 + 개설직접원가 + 복구원가 현가 [1116-24]")

    # 감가상각 기간: 소유권 이전·매수선택권 상당히 확실 → 내용연수, 그 외 → 리스기간 [1116-32]
    if lease.purchase_option_reasonably_certain and lease.asset_useful_life_years is not None:
        dep_years = lease.asset_useful_life_years
        reasons.append("매수선택권 상당히 확실 → 내용연수 감가 [1116-32]")
    else:
        if lease.lease_term_years is None:
            raise ValueError(f"{lease.label}: 감가 기간 산정에 lease_term_years 필요")
        dep_years = lease.lease_term_years
        reasons.append("소유권 이전·매수선택권 X → 리스기간 감가 [1116-32]")

    annual_dep = won(rou / dep_years)

    return LesseeMeasurement(
        lease_liability=liability, rou_asset=rou, restoration_provision=restoration_pv,
        depreciation_years=dep_years, annual_depreciation=annual_dep, reasons=reasons,
    )


def measure_lessor(lease: Lease1116) -> LessorMeasurement:
    if lease.lessor_classification == "finance":
        if lease.annual_payment is None or lease.annuity_factor is None:
            raise ValueError(f"{lease.label}: 금융리스는 annual_payment·annuity_factor 필요")
        ni = won(lease.annual_payment * lease.annuity_factor)
        if lease.lessor_residual_value is not None and lease.lessor_residual_factor is not None:
            ni += won(lease.lessor_residual_value * lease.lessor_residual_factor)
        return LessorMeasurement(
            kind="finance", net_investment=ni,
            reasons=["리스순투자 = 리스료 현가 + 잔존가치 현가 [1116-67, 70]"],
        )

    # 운용리스: 자산 보유 + 개설직접원가 가산, 정액 감가
    if lease.asset_cost is None:
        raise ValueError(f"{lease.label}: 운용리스는 asset_cost 필요")
    operating_asset = won(lease.asset_cost) + won(lease.lessor_initial_direct_costs)
    return LessorMeasurement(
        kind="operating", operating_asset=operating_asset,
        reasons=["운용리스자산 = 자산 원가 + 개설직접원가 [1116-83, 84]"],
    )
