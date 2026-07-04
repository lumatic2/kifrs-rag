"""RP1 — F-ACC review pack composition tests."""
from __future__ import annotations

from kifrs.workflows.kifrs1116.fixtures import FIXTURES
from kifrs.runtime.evidence import load_runtime_evidence
from kifrs.workflows.kifrs1116.review_pack import (
    generate_review_pack,
    render_review_pack_markdown,
)


def _fixture(label: str):
    return next(f for f in FIXTURES if f.txn.label == label)


def test_lessee_review_pack_contains_core_sections():
    pack = generate_review_pack(_fixture("scenario_01_simple_office_lease").txn)

    assert pack.standard == "KIFRS1116"
    assert pack.status == "automated"
    assert pack.journal_entry is not None
    assert pack.review_memo and "검토 메모" in pack.review_memo
    assert pack.disclosure_draft and "리스 주석" in pack.disclosure_draft
    assert any(item.label == "리스 주석 초안 검토" for item in pack.review_checklist)
    assert any(action.issue == "조건부 리스 주석 항목" for action in pack.needs_human_review)
    assert "[1116-53]" in pack.citations

    rendered = render_review_pack_markdown(pack)
    assert "# F-ACC Review Pack" in rendered
    assert "## 1. 검토메모" in rendered
    assert "## 2. 분개 초안" in rendered
    assert "## 3. 주석 초안" in rendered
    assert "## 4. 리뷰 체크리스트" in rendered
    assert "변동리스료" in rendered


def test_needs_human_review_pack_keeps_blocker_visible():
    pack = generate_review_pack(_fixture("scenario_09_lessee_modification_expand_shrink").txn)

    assert pack.status == "needs_human_review"
    assert pack.review_memo is None
    assert pack.disclosure_draft is None
    assert pack.needs_human_review
    assert pack.review_checklist[0].status == "needs_human_review"

    action = pack.needs_human_review[0]
    assert "확장+축소" in action.issue
    assert any("수정 할인율" in item for item in action.required_inputs)
    assert any("별도 리스" in item for item in action.review_questions)
    assert any("[1116-46(a)]" in item for item in action.candidate_guidance)

    rendered = render_review_pack_markdown(pack)
    assert "리스범위 확장+축소 동시 변경" in rendered
    assert "필요한 추가자료" in rendered
    assert "리뷰 질문" in rendered
    assert "[1116-46(a)]" in rendered


def test_all_fixtures_generate_review_pack_statuses():
    packs = [generate_review_pack(f.txn) for f in FIXTURES]

    automated = [p for p in packs if p.status == "automated"]
    needs_review = [p for p in packs if p.status == "needs_human_review"]

    assert len(packs) == 10
    assert len(automated) == 9
    assert len(needs_review) == 1
    assert needs_review[0].case_id == "scenario_09_lessee_modification_expand_shrink"
    assert all(p.judgment_summary for p in packs)


def test_1116_review_pack_renders_external_evidence_panel_without_body_text():
    pack = generate_review_pack(_fixture("scenario_01_simple_office_lease").txn, load_runtime_evidence())

    rendered = render_review_pack_markdown(pack)

    assert "## 외부 근거" in rendered
    assert "### 해석 보조 근거" in rendered
    assert "### 법적 경계 근거" in rendered
    assert "### 수치 사실 근거" in rendered
    assert "ev-kasb-interpretation-catalog-seed" in {item["evidence_id"] for item in pack.external_evidence}
    assert "copied source" not in rendered
