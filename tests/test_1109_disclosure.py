"""DG4 tests for 1109 disclosure skeleton generation."""

from kifrs.workflows.kifrs1109.disclosure import generate_disclosure_skeleton
from kifrs.workflows.kifrs1109.fixtures import FIXTURES
from kifrs.workflows.kifrs1109.review_pack import generate_review_pack


def _fixture(label: str):
    return next(f for f in FIXTURES if f.txn.label == label)


def test_1109_disclosure_skeleton_contains_classification_and_human_questions():
    skeleton = generate_disclosure_skeleton(_fixture("scenario_01_corporate_bond_ac"))

    assert "# 금융상품 주석 skeleton" in skeleton
    assert "## 1. 자동 산출 후보" in skeleton
    assert "금융상품 분류: AC" in skeleton
    assert "## 2. 사람 보완 필요" in skeleton
    assert "회사 보유 목적과 회계정책 확인" in skeleton
    assert "금융상품 보유 목적 문서" in skeleton
    assert "[1109-4.1.2]" in skeleton


def test_1109_disclosure_skeleton_accepts_review_pack():
    pack = generate_review_pack(_fixture("scenario_03_credit_linked_note_fvpl"))
    skeleton = generate_disclosure_skeleton(pack)

    assert "금융상품 분류: FVPL" in skeleton
    assert "후속측정 입력값 검토" in skeleton


def test_1109_disclosure_skeleton_for_needs_human_review_pack():
    skeleton = generate_disclosure_skeleton(
        _fixture("scenario_06_floating_rate_bond_sppi_nuance")
    )

    assert "자동 산출 후보 없음" in skeleton
    assert "변동금리 재설정 불일치 SPPI 판단" in skeleton
    assert "재설정 주기" in skeleton
    assert "benchmark cash flow" in skeleton
