"""분류·면제 판정 (WORKFLOW.md §2A 면제 / §2B 리스제공자 분류) + NeedsHumanReview.

- 이용자: §2A 단기·저가 면제 여부(구조화 입력) → 면제면 사용권자산·리스부채 없이 정액 비용.
- 제공자: §2B 금융/운용 분류는 [1116-62] "위험·보상 대부분 이전" 종합 판단이라 **입력**으로 받는다
  (WA1이 SPPI/사업모형 판단을 evidence로 받은 것과 동일). 엔진은 그 분류에 맞는 측정만 한다.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .schema import ExemptionCase, Lease1116

PathKind = Literal["lessee_recognition", "lessee_exemption", "lessor_finance", "lessor_operating"]


class NeedsHumanReview(Exception):
    """AE1 core pipeline이 자동화하지 않는 케이스.

    동시 확장+축소 변경(scenario_09)처럼 [1116-46(a)] 축소분 PL과 [1116-45]/[1116-46(b)]
    재측정을 2차원으로 분해해야 하는 변경은 단일-차원 변경과 달리 별도 결정 로직이 필요해 이번
    범위 밖이다(docs/plans/2026-07-04-ae1-1116-lease-engine.md 결정 로그). 회귀 하네스는 이
    예외를 "사람 개입 필요"로 집계하고 완료율 계산에서 실패로 세지 않는다(별도 카테고리).
    """

    def __init__(self, special_case: str, label: str):
        self.special_case = special_case
        self.label = label
        super().__init__(f"{label}: special_case={special_case!r} — AE1 core pipeline 밖")


@dataclass
class PathResult:
    path: PathKind
    reasons: list[str]


def classify_path(lease: Lease1116) -> PathResult:
    """식별 이후 진입 경로 결정: 이용자 면제/인식 · 제공자 금융/운용."""
    if lease.party == "lessor":
        if lease.lessor_classification == "finance":
            return PathResult("lessor_finance", ["위험·보상 대부분 이전 → 금융리스 [1116-62, 63]"])
        if lease.lessor_classification == "operating":
            return PathResult("lessor_operating", ["위험·보상 대부분 미이전 → 운용리스 [1116-62]"])
        raise ValueError(f"{lease.label}: 리스제공자는 lessor_classification 필요")

    if lease.exemption_cases:
        return PathResult(
            "lessee_exemption",
            ["단기·소액 기초자산 면제 선택 → 정액 비용, 사용권자산·리스부채 미인식 [1116-5, 6]"],
        )
    return PathResult(
        "lessee_recognition", ["면제 미적용 → 사용권자산·리스부채 인식 [1116-22]"]
    )


@dataclass
class ExemptionExpense:
    label: str
    basis: str
    annual_expense: float
    total_expense: float


def exemption_expenses(cases: list[ExemptionCase]) -> list[ExemptionExpense]:
    """§2A 면제 케이스별 정액 비용 — 월 리스료 × 12(연) / × 총개월(총액)."""
    out: list[ExemptionExpense] = []
    for c in cases:
        annual = c.monthly_payment * 12
        out.append(
            ExemptionExpense(
                label=c.label, basis=c.basis,
                annual_expense=annual, total_expense=c.monthly_payment * c.months,
            )
        )
    return out
