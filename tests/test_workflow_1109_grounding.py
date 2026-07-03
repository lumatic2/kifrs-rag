"""RGA1 — 런타임 citation 존재 검증 (docs/plans/2026-07-03-rga1-runtime-citation-grounding.md)."""
from __future__ import annotations

import pytest

from kifrs.workflows.kifrs1109.classify import NeedsHumanReview, classify
from kifrs.workflows.kifrs1109.grounding import (
    GroundingFailure,
    extract_citations,
    ground_reasons,
    verify_citation_exists,
)
from kifrs.workflows.kifrs1109.schema import BusinessModelEvidence, Transaction1109


@pytest.mark.parametrize(
    "reason,expected",
    [
        (
            "제3자 신용위험 연동(CLN류) — 원금·이자 외 현금흐름 [1109-B4.1.18~19]",
            ["1109-B4.1.18~19"],
        ),
        (
            "보유자 전환권 — 지분가치 연동, 보유자는 분리 안 함 [1109-4.3.1, B4.1.18(b)]",
            ["1109-4.3.1", "1109-B4.1.18(b)"],
        ),
        (
            "원금+이자만으로 구성, 이자는 기본 구성요소만 반영 [1109-4.1.2(b)/4.1.2A(b), B4.1.7~7B]",
            ["1109-4.1.2(b)", "1109-4.1.2A(b)", "1109-B4.1.7~7B"],
        ),
        ("인용 없는 서술문", []),
    ],
)
def test_extract_citations(reason, expected):
    assert extract_citations(reason) == expected


@pytest.mark.parametrize(
    "token,base_no",
    [
        ("1109-4.1.2(b)", "4.1.2"),
        ("1109-4.1.2A(b)", "4.1.2A"),
        ("1109-B4.1.18~19", "B4.1.18"),
        ("1109-B4.1.7~7B", "B4.1.7"),
    ],
)
def test_verify_citation_exists_true_for_real_paragraphs(token, base_no):
    check = verify_citation_exists(token)
    assert check.exists is True
    assert check.base_no == base_no


def test_verify_citation_exists_false_for_fake_paragraph():
    check = verify_citation_exists("1109-99.99.99")
    assert check.exists is False


def test_ground_reasons_passes_for_real_citations():
    ground_reasons(["SPPI Pass + 사업모형1(수취) [1109-4.1.2]"])  # no exception


def test_ground_reasons_raises_for_missing_citation():
    with pytest.raises(GroundingFailure):
        ground_reasons(["가짜 인용 [1109-99.99.99]"])


def _debt_txn(**overrides):
    defaults = dict(
        label="grounding_test",
        instrument_type="debt",
        principal=1_000_000,
        acceleration_ordinary=True,
        business_model=BusinessModelEvidence(sale_frequency="rare"),
        purchase_price=1_000_000,
    )
    defaults.update(overrides)
    return Transaction1109(**defaults)


def test_classify_grounds_hardcoded_citations_for_real_transaction():
    """classify()의 모든 return 경로가 실제 하드코딩 인용으로 grounding을 통과하는지
    (AC 경로 — sppi.reasons + business_model.reasons + 자체 reasons 모두 검증됨)."""
    result = classify(_debt_txn())
    assert result.classification == "AC"


def test_classify_escalates_to_needs_human_review_on_bad_citation(monkeypatch):
    """하드코딩 인용이 깨졌다고 가정(monkeypatch)하면 classify()가 NeedsHumanReview로
    에스컬레이션한다 — grounding 실패가 조용히 통과하지 않는지 확인."""
    import kifrs.workflows.kifrs1109.classify as classify_module

    def _bad_core(txn):
        from kifrs.workflows.kifrs1109.classify import ClassificationResult

        return ClassificationResult("AC", ["가짜 인용 [1109-99.99.99]"])

    monkeypatch.setattr(classify_module, "_classify_core", _bad_core)

    with pytest.raises(NeedsHumanReview) as exc_info:
        classify(_debt_txn())
    assert exc_info.value.special_case == "citation_grounding_failed"
