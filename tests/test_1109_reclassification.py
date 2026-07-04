"""FH3 tests for 1109 reclassification review-memo skeleton."""

from kifrs.workflows.kifrs1109.fixtures import FIXTURES
from kifrs.workflows.kifrs1109.reclassification import (
    SECTION_TITLES,
    generate_reclassification_memo,
)
from kifrs.workflows.kifrs1109.review_pack import (
    generate_review_pack,
    render_review_pack_markdown,
)


def _fixture(label: str):
    return next(f for f in FIXTURES if f.txn.label == label)


def test_reclassification_memo_contains_all_skeleton_sections():
    memo = generate_reclassification_memo(
        _fixture("scenario_08_business_model_change_reclassification").txn
    )

    for idx, title in enumerate(SECTION_TITLES, start=1):
        assert f"## {idx}. {title}" in memo
    assert "사업모형 변경 승인 자료" in memo
    assert "재분류일 공정가치" in memo
    assert "전진 적용" in memo


def test_reclassification_review_pack_includes_skeleton_memo():
    pack = generate_review_pack(_fixture("scenario_08_business_model_change_reclassification"))

    assert pack.status == "needs_human_review"
    assert pack.review_memo is not None
    assert "1109 재분류 검토메모 skeleton" in pack.review_memo
    assert pack.journal_entry is None

    rendered = render_review_pack_markdown(pack)
    assert "## 1. 검토메모" in rendered
    assert "기존 장부금액과 유효이자율" in rendered
    assert "실제 사업 활동 변경" in rendered
