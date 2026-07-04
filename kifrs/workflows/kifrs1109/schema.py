"""구조화 거래 입력 스키마 (WA1 Step 1).

WORKFLOW.md 결정트리(§0~§6)가 실제로 참조하는 필드만 담는다 — transaction.md의 모든 서술형
항목을 그대로 옮기지 않는다. `assumed_eir`/`PeriodObservation.period_end_fair_value`는
기존 시나리오 관행대로 **입력값**이다(수치해석으로 역산하지 않음 — 계획 단계 확인, docs/plans
/2026-07-03-wa1-1109-pilot-engine.md 참조).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

InstrumentType = Literal["debt", "equity"]
CouponType = Literal["fixed", "floating", "none"]
SaleFrequency = Literal["rare", "moderate", "frequent"]
PerformanceBasis = Literal["interest_ecl", "fv_mixed", "fv_trading"]


@dataclass
class PeriodObservation:
    """기말 관측치 — 표시이자 현금흐름 + (FVOCI/FVPL용) 기말 공정가치."""

    label: str  # 예: "20x1.12.31"
    coupon_cash: float = 0.0
    period_end_fair_value: float | None = None


@dataclass
class BusinessModelEvidence:
    """WORKFLOW.md §2 사업모형 평가 근거 — 부채성 자산에만 적용(지분증권은 §1B 별도 분기)."""

    sale_frequency: SaleFrequency = "rare"
    sale_reasons: list[str] = field(default_factory=list)
    performance_basis: PerformanceBasis = "interest_ecl"
    compensation_trading_linked: bool = False


@dataclass
class Transaction1109:
    """1109 분류·측정 대상 거래 — WA1 core pipeline 입력.

    SPPI-fail을 유발하는 구조적 플래그(embedded_conversion_option 등)는 WA1이 자동화하는
    5개 경로(AC/FVOCI-debt/FVOCI-equity/FVPL via SPPI-fail/FVPL via designation) 중
    "FVPL via SPPI-fail"에 해당하는 것만 자동 처리한다. IFRIC19/재분류/외화/변동금리
    재설정불일치/보유자 전환사채 미분리처럼 별도 결정 로직이 필요한 케이스는
    `special_case`로 명시해 `classify()`가 `NeedsHumanReview`를 던지게 한다.
    """

    label: str
    instrument_type: InstrumentType

    # 부채성 자산 (instrument_type == "debt")
    principal: float | None = None
    coupon_type: CouponType = "fixed"
    coupon_rate: float | None = None  # 연 표시이자율 (fixed일 때)
    maturity_years: float | None = None

    # SPPI 구조적 플래그
    third_party_credit_linkage: bool = False  # CLN류 — 제3자 신용위험 연동
    embedded_conversion_option_holder_side: bool = False  # 보유자 전환권 — 미분리
    has_leverage: bool = False  # 레버리지·승수 조항
    acceleration_ordinary: bool = True  # 통상적 디폴트 가속조항이면 True(SPPI 무해)
    floating_rate_reset_frequency_months: int | None = None
    floating_rate_benchmark_tenor_months: int | None = None
    floating_rate_mismatch_significant: bool | None = None

    # 사업모형 (부채성 자산만)
    business_model: BusinessModelEvidence | None = None

    # 지분증권 (instrument_type == "equity")
    held_for_trading: bool = False
    fvoci_irrevocable_election: bool = False

    # 정책 오버라이드
    fvpl_designation_override: bool = False  # 회계불일치 제거 목적 FVPL 지정 [1109-4.1.5]

    # 이번 범위 밖 특수 케이스 마커 — 지정되면 classify()가 NeedsHumanReview
    special_case: str | None = None  # 예: "ifric19_debt_equity_swap", "reclassification", "fx_dual_track"

    # 금액
    purchase_price: float = 0.0  # 취득 시점 공정가치
    transaction_cost: float = 0.0

    # 후속측정 입력 (주어진 값 — 역산 안 함)
    assumed_eir: float | None = None
    periods: list[PeriodObservation] = field(default_factory=list)
