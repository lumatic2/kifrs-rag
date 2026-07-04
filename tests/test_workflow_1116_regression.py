"""AE1 Step 10 — 회귀 하네스: 10개 1116 시나리오를 전체 파이프라인으로 실행해 완료율을 잰다.

(docs/plans/2026-07-04-ae1-1116-lease-engine.md 통합 검증 항목)

headline 금액은 시나리오 손계산의 반올림 관행(±1~2원, 시나리오 문서가 명시)을 흡수하기 위해
절대오차 ±2원 tolerance로 비교한다 — fixture 자체가 그 해상도로 검증됐다.
"""
from __future__ import annotations

import pytest

from kifrs.workflows.kifrs1116.fixtures import FIXTURES
from kifrs.workflows.kifrs1116.runner import run_lease

TOLERANCE_WON = 2


@pytest.mark.parametrize("fixture", FIXTURES, ids=lambda f: f.txn.label)
def test_scenario_pipeline_matches_expected(fixture):
    outcome = run_lease(fixture.txn)
    if fixture.expected is None:
        assert outcome.status == "needs_human_review"
        assert outcome.reason  # NeedsHumanReview must explain itself
        return

    assert outcome.status == "automated", outcome.reason
    for key, expected_value in fixture.expected.items():
        got = outcome.headlines.get(key)
        assert got is not None, f"{fixture.txn.label}: headline {key!r} 누락"
        assert abs(got - expected_value) <= TOLERANCE_WON, (
            f"{fixture.txn.label}: {key} 기대 {expected_value} 실제 {got}"
        )
    assert outcome.review_memo is not None
    # §6 검토메모 7섹션 골격 확인
    assert outcome.review_memo.count("## ") == 7


def test_completion_rate():
    """10개 시나리오 전체를 분모로, 사람 개입 없이 headline까지 산출·일치한 비율.

    이 숫자가 바뀌면(파이프라인이 개선/퇴행하면) 이 assert가 알려준다 — AE1이 만든 2번째
    도메인 "시나리오 완료율" 값(docs/OBJECTIVE.md 움직이는 축, 1109=6/10과 비교).
    """
    outcomes = [run_lease(f.txn) for f in FIXTURES]
    automated = [o for o in outcomes if o.status == "automated"]
    needs_review = [o for o in outcomes if o.status == "needs_human_review"]

    assert len(automated) + len(needs_review) == len(FIXTURES) == 10
    assert len(automated) == 9
    assert len(needs_review) == 1
    assert {o.label for o in needs_review} == {
        "scenario_09_lessee_modification_expand_shrink",
    }
