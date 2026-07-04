"""F-ACC review pack composition tests for K-IFRS 1115."""

from kifrs.workflows.kifrs1115.fixtures import FIXTURES
from kifrs.workflows.kifrs1115.review_pack import (
    generate_review_pack,
    render_review_pack_markdown,
)
from kifrs.workflows.kifrs1115.schema import Revenue1115


def test_automated_1115_review_pack_contains_core_sections():
    pack = generate_review_pack(FIXTURES[0])

    assert pack.standard == "KIFRS1115"
    assert pack.status == "automated"
    assert pack.path == "material_right_renewal_option"
    assert pack.measurement is not None
    assert pack.journal_entries
    assert pack.review_memo and "검토 메모" in pack.review_memo
    assert any(item.label == "5단계 판단" for item in pack.review_checklist)
    assert any(action.issue == "입력 사실과 추정치 검토" for action in pack.needs_human_review)
    assert "1115-B39~B43" in pack.citations

    rendered = render_review_pack_markdown(pack)
    assert "# F-ACC Review Pack" in rendered
    assert "## 1. 검토메모" in rendered
    assert "## 2. 분개 초안" in rendered
    assert "## 3. 리뷰 체크리스트" in rendered
    assert "계약부채(중요한 권리)" in rendered


def test_needs_human_review_1115_pack_explains_missing_input():
    txn = Revenue1115(
        label="missing_financing_facts",
        scenario_type="significant_financing",
        has_significant_financing_component=True,
    )
    pack = generate_review_pack(txn)

    assert pack.status == "needs_human_review"
    assert pack.path is None
    assert pack.review_memo is None
    assert not pack.journal_entries
    assert pack.review_checklist[0].status == "needs_human_review"

    action = pack.needs_human_review[0]
    assert "1115 자동 판단 중단" in action.issue
    assert any("거래가격" in item for item in action.required_inputs)

    rendered = render_review_pack_markdown(pack)
    assert "필요한 추가자료" in rendered
    assert "리뷰 질문" in rendered


def test_all_1115_fixtures_generate_automated_review_packs():
    packs = [generate_review_pack(fixture) for fixture in FIXTURES]

    assert len(packs) == 4
    assert all(pack.status == "automated" for pack in packs)
    assert all(pack.judgment_summary for pack in packs)
    assert all(pack.review_memo for pack in packs)
    assert sum(len(pack.journal_entries) for pack in packs) == 5
