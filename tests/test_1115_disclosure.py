"""DG3 tests for 1115 disclosure skeleton generation."""

from kifrs.workflows.kifrs1115.disclosure import generate_disclosure_skeleton
from kifrs.workflows.kifrs1115.fixtures import FIXTURES
from kifrs.workflows.kifrs1115.review_pack import generate_review_pack
from kifrs.workflows.kifrs1115.schema import Revenue1115


def test_1115_disclosure_skeleton_contains_auto_and_human_sections():
    skeleton = generate_disclosure_skeleton(FIXTURES[0])

    assert "# 수익인식 주석 skeleton" in skeleton
    assert "## 1. 자동 산출 후보" in skeleton
    assert "수익인식 판단 경로" in skeleton
    assert "수익 및 이연/금융요소 측정" in skeleton
    assert "## 2. 사람 보완 필요" in skeleton
    assert "입력 사실과 추정치 검토" in skeleton
    assert "1115-B39~B43" in skeleton


def test_1115_disclosure_skeleton_accepts_review_pack():
    pack = generate_review_pack(FIXTURES[2])
    skeleton = generate_disclosure_skeleton(pack)

    assert "significant_financing_component" in skeleton
    assert "financing=100,000" in skeleton


def test_1115_disclosure_skeleton_for_needs_human_review_pack():
    txn = Revenue1115(
        label="missing_financing_facts",
        scenario_type="significant_financing",
        has_significant_financing_component=True,
    )
    skeleton = generate_disclosure_skeleton(txn)

    assert "자동 산출 후보 없음" in skeleton
    assert "1115 자동 판단 중단" in skeleton
    assert "거래가격 입력값" in skeleton
