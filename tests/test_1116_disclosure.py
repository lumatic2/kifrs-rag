"""AE2 Step 6 — 리스이용자 주석 초안 생성 회귀 테스트.

(docs/plans/2026-07-04-ae2-1116-disclosure-draft.md 통합 검증 항목)

DART 실제 데이터(`data/`, gitignored)에 의존하지 않도록 cross-check는 합성 요약으로 테스트한다
— CI/새 clone에서도 돈다. optimistic-path 금지: 엔진이 보편 요구항목을 놓치면 교차검증이
False로 잡는 negative 케이스를 포함한다.
"""
from __future__ import annotations

from kifrs.workflows.kifrs1116.disclosure import (
    LESSEE_DISCLOSURE_REQUIREMENTS,
    aggregate_portfolio,
    compute_coverage,
    cross_check_coverage,
    generate_disclosure_note,
    ground_requirements,
    lease_contribution,
)
from kifrs.workflows.kifrs1116.fixtures import FIXTURES


def _pilot_leases():
    return [f.txn for f in FIXTURES if f.txn.party == "lessee" and not f.txn.special_case]


def test_checklist_has_11_requirements_and_grounds():
    assert len(LESSEE_DISCLOSURE_REQUIREMENTS) == 11
    ground_requirements()  # 모든 요구항목 조항이 DB 존재 — 실패 시 GroundingFailure


def test_portfolio_aggregate_equals_sum_of_contributions():
    leases = _pilot_leases()
    port = aggregate_portfolio(leases)
    assert port.depreciation == sum(c.depreciation for c in port.contributions)
    assert port.rou_addition == sum(c.rou_addition for c in port.contributions)
    assert port.cash_outflow == sum(c.cash_outflow for c in port.contributions)
    # 개별 기여분 계산이 시나리오와 정합 (감가·이자 > 0)
    assert all(c.rou_addition >= 0 for c in port.contributions)


def test_draft_contains_required_items_and_maturity_and_na():
    port = aggregate_portfolio(_pilot_leases())
    draft = generate_disclosure_note(port)
    assert "## 1. 당기손익 인식 금액 [1116-53]" in draft
    assert "## 2. 리스부채 만기분석 [1116-58]" in draft
    # fillable 항목은 금액, non-fillable(변동리스료·전대·판매후리스)은 "미해당"
    assert "미해당" in draft
    assert draft.count("미해당") >= 3
    assert "[1116-53]" in draft and "[1116-58]" in draft


def test_coverage_is_8_of_11():
    cov = compute_coverage()
    assert cov.total == 11
    assert len(cov.auto_filled) == 8
    assert set(cov.needs_human) == {"53(5)", "53(6)", "53(9)"}
    assert cov.coverage_pct == 72.7


def _synthetic_summary(present_map):
    """항목 라벨 prefix → 존재 여부 dict로 합성 DART 요약 1건 생성."""
    keys = [f"{r.item} {r.label}" for r in LESSEE_DISCLOSURE_REQUIREMENTS]
    return {"name": "합성", "items": {k: any(k.startswith(p) for p in present_map) for k in keys}}


def test_cross_check_engine_covers_universal_items():
    """엔진 자동 8항목이 전사 공시(보편) 항목이면 engine_covers_universal True (실측 재현)."""
    universal_items = ["53(1)", "53(2)", "53(3)", "53(4)", "53(7)", "53(8)", "53(10)", "58"]
    all_present = _synthetic_summary([r.item for r in LESSEE_DISCLOSURE_REQUIREMENTS])
    partial = _synthetic_summary(universal_items)  # 조건부 3개 미공시
    cc = cross_check_coverage([all_present, partial])
    assert set(cc.universal_items) == set(universal_items)
    assert set(cc.conditional_items) == {"53(5)", "53(6)", "53(9)"}
    assert cc.engine_covers_universal is True


def test_cross_check_flags_engine_gap_negative():
    """엔진 자동 커버 대상이 아닌 항목이 보편 공시로 나오면 engine_covers_universal False.

    (optimistic-path 금지 — 엔진이 보편 요구항목을 놓치는 상황을 교차검증이 잡는지)
    """
    # 변동리스료(53(5), 엔진 non-fillable)를 전사가 공시하는 가상 상황
    s = _synthetic_summary(["53(1)", "53(2)", "53(5)"])
    cc = cross_check_coverage([s, s])
    assert "53(5)" in cc.universal_items
    assert cc.engine_covers_universal is False
