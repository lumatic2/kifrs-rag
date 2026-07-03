"""분류 매트릭스 (WORKFLOW.md §0·§1B·§3) — SPPI × 사업모형 × 지분/오버라이드 종합 판단."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .business_model import BusinessModelResult, classify_business_model
from .schema import Transaction1109
from .sppi import SPPIResult, classify_sppi

Classification = Literal["AC", "FVOCI_DEBT", "FVOCI_EQUITY", "FVPL"]


class NeedsHumanReview(Exception):
    """이번 WA1 core pipeline이 자동화하지 않는 특수 케이스(§0 사전분기 밖).

    IFRIC19 발행자 부채소멸, SPPI 변동금리 재설정 불일치, 보유자 전환사채 미분리
    특례 확인, 재분류, 외화 이중트랙 등 — 각자 별도 결정 로직이 필요해 이번 범위 밖이다
    (docs/plans/2026-07-03-wa1-1109-pilot-engine.md 결정 로그 참조). 회귀 하네스는 이 예외를
    "사람 개입 필요"로 집계하고 완료율 계산에서 실패로 세지 않는다(별도 카테고리).
    """

    def __init__(self, special_case: str, label: str):
        self.special_case = special_case
        self.label = label
        super().__init__(f"{label}: special_case={special_case!r} — WA1 core pipeline 밖")


@dataclass
class ClassificationResult:
    classification: Classification
    reasons: list[str]
    sppi: SPPIResult | None = None
    business_model: BusinessModelResult | None = None


def classify(txn: Transaction1109) -> ClassificationResult:
    """WORKFLOW.md §0(자산유형 사전분기) → §1(SPPI, 부채성만) → §1B(지분증권) → §3(매트릭스)."""
    if txn.special_case:
        raise NeedsHumanReview(txn.special_case, txn.label)

    if txn.instrument_type == "equity":
        if txn.held_for_trading:
            return ClassificationResult(
                "FVPL", ["매매목적 지분증권 — FVOCI 선택 불가 [1109-4.1.4]"],
            )
        if txn.fvoci_irrevocable_election:
            return ClassificationResult(
                "FVOCI_EQUITY",
                ["매매목적 아님 + 취소불가능 FVOCI 선택 [1109-4.1.4, 5.7.5]"],
            )
        return ClassificationResult(
            "FVPL", ["지분증권 기본 분류 — FVOCI 미선택 [1109-4.1.4]"],
        )

    sppi = classify_sppi(txn)
    if not sppi.passed:
        return ClassificationResult("FVPL", sppi.reasons, sppi=sppi)

    if txn.fvpl_designation_override:
        return ClassificationResult(
            "FVPL",
            ["회계불일치 제거 목적 취소불가능 FVPL 지정 [1109-4.1.5]"],
            sppi=sppi,
        )

    if txn.business_model is None:
        raise ValueError(f"{txn.label}: debt instrument classification requires business_model evidence")
    bm = classify_business_model(txn.business_model)

    if bm.model == 1:
        return ClassificationResult(
            "AC", ["SPPI Pass + 사업모형1(수취) [1109-4.1.2]"], sppi=sppi, business_model=bm,
        )
    if bm.model == 2:
        return ClassificationResult(
            "FVOCI_DEBT", ["SPPI Pass + 사업모형2(수취+매도) [1109-4.1.2A]"], sppi=sppi, business_model=bm,
        )
    return ClassificationResult(
        "FVPL", ["SPPI Pass이나 사업모형3(매매·기타) [1109-4.1.4]"], sppi=sppi, business_model=bm,
    )
