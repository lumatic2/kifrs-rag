"""리스 식별 판정 (WORKFLOW.md §1) — 계약이 리스인가.

[1116-9] 식별되는 자산 + 사용 통제권(경제적 효익 + 사용 지시) 이전이면 리스. 공급자에게
실질적 대체권이 있으면 식별 실패(서비스 계약).
"""
from __future__ import annotations

from dataclasses import dataclass

from .schema import Lease1116


@dataclass
class IdentificationResult:
    is_lease: bool
    reasons: list[str]


def identify_lease(lease: Lease1116) -> IdentificationResult:
    """§1 결정트리: 식별자산 → 실질적 대체권 부재 → 통제권(효익+지시) 이전."""
    if not lease.identified_asset:
        return IdentificationResult(False, ["식별되는 자산 없음 → 리스 아님 [1116-9]"])
    if lease.supplier_substantive_substitution_right:
        return IdentificationResult(
            False, ["공급자 실질적 대체권 존재 → 식별 실패, 서비스 계약 [1116-9]"]
        )
    if not (lease.lessee_gets_economic_benefits and lease.lessee_directs_use):
        return IdentificationResult(
            False, ["사용 통제권 미이전(효익·지시 권리 미충족) → 서비스 계약 [1116-9]"]
        )
    return IdentificationResult(
        True, ["식별되는 자산 + 사용 통제권(효익+지시) 이전 → 리스 [1116-9]"]
    )
