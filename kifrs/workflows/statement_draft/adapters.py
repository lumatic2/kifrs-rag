"""Adapters from F-ACC review packs into statement draft line candidates."""

from typing import Any

from kifrs.workflows.kifrs1109.review_pack import ReviewPack as ReviewPack1109
from kifrs.workflows.kifrs1115.review_pack import ReviewPack as ReviewPack1115
from kifrs.workflows.kifrs1116.review_pack import ReviewPack as ReviewPack1116

from .schema import DebitCredit, PresentationStatus, StatementKind, StatementLineCandidate

_ACCOUNT_MAP: dict[str, tuple[StatementKind, str]] = {
    "AC금융자산": ("balance_sheet", "금융자산(상각후원가)"),
    "FVOCI금융자산": ("balance_sheet", "금융자산(FVOCI)"),
    "FVOCI금융자산(자본)": ("balance_sheet", "금융자산(FVOCI-지분)"),
    "FVPL금융자산": ("balance_sheet", "금융자산(FVPL)"),
    "현금": ("balance_sheet", "현금및현금성자산"),
    "현금(선급·개설직접원가 − 인센티브)": ("balance_sheet", "현금및현금성자산"),
    "수수료비용": ("income_statement", "금융상품 거래비용"),
    "이자수익": ("income_statement", "이자수익"),
    "배당수익(PL)": ("income_statement", "배당수익"),
    "평가이익(PL)": ("income_statement", "평가이익"),
    "평가손실(PL)": ("income_statement", "평가손실"),
    "평가이익(OCI)": ("oci", "기타포괄손익-금융자산평가이익"),
    "평가손실(OCI)": ("oci", "기타포괄손익-금융자산평가손실"),
    "수익": ("income_statement", "수익"),
    "계약부채(중요한 권리)": ("balance_sheet", "계약부채"),
    "매출채권": ("balance_sheet", "매출채권"),
    "이연금융수익": ("balance_sheet", "이연금융수익"),
    "금융부채": ("balance_sheet", "금융부채"),
    "금융비용": ("income_statement", "금융비용"),
    "사용권자산": ("balance_sheet", "사용권자산"),
    "리스부채": ("balance_sheet", "리스부채"),
    "복구충당부채": ("balance_sheet", "충당부채"),
    "리스채권": ("balance_sheet", "리스채권"),
    "운용리스자산": ("balance_sheet", "운용리스자산"),
    "리스료비용": ("income_statement", "리스료비용"),
}


def from_1109_review_pack(pack: ReviewPack1109) -> list[StatementLineCandidate]:
    questions = _review_questions(pack)
    fact_evidence_refs = _fact_evidence_refs(pack)
    items: list[StatementLineCandidate] = []
    if pack.journal_entry is not None:
        items.extend(
            _from_entry_lines(
                pack.journal_entry.lines,
                standard=pack.standard,
                case_id=pack.case_id,
                source_field="journal_entry.lines",
                status=_status(pack.status),
                review_questions=questions,
                note_links=pack.citations,
                evidence_refs=fact_evidence_refs,
            )
        )
    for entry_index, entry in enumerate(pack.subsequent_entries):
        items.extend(
            _from_entry_lines(
                entry.lines,
                standard=pack.standard,
                case_id=pack.case_id,
                source_field=f"subsequent_entries[{entry_index}].lines",
                status=_status(pack.status),
                review_questions=questions,
                note_links=pack.citations,
                evidence_refs=fact_evidence_refs,
            )
        )
    items.append(
        StatementLineCandidate(
            statement="note",
            line_item=f"금융상품 분류: {pack.classification or '사람 검토 필요'}",
            source_standard=pack.standard,
            source_case_id=pack.case_id,
            source_field="classification",
            presentation_status=_status(pack.status),
            review_questions=questions,
            note_links=pack.citations,
        )
    )
    return items


def from_1115_review_pack(pack: ReviewPack1115) -> list[StatementLineCandidate]:
    questions = _review_questions(pack)
    fact_evidence_refs = _fact_evidence_refs(pack)
    items: list[StatementLineCandidate] = []
    for entry_index, entry in enumerate(pack.journal_entries):
        items.extend(
            _from_entry_lines(
                entry.lines,
                standard=pack.standard,
                case_id=pack.case_id,
                source_field=f"journal_entries[{entry_index}].lines",
                status=_status(pack.status),
                review_questions=questions,
                note_links=pack.citations,
                evidence_refs=fact_evidence_refs,
            )
        )
    if pack.measurement is not None:
        items.append(
            StatementLineCandidate(
                statement="note",
                line_item=(
                    f"수익인식 측정: {pack.measurement.path}; "
                    f"revenue={pack.measurement.recognized_revenue:,.0f}; "
                    f"deferred={pack.measurement.deferred_revenue:,.0f}; "
                    f"financing={pack.measurement.financing_effect:,.0f}; "
                    f"repurchase_liability={pack.measurement.repurchase_liability:,.0f}"
                ),
                source_standard=pack.standard,
                source_case_id=pack.case_id,
                source_field="measurement",
                presentation_status=_status(pack.status),
                review_questions=questions,
                note_links=pack.citations,
            )
        )
    if pack.status == "needs_human_review":
        items.extend(_human_review_note_candidates(pack.standard, pack.case_id, questions))
    return items


def from_1116_review_pack(pack: ReviewPack1116) -> list[StatementLineCandidate]:
    questions = _review_questions(pack)
    fact_evidence_refs = _fact_evidence_refs(pack)
    items: list[StatementLineCandidate] = []
    if pack.journal_entry is not None:
        items.extend(
            _from_entry_lines(
                pack.journal_entry.lines,
                standard=pack.standard,
                case_id=pack.case_id,
                source_field="journal_entry.lines",
                status=_status(pack.status),
                review_questions=questions,
                note_links=pack.citations,
                evidence_refs=fact_evidence_refs,
            )
        )
    if pack.disclosure_draft:
        items.append(
            StatementLineCandidate(
                statement="note",
                line_item="리스 주석 초안",
                source_standard=pack.standard,
                source_case_id=pack.case_id,
                source_field="disclosure_draft",
                presentation_status=_status(pack.status),
                review_questions=questions,
                note_links=pack.citations,
            )
        )
    if pack.status == "needs_human_review":
        items.extend(_human_review_note_candidates(pack.standard, pack.case_id, questions))
    return items


def _from_entry_lines(
    lines: list[Any],
    *,
    standard: str,
    case_id: str,
    source_field: str,
    status: PresentationStatus,
    review_questions: list[str],
    note_links: list[str],
    evidence_refs: list[dict[str, object]] | None = None,
) -> list[StatementLineCandidate]:
    candidates: list[StatementLineCandidate] = []
    for index, line in enumerate(lines):
        statement, line_item = _ACCOUNT_MAP.get(line.account, ("note", line.account))
        amount, debit_credit = _amount_and_side(line)
        line_evidence_refs = list(evidence_refs or []) if amount is not None and statement != "note" else []
        candidates.append(
            StatementLineCandidate(
                statement=statement,
                line_item=line_item,
                amount=amount,
                debit_credit=debit_credit,
                source_standard=standard,
                source_case_id=case_id,
                source_field=f"{source_field}[{index}]",
                presentation_status=status,
                review_questions=review_questions,
                note_links=note_links,
                evidence_refs=line_evidence_refs,
            )
        )
    return candidates


def _amount_and_side(line: Any) -> tuple[float | None, DebitCredit]:
    if line.debit:
        return line.debit, "debit"
    if line.credit:
        return line.credit, "credit"
    return None, "none"


def _status(status: str) -> PresentationStatus:
    return "needs_human_review" if status == "needs_human_review" else "draft"


def _review_questions(pack: Any) -> list[str]:
    questions: list[str] = []
    for action in pack.needs_human_review:
        questions.extend(action.review_questions)
    return questions


def _fact_evidence_refs(pack: Any) -> list[dict[str, object]]:
    old_refs = [
        dict(item)
        for item in getattr(pack, "external_evidence", [])
        if item.get("citation_role") == "fact_evidence"
    ]
    authority_refs = [
        dict(item)
        for item in getattr(pack, "authority_boundary", {}).get("fact_evidence", [])
        if item.get("authority_role") == "fact_evidence"
    ]
    return old_refs + authority_refs


def _human_review_note_candidates(
    standard: str, case_id: str, questions: list[str]
) -> list[StatementLineCandidate]:
    return [
        StatementLineCandidate(
            statement="note",
            line_item="사람 검토 필요 항목",
            source_standard=standard,
            source_case_id=case_id,
            source_field="needs_human_review",
            presentation_status="needs_human_review",
            review_questions=questions,
        )
    ]
