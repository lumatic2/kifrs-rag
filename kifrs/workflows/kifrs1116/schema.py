"""구조화 거래 입력 스키마 (AE1 Step 1).

WORKFLOW.md 결정트리(§0~§6)가 실제로 참조하는 필드만 담는다 — transaction.md의 모든 서술형
항목을 그대로 옮기지 않는다. 할인율 현가계수(`annuity_factor`/`single_factor`)와 리스제공자
분류, 변경 유형은 시나리오가 제시한 **입력값**이다(WA1의 assumed_eir/SPPI 판단과 동일 — 엔진은
수치해석·판단을 하지 않고 주어진 값으로 결정론적 산술만 한다, docs/plans/2026-07-04-ae1-1116-
lease-engine.md 결정 로그).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Party = Literal["lessee", "lessor"]
PaymentTiming = Literal["arrears", "advance"]
LessorClass = Literal["finance", "operating"]
EventKind = Literal[
    "term_reassessment",       # §4A 리스기간 재평가 [1116-40] (이용자)
    "modification_extend",     # §5 기간 연장 단독 [1116-45/46(b)] (이용자)
    "lessor_finance_to_operating",   # §5 [1116-80(1)] (제공자)
    "lessor_operating_to_finance",   # §5 [1116-80] (제공자)
    "lessor_finance_to_finance",     # §5 [1116-80(2)] (제공자)
]


@dataclass
class ExemptionCase:
    """§2A 단기·저가 면제 하위 케이스 — 사용권자산·리스부채 없이 리스료를 정액 비용 인식."""

    label: str
    monthly_payment: float
    months: int
    basis: Literal["short_term", "low_value"]


@dataclass
class LeaseEvent:
    """§4A 재평가 / §5 변경 이벤트 — 변경 유효일과 새 조건(입력값)."""

    kind: EventKind
    effective: str                         # 예: "20x2.1.1"
    periods_elapsed: int = 0               # 변경 전 경과(상각·감가) 기간 수
    new_rate: float | None = None
    new_remaining_term: int | None = None
    new_annuity_factor: float | None = None
    new_annual_payment: float | None = None
    new_residual: float | None = None
    new_residual_factor: float | None = None


@dataclass
class Lease1116:
    """1116 리스 거래 — AE1 core pipeline 입력.

    동시 확장+축소 변경(scenario_09)처럼 별도 결정 로직이 필요한 케이스는 `special_case`로
    명시해 `run_lease()`가 `NeedsHumanReview`를 던지게 한다.
    """

    label: str
    party: Party

    # 식별 (§1) — 구조적 사실
    identified_asset: bool = True
    supplier_substantive_substitution_right: bool = False
    lessee_gets_economic_benefits: bool = True
    lessee_directs_use: bool = True

    # 면제 (§2A, 이용자)
    exemption_cases: list[ExemptionCase] = field(default_factory=list)

    # 리스료·할인율
    annual_payment: float | None = None
    lease_term_years: int | None = None
    discount_rate: float | None = None
    annuity_factor: float | None = None        # 리스료 정상연금 현가계수 (rate·term)
    payment_timing: PaymentTiming = "arrears"

    # 옵션 (이용자)
    purchase_option_price: float | None = None
    purchase_option_reasonably_certain: bool = False
    purchase_option_factor: float | None = None   # 매수선택권 행사가 단일현가계수
    asset_useful_life_years: int | None = None

    # 사용권자산 원가 구성 (§3A, 이용자) [1116-24]
    prepaid_lease_payment: float = 0.0
    lease_incentive_received: float = 0.0
    initial_direct_costs: float = 0.0
    restoration_future_estimate: float | None = None
    restoration_factor: float | None = None       # 복구원가 단일현가계수

    # 리스제공자 (§2B/§3B)
    lessor_classification: LessorClass | None = None   # 판단 결과(입력)
    asset_cost: float | None = None
    lessor_residual_value: float | None = None
    lessor_residual_factor: float | None = None
    lessor_initial_direct_costs: float = 0.0

    # 재평가·변경 이벤트 (§4A/§5)
    events: list[LeaseEvent] = field(default_factory=list)

    # 이번 범위 밖 특수 케이스 마커 — 지정되면 run_lease()가 NeedsHumanReview
    special_case: str | None = None
