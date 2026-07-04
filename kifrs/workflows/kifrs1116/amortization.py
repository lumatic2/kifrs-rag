"""후속측정 상각·감가 계산 (WORKFLOW.md §4A 이용자 / §4B 제공자).

리스부채·리스채권 상각표: 기간 이자 = round_half_up(기초 × 이자율), 원금 = 리스료 − 이자,
기말 = 기초 + 이자 − 리스료. 사용권자산·운용리스자산 감가: 정액, 장부금액은 원가 −
누적감가(round_half_up(원가 × 경과/총기간))로 계산한다(fixture의 누적 반올림 방식과 일치).
"""
from __future__ import annotations

from dataclasses import dataclass

from .money import won


@dataclass
class AmortizationRow:
    """리스부채/리스채권 상각표 1행."""

    label: str
    opening: int
    interest: int
    payment: float
    closing: int


def amortize(opening: int, rate: float, payment: float, periods: int,
             start_index: int = 1) -> list[AmortizationRow]:
    """유효이자율 상각표 — 부채/채권 공통. closing = opening + interest − payment."""
    rows: list[AmortizationRow] = []
    balance = opening
    for i in range(periods):
        interest = won(balance * rate)
        closing = balance + interest - int(round(payment))
        rows.append(AmortizationRow(
            label=f"기{start_index + i}", opening=balance, interest=interest,
            payment=payment, closing=closing,
        ))
        balance = closing
    return rows


def carrying_after(opening_balance: int, rate: float, payment: float, periods: int) -> int:
    """`periods`기 상각 후 리스부채/채권 잔액."""
    if periods == 0:
        return opening_balance
    return amortize(opening_balance, rate, payment, periods)[-1].closing


def straight_line_depreciation(cost: int, total_years: int, elapsed_years: int) -> int:
    """정액 감가 누계 — round_half_up(원가 × 경과/총기간). fixture 누적 방식과 일치."""
    return won(cost * elapsed_years / total_years)


def depreciated_carrying(cost: int, total_years: int, elapsed_years: int) -> int:
    """정액 감가 후 장부금액 = 원가 − 누적감가."""
    return cost - straight_line_depreciation(cost, total_years, elapsed_years)
