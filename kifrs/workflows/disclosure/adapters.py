"""Adapters from domain review outputs into the common disclosure schema."""

from kifrs.workflows.kifrs1109.review_pack import ReviewPack as ReviewPack1109
from kifrs.workflows.kifrs1115.review_pack import ReviewPack as ReviewPack1115
from kifrs.workflows.kifrs1116.disclosure import LESSEE_DISCLOSURE_REQUIREMENTS

from .schema import DisclosureChecklistItem

_1116_FIELD_BY_ITEM = {
    "53(1)": "depreciation",
    "53(2)": "interest",
    "53(3)": "short_term_expense",
    "53(4)": "low_value_expense",
    "53(7)": "cash_outflow",
    "53(8)": "rou_addition",
    "53(10)": "rou_year_end",
    "58": "maturity",
}


def from_1116_requirements() -> list[DisclosureChecklistItem]:
    items: list[DisclosureChecklistItem] = []
    for req in LESSEE_DISCLOSURE_REQUIREMENTS:
        source_field = _1116_FIELD_BY_ITEM.get(req.item, "")
        items.append(
            DisclosureChecklistItem(
                standard="KIFRS1116",
                item_id=req.item,
                label=req.label,
                citation=req.citation,
                source_kind="requirement",
                source_field=source_field,
                fill_status="auto" if req.fillable else "needs_human_review",
                required_inputs=[] if req.fillable else [req.label],
                review_questions=[] if req.fillable else [f"{req.label} 거래가 회사에 존재하는가?"],
            )
        )
    return items


def from_1115_review_pack(pack: ReviewPack1115) -> list[DisclosureChecklistItem]:
    if pack.status == "needs_human_review":
        return [_human_item("KIFRS1115", pack.case_id, action) for action in pack.needs_human_review]

    items = [
        DisclosureChecklistItem(
            standard="KIFRS1115",
            item_id=f"{pack.case_id}:path",
            label="수익인식 판단 경로",
            citation=", ".join(pack.citations),
            source_kind="decision",
            source_field="path",
            fill_status="auto",
            draft_value=pack.path,
        )
    ]
    if pack.measurement is not None:
        items.append(
            DisclosureChecklistItem(
                standard="KIFRS1115",
                item_id=f"{pack.case_id}:measurement",
                label="수익 및 이연/금융요소 측정",
                citation=", ".join(pack.citations),
                source_kind="measurement",
                source_field="measurement",
                fill_status="auto",
                draft_value=(
                    f"revenue={pack.measurement.recognized_revenue:,.0f}; "
                    f"deferred={pack.measurement.deferred_revenue:,.0f}; "
                    f"financing={pack.measurement.financing_effect:,.0f}"
                ),
            )
        )
    items.extend(_human_item("KIFRS1115", pack.case_id, action) for action in pack.needs_human_review)
    return items


def from_1109_review_pack(pack: ReviewPack1109) -> list[DisclosureChecklistItem]:
    if pack.status == "needs_human_review":
        return [_human_item("KIFRS1109", pack.case_id, action) for action in pack.needs_human_review]

    items = [
        DisclosureChecklistItem(
            standard="KIFRS1109",
            item_id=f"{pack.case_id}:classification",
            label="금융상품 분류",
            citation=", ".join(pack.citations),
            source_kind="decision",
            source_field="classification",
            fill_status="auto",
            draft_value=pack.classification,
        )
    ]
    items.extend(_human_item("KIFRS1109", pack.case_id, action) for action in pack.needs_human_review)
    return items


def _human_item(standard: str, case_id: str, action) -> DisclosureChecklistItem:
    return DisclosureChecklistItem(
        standard=standard,
        item_id=f"{case_id}:human:{action.issue}",
        label=action.issue,
        citation="",
        source_kind="human_input",
        source_field="needs_human_review",
        fill_status="needs_human_review",
        required_inputs=list(action.required_inputs),
        review_questions=list(action.review_questions),
    )
