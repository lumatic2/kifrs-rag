"""SPPI 테스트 (WORKFLOW.md §1) — 부채성 자산에만 적용."""
from __future__ import annotations

from dataclasses import dataclass

from .schema import Transaction1109


@dataclass
class SPPIResult:
    passed: bool
    reasons: list[str]


def classify_sppi(txn: Transaction1109) -> SPPIResult:
    """WORKFLOW.md §1 결정트리. 지분증권은 SPPI 대상이 아니다(§1B 별도 분기, `classify.py`)."""
    if txn.instrument_type != "debt":
        raise ValueError("SPPI test applies to debt instruments only (instrument_type='debt')")

    if txn.third_party_credit_linkage:
        return SPPIResult(
            passed=False,
            reasons=["제3자 신용위험 연동(CLN류) — 원금·이자 외 현금흐름 [1109-B4.1.18~19]"],
        )
    if txn.embedded_conversion_option_holder_side:
        return SPPIResult(
            passed=False,
            reasons=["보유자 전환권 — 지분가치 연동, 보유자는 분리 안 함 [1109-4.3.1, B4.1.18(b)]"],
        )
    if txn.has_leverage:
        return SPPIResult(
            passed=False,
            reasons=["레버리지·승수 조항 — 기본 이자 구성요소 초과 [1109-B4.1.16]"],
        )
    if not txn.acceleration_ordinary:
        return SPPIResult(
            passed=False,
            reasons=["비통상적 가속조항 — SPPI 본질을 변경할 위험 [1109-B4.1.10]"],
        )
    return SPPIResult(
        passed=True,
        reasons=["원금+이자만으로 구성, 이자는 기본 구성요소만 반영 [1109-4.1.2(b)/4.1.2A(b), B4.1.7~7B]"],
    )
