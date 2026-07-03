"""사업모형 평가 (WORKFLOW.md §2) — 부채성 자산에만 적용."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .schema import BusinessModelEvidence

BusinessModel = Literal[1, 2, 3]


@dataclass
class BusinessModelResult:
    model: BusinessModel
    reasons: list[str]


def classify_business_model(evidence: BusinessModelEvidence) -> BusinessModelResult:
    """WORKFLOW.md §2 결정트리 — 매도 빈도·이유, 성과 평가 방식, 보상 구조 종합 판단
    [1109-4.1.1, B4.1.1~6]."""
    if evidence.compensation_trading_linked or evidence.performance_basis == "fv_trading" or evidence.sale_frequency == "frequent":
        return BusinessModelResult(
            model=3,
            reasons=["매매차익 연동 보상 또는 빈번한 매도 또는 공정가치 성과평가 — 매매목적 [1109-B4.1.5~6]"],
        )
    if evidence.sale_frequency == "moderate" or evidence.performance_basis == "fv_mixed":
        return BusinessModelResult(
            model=2,
            reasons=["일정 수준 매도가 모형의 일부, 이자+공정가치 통합 평가 [1109-4.1.2A, B4.1.4~4B]"],
        )
    return BusinessModelResult(
        model=1,
        reasons=["매도 드묾/예외적, 이자수익·신용손실 기준 성과평가 [1109-4.1.1, B4.1.2~3A]"],
    )
