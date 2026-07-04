"""AE1 Step 9 — 런타임 citation 존재 검증 (RGA1 미러, 1109 grounding 테스트 구조 복제).

optimistic-path 금지(docs/plans/2026-07-04-ae1-1116-lease-engine.md): 존재하지 않는 조항을
인용하면 run_lease()가 NeedsHumanReview로 escalate하는 negative 경로를 함께 검증한다.
"""
from __future__ import annotations

import pytest

from kifrs.workflows.kifrs1116.grounding import (
    GroundingFailure,
    extract_citations,
    ground_reasons,
    verify_citation_exists,
)
from kifrs.workflows.kifrs1116.runner import run_lease
from kifrs.workflows.kifrs1116.schema import Lease1116


@pytest.mark.parametrize(
    "reason,expected",
    [
        ("리스부채 = 정기리스료 현가 [1116-26]", ["1116-26"]),
        ("사용권자산 원가 4구성요소 [1116-24]", ["1116-24"]),
        ("금융→금융 변경 [1116-80] [1109-5.4.3]", ["1116-80", "1109-5.4.3"]),
        ("매수선택권 상당히 확실 → 내용연수 감가 [1116-32]", ["1116-32"]),
        ("인용 없는 서술문", []),
    ],
)
def test_extract_citations(reason, expected):
    assert extract_citations(reason) == expected


@pytest.mark.parametrize(
    "token,base_no",
    [
        ("1116-24", "24"),
        ("1116-46(a)", "46"),
        ("1116-46(b)", "46"),
        ("1116-23~24", "23"),
    ],
)
def test_verify_citation_exists_true_for_real_paragraphs(token, base_no):
    check = verify_citation_exists(token)
    assert check.exists is True
    assert check.base_no == base_no


def test_verify_citation_exists_false_for_fake_paragraph():
    check = verify_citation_exists("1116-99.99.99")
    assert check.exists is False


def test_ground_reasons_passes_for_real_citations():
    ground_reasons(["사용권자산 = 리스부채 + 선급 − 인센티브 + 개설직접원가 + 복구원가 현가 [1116-24]"])


def test_ground_reasons_raises_for_missing_citation():
    with pytest.raises(GroundingFailure):
        ground_reasons(["가짜 인용 [1116-99.99.99]"])


def _lessee_txn(**overrides):
    defaults = dict(
        label="grounding_test", party="lessee",
        annual_payment=1_000_000, lease_term_years=4, discount_rate=0.05,
        annuity_factor=3.54595,
    )
    defaults.update(overrides)
    return Lease1116(**defaults)


def test_run_lease_grounds_hardcoded_citations_for_real_transaction():
    """run_lease()의 모든 reasons(식별·분류·측정 인용)가 실제 DB 조항으로 grounding을 통과."""
    outcome = run_lease(_lessee_txn())
    assert outcome.status == "automated"
    assert outcome.path == "lessee_recognition"


def test_run_lease_escalates_to_needs_human_review_on_bad_citation(monkeypatch):
    """측정 reason에 깨진 인용이 섞이면 run_lease()가 NeedsHumanReview로 escalate."""
    import kifrs.workflows.kifrs1116.runner as runner_module
    from kifrs.workflows.kifrs1116.measurement import LesseeMeasurement

    def _bad_measure(lease):
        return LesseeMeasurement(
            lease_liability=1, rou_asset=1, restoration_provision=0,
            depreciation_years=4, annual_depreciation=1,
            reasons=["가짜 인용 [1116-99.99.99]"],
        )

    monkeypatch.setattr(runner_module, "measure_lessee", _bad_measure)
    outcome = run_lease(_lessee_txn())
    assert outcome.status == "needs_human_review"
    assert "citation_grounding_failed" in outcome.reason
