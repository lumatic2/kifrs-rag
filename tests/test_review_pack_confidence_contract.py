from __future__ import annotations

from scripts.review_pack_confidence_contract import (
    ALLOWED_LABELS,
    build_contract,
    confidence_sections_for_pack,
    render_markdown,
)
from kifrs.runtime.authority_boundary import build_runtime_authority_boundary
from kifrs.workflows.kifrs1116.fixtures import FIXTURES
from kifrs.workflows.kifrs1116.review_pack import generate_review_pack


def _pack(label: str):
    fixture = next(item for item in FIXTURES if item.txn.label == label)
    return generate_review_pack(
        fixture.txn,
        authority_boundary=build_runtime_authority_boundary(primary_citations=["[1116-53]", "[1116-59]"]),
    )


def test_confidence_contract_labels_automated_pack_without_overclaiming() -> None:
    sections = confidence_sections_for_pack(_pack("scenario_01_simple_office_lease"))
    by_section = {section.section: section for section in sections}

    assert by_section["review_memo"].label == "ready"
    assert by_section["journal_entry"].label == "ready"
    assert by_section["disclosure_draft"].label == "caution"
    assert by_section["authority_boundary"].label == "ready"
    assert by_section["human_review_items"].label == "human_review_required"
    assert {section.label for section in sections}.issubset(ALLOWED_LABELS)
    assert all("Decision-support only" in section.human_boundary for section in sections)


def test_confidence_contract_marks_stopped_workflow_as_human_review_required() -> None:
    sections = confidence_sections_for_pack(_pack("scenario_09_lessee_modification_expand_shrink"))
    by_section = {section.section: section for section in sections}

    assert by_section["review_memo"].label == "human_review_required"
    assert by_section["journal_entry"].label == "human_review_required"
    assert by_section["disclosure_draft"].label == "human_review_required"
    assert by_section["human_review_items"].label == "human_review_required"


def test_review_pack_confidence_contract_report_is_public_safe() -> None:
    contract = build_contract()
    rendered = render_markdown(contract)

    assert contract["ok"] is True
    assert contract["milestone"] == "PTQ2"
    assert "ready/caution/human-review-required" in rendered
    assert "Final accounting judgment" in rendered
    assert "api_key" not in rendered
    assert "source_body" not in rendered
