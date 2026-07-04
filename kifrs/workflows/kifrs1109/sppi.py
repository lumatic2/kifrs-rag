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
    if _has_floating_rate_mismatch(txn):
        if txn.floating_rate_mismatch_significant is None:
            return SPPIResult(
                passed=False,
                reasons=[
                    "변동금리 재설정 주기와 기준금리 테너 불일치 — benchmark cash flow 비교 필요 [1109-B4.1.7~7B]"
                ],
            )
        if txn.floating_rate_mismatch_significant:
            return SPPIResult(
                passed=False,
                reasons=[
                    "변동금리 재설정 불일치 효과가 유의적 — 기본 이자 구성요소 초과 [1109-B4.1.7~7B]"
                ],
            )
        return SPPIResult(
            passed=True,
            reasons=[
                "변동금리 재설정 주기와 기준금리 테너가 다르지만 benchmark cash flow 비교상 유의적 변형 없음 [1109-B4.1.7~7B]"
            ],
        )
    return SPPIResult(
        passed=True,
        reasons=["원금+이자만으로 구성, 이자는 기본 구성요소만 반영 [1109-4.1.2(b)/4.1.2A(b), B4.1.7~7B]"],
    )


def _has_floating_rate_mismatch(txn: Transaction1109) -> bool:
    if txn.coupon_type != "floating":
        return False
    if txn.floating_rate_reset_frequency_months is None:
        return False
    if txn.floating_rate_benchmark_tenor_months is None:
        return False
    return txn.floating_rate_reset_frequency_months != txn.floating_rate_benchmark_tenor_months
