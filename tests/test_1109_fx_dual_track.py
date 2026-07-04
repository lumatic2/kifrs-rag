"""FH4 tests for 1109+1021 FX dual-track boundary memo."""

from kifrs.workflows.kifrs1109.fixtures import FIXTURES
from kifrs.workflows.kifrs1109.fx_dual_track import (
    SECTION_TITLES,
    generate_fx_dual_track_memo,
)
from kifrs.workflows.kifrs1109.review_pack import (
    generate_review_pack,
    render_review_pack_markdown,
)


def _fixture(label: str):
    return next(f for f in FIXTURES if f.txn.label == label)


def test_fx_dual_track_memo_contains_1109_and_1021_sections():
    memo = generate_fx_dual_track_memo(_fixture("scenario_10_foreign_currency_bond_1109_1021").txn)

    for idx, title in enumerate(SECTION_TITLES, start=1):
        assert f"## {idx}. {title}" in memo
    assert "SPPI 판단 입력" in memo
    assert "기능통화" in memo
    assert "보고일 환율" in memo
    assert "공정가치 변동" in memo


def test_fx_dual_track_review_pack_includes_boundary_memo():
    pack = generate_review_pack(_fixture("scenario_10_foreign_currency_bond_1109_1021"))

    assert pack.status == "needs_human_review"
    assert pack.review_memo is not None
    assert "1109+1021 외화 금융상품 boundary memo" in pack.review_memo
    assert pack.journal_entry is None

    rendered = render_review_pack_markdown(pack)
    assert "취득일 환율" in rendered
    assert "FVOCI 부채상품" in rendered
    assert "기능통화 판단" in rendered
