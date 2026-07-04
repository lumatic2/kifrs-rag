"""1109 disclosure skeleton renderer built from review-pack outputs."""

from kifrs.workflows.disclosure.adapters import from_1109_review_pack
from kifrs.workflows.disclosure.schema import DisclosureChecklistItem

from .fixtures import ScenarioFixture
from .review_pack import ReviewPack, generate_review_pack


def generate_disclosure_skeleton(source: ScenarioFixture | ReviewPack) -> str:
    pack = source if isinstance(source, ReviewPack) else generate_review_pack(source)
    items = from_1109_review_pack(pack)

    md: list[str] = [
        f"# 금융상품 주석 skeleton — {pack.case_id}",
        "",
        "> 1109 review pack 기반 초안. 금융위험, 공정가치, 회계정책 문구는 회사 자료로 보완.",
        "",
        "## 1. 자동 산출 후보",
    ]
    auto_items = [item for item in items if item.fill_status == "auto"]
    if auto_items:
        md.extend(_item_line(item) for item in auto_items)
    else:
        md.append("- 자동 산출 후보 없음")

    md.extend(["", "## 2. 사람 보완 필요"])
    human_items = [item for item in items if item.fill_status == "needs_human_review"]
    if human_items:
        for item in human_items:
            md.append(f"### {item.label}")
            if item.required_inputs:
                md.append("- 필요한 추가자료:")
                md.extend(f"  - {value}" for value in item.required_inputs)
            if item.review_questions:
                md.append("- 리뷰 질문:")
                md.extend(f"  - {value}" for value in item.review_questions)
    else:
        md.append("- 사람 보완 필요 항목 없음")

    md.extend(["", "## 3. 근거"])
    citations = sorted({citation for item in items for citation in _split_citations(item.citation)})
    if citations:
        md.extend(f"- {citation}" for citation in citations)
    else:
        md.append("- citation id 없음")

    return "\n".join(md)


def _item_line(item: DisclosureChecklistItem) -> str:
    value = item.draft_value or "값 미정"
    citation = f" ({item.citation})" if item.citation else ""
    return f"- {item.label}: {value}{citation}"


def _split_citations(citation_text: str) -> list[str]:
    return [part.strip() for part in citation_text.split(",") if part.strip()]
