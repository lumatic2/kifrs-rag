"""후속측정 계산 (WORKFLOW.md §5) — 주어진 `assumed_eir`/`period_end_fair_value`로 결정론적 산술.

AC/FVOCI(부채): 유효이자율법 상각표. `effective_interest = round(opening_bv * eir)`,
`amortization = effective_interest - coupon_cash`. FVOCI는 추가로 (기말FV − AC상각후잔액)을
누적 OCI로, 전기 대비 증분을 그 기의 OCI 조정으로 계산한다.

FVPL/FVOCI(자본): EIR 상각이 아니라 표시이자(명목)를 그대로 이자수익으로, 기말FV 변동을
그대로 손익/OCI로 인식한다 — WORKFLOW.md §5 FVPL/FVOCI(자본) 절.
"""
from __future__ import annotations

from dataclasses import dataclass

from .classify import Classification
from .schema import PeriodObservation, Transaction1109


@dataclass
class AmortizationRow:
    """AC/FVOCI(부채) 상각표 1행."""

    label: str
    opening_bv: float
    coupon_cash: float
    effective_interest: float
    amortization: float
    closing_ac_bv: float
    closing_fair_value: float | None = None
    oci_cumulative: float | None = None
    oci_delta: float | None = None


@dataclass
class RevaluationRow:
    """FVPL/FVOCI(자본) 기말 평가 1행 — EIR 상각 없이 표시이자 + FV 변동만."""

    label: str
    coupon_cash: float
    opening_fair_value: float
    closing_fair_value: float
    fv_delta: float


def amortize_ac_or_fvoci_debt(
    txn: Transaction1109, classification: Classification
) -> list[AmortizationRow]:
    if classification not in ("AC", "FVOCI_DEBT"):
        raise ValueError(f"amortize_ac_or_fvoci_debt는 AC/FVOCI_DEBT 전용, got {classification!r}")
    if txn.assumed_eir is None:
        raise ValueError(f"{txn.label}: assumed_eir가 없으면 상각표를 계산할 수 없음")

    eir = txn.assumed_eir
    opening = txn.purchase_price + txn.transaction_cost
    prev_oci_cumulative = 0.0
    rows: list[AmortizationRow] = []

    for period in txn.periods:
        effective_interest = round(opening * eir)
        amortization = effective_interest - period.coupon_cash
        closing_ac = opening + amortization

        closing_fv = None
        oci_cumulative = None
        oci_delta = None
        if classification == "FVOCI_DEBT":
            if period.period_end_fair_value is None:
                raise ValueError(f"{txn.label}/{period.label}: FVOCI_DEBT는 period_end_fair_value 필요")
            closing_fv = period.period_end_fair_value
            oci_cumulative = closing_fv - closing_ac
            oci_delta = oci_cumulative - prev_oci_cumulative
            prev_oci_cumulative = oci_cumulative

        rows.append(AmortizationRow(
            label=period.label, opening_bv=opening, coupon_cash=period.coupon_cash,
            effective_interest=effective_interest, amortization=amortization,
            closing_ac_bv=closing_ac, closing_fair_value=closing_fv,
            oci_cumulative=oci_cumulative, oci_delta=oci_delta,
        ))
        opening = closing_ac

    return rows


def revalue_fvpl_or_fvoci_equity(
    txn: Transaction1109, classification: Classification
) -> list[RevaluationRow]:
    if classification not in ("FVPL", "FVOCI_EQUITY"):
        raise ValueError(f"revalue_fvpl_or_fvoci_equity는 FVPL/FVOCI_EQUITY 전용, got {classification!r}")

    opening_fv = txn.purchase_price
    rows: list[RevaluationRow] = []
    for period in txn.periods:
        if period.period_end_fair_value is None:
            raise ValueError(f"{txn.label}/{period.label}: {classification}는 period_end_fair_value 필요")
        closing_fv = period.period_end_fair_value
        rows.append(RevaluationRow(
            label=period.label, coupon_cash=period.coupon_cash,
            opening_fair_value=opening_fv, closing_fair_value=closing_fv,
            fv_delta=closing_fv - opening_fv,
        ))
        opening_fv = closing_fv
    return rows
