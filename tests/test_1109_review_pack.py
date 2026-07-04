"""F-ACC review pack composition tests for K-IFRS 1109."""
from __future__ import annotations

from kifrs.workflows.kifrs1109.fixtures import FIXTURES
from kifrs.runtime.evidence import load_runtime_evidence
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
    pack = generate_review_pack(_fixture("scenario_08_business_model_change_reclassification"))

    assert pack.status == "needs_human_review"
    assert pack.classification is None
    assert pack.review_memo and "1109 재분류 검토메모 skeleton" in pack.review_memo
    assert pack.journal_entry is None
    assert pack.review_checklist[0].status == "needs_human_review"

    action = pack.needs_human_review[0]
    assert "재분류" in action.issue
    assert any("사업모형 변경 승인 자료" in item for item in action.required_inputs)
    assert any("전진 적용" in item for item in action.review_questions)

    rendered = render_review_pack_markdown(pack)
    assert "사업모형 변경에 따른 재분류" in rendered
    assert "필요한 추가자료" in rendered
    assert "리뷰 질문" in rendered


def test_floating_rate_reset_mismatch_is_hardened_to_automated_pack():
    pack = generate_review_pack(_fixture("scenario_06_floating_rate_bond_sppi_nuance"))

    assert pack.status == "automated"
    assert pack.classification == "AC"
    assert pack.journal_entry is not None
    assert pack.review_memo and "benchmark cash flow 비교상 유의적 변형 없음" in pack.review_memo


def test_all_1109_fixtures_generate_review_pack_statuses():
    packs = [generate_review_pack(f) for f in FIXTURES]

    automated = [p for p in packs if p.status == "automated"]
    needs_review = [p for p in packs if p.status == "needs_human_review"]

    assert len(packs) == 10
    assert len(automated) == 7
    assert len(needs_review) == 3
    assert {p.case_id for p in needs_review} == {
        "scenario_05_ifric19_debt_equity_swap",
        "scenario_08_business_model_change_reclassification",
        "scenario_10_foreign_currency_bond_1109_1021",
    }
    assert all(p.judgment_summary for p in packs)


def test_1109_review_pack_renders_external_evidence_panel_without_body_text():
    pack = generate_review_pack(_fixture("scenario_01_corporate_bond_ac"), load_runtime_evidence())

    rendered = render_review_pack_markdown(pack)

    assert "## 외부 근거" in rendered
    assert "### 수치 사실 근거" in rendered
    assert "synthetic-dart-2025-annual-001-revenue" in rendered
    assert "copied source" not in rendered
