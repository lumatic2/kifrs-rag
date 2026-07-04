"""F-ACC review pack composition tests for K-IFRS 1109."""
from __future__ import annotations

from kifrs.workflows.kifrs1109.fixtures import FIXTURES
from kifrs.workflows.kifrs1109.review_pack import (
    generate_review_pack,
    render_review_pack_markdown,
)


def _fixture(label: str):
    return next(f for f in FIXTURES if f.txn.label == label)


def test_automated_1109_review_pack_contains_core_sections():
    pack = generate_review_pack(_fixture("scenario_01_corporate_bond_ac"))

    assert pack.standard == "KIFRS1109"
    assert pack.status == "automated"
    assert pack.classification == "AC"
    assert pack.journal_entry is not None
    assert pack.review_memo and "검토 메모" in pack.review_memo
    assert any(item.label == "SPPI/사업모형 판단" for item in pack.review_checklist)
    assert any(action.issue == "후속측정 입력값 검토" for action in pack.needs_human_review)
    assert "[1109-4.1.2]" in pack.citations

    rendered = render_review_pack_markdown(pack)
    assert "# F-ACC Review Pack" in rendered
    assert "## 1. 검토메모" in rendered
    assert "## 2. 분개 초안" in rendered
    assert "## 3. 리뷰 체크리스트" in rendered
    assert "유효이자율" in rendered


def test_needs_human_review_1109_pack_explains_special_case():
    pack = generate_review_pack(_fixture("scenario_06_floating_rate_bond_sppi_nuance"))

    assert pack.status == "needs_human_review"
    assert pack.classification is None
    assert pack.review_memo is None
    assert pack.journal_entry is None
    assert pack.review_checklist[0].status == "needs_human_review"

    action = pack.needs_human_review[0]
    assert "SPPI" in action.issue
    assert any("재설정 주기" in item for item in action.required_inputs)
    assert any("benchmark cash flow" in item for item in action.review_questions)
    assert any("[1109-B4.1.7~7B]" in item for item in action.candidate_guidance)

    rendered = render_review_pack_markdown(pack)
    assert "변동금리 재설정 불일치 SPPI 판단" in rendered
    assert "필요한 추가자료" in rendered
    assert "리뷰 질문" in rendered


def test_all_1109_fixtures_generate_review_pack_statuses():
    packs = [generate_review_pack(f) for f in FIXTURES]

    automated = [p for p in packs if p.status == "automated"]
    needs_review = [p for p in packs if p.status == "needs_human_review"]

    assert len(packs) == 10
    assert len(automated) == 6
    assert len(needs_review) == 4
    assert {p.case_id for p in needs_review} == {
        "scenario_05_ifric19_debt_equity_swap",
        "scenario_06_floating_rate_bond_sppi_nuance",
        "scenario_08_business_model_change_reclassification",
        "scenario_10_foreign_currency_bond_1109_1021",
    }
    assert all(p.judgment_summary for p in packs)
