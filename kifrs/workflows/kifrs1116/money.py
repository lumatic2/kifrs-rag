"""원 단위 반올림 헬퍼.

시나리오 fixture는 회계 관행대로 **round-half-up**(사사오입)으로 손계산됐다(예: 유효이자
177,297.5 → 177,298, 136,162.5 → 136,163). Python 내장 `round()`는 banker's rounding(round
half to even)이라 .5 케이스에서 fixture와 어긋난다 — 그래서 `Decimal(ROUND_HALF_UP)`로 원
단위 정수 반올림을 강제한다.
"""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal


def won(amount: float) -> int:
    """원 단위 정수로 round-half-up 반올림."""
    return int(Decimal(str(amount)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
