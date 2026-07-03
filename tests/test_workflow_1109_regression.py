"""WA1 Step 8 — 회귀 하네스: 10개 1109 시나리오를 전체 파이프라인으로 실행해 완료율을 잰다.

(docs/plans/2026-07-03-wa1-1109-pilot-engine.md 통합 검증 항목)
"""
from __future__ import annotations

import pytest

from kifrs.workflows.kifrs1109.fixtures import FIXTURES
from kifrs.workflows.kifrs1109.runner import run_scenario


@pytest.mark.parametrize("fixture", FIXTURES, ids=lambda f: f.txn.label)
def test_scenario_pipeline_matches_expected(fixture):
    outcome = run_scenario(fixture)
    if fixture.expected_classification is None:
        assert outcome.status == "needs_human_review"
        assert outcome.reason  # NeedsHumanReview must explain itself
    else:
        assert outcome.status == "automated"
        assert outcome.classification == fixture.expected_classification
        assert outcome.initial_total == fixture.expected_initial_total
        assert outcome.review_memo is not None


def test_completion_rate():
    """10개 시나리오 전체를 분모로, 사람 개입 없이 끝까지 산출된 비율.

    이 숫자가 바뀌면(파이프라인이 개선/퇴행하면) 이 assert가 알려준다 — WA1이 처음 만든
    측정 가능한 "시나리오 완료율" 값(docs/OBJECTIVE.md 움직이는 축).
    """
    outcomes = [run_scenario(f) for f in FIXTURES]
    automated = [o for o in outcomes if o.status == "automated"]
    needs_review = [o for o in outcomes if o.status == "needs_human_review"]

    assert len(automated) + len(needs_review) == len(FIXTURES) == 10
    assert len(automated) == 6
    assert len(needs_review) == 4
    assert {o.label for o in needs_review} == {
        "scenario_05_ifric19_debt_equity_swap",
        "scenario_06_floating_rate_bond_sppi_nuance",
        "scenario_08_business_model_change_reclassification",
        "scenario_10_foreign_currency_bond_1109_1021",
    }
