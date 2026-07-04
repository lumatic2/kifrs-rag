"""Common financial-statement line candidate schema."""

from dataclasses import dataclass, field
from typing import Literal

StatementKind = Literal["balance_sheet", "income_statement", "oci", "note"]
DebitCredit = Literal["debit", "credit", "none"]
PresentationStatus = Literal["draft", "needs_human_review", "not_applicable"]


@dataclass(frozen=True)
class StatementLineCandidate:
    statement: StatementKind
    line_item: str
    source_standard: str
    source_case_id: str
    source_field: str
    presentation_status: PresentationStatus
    amount: float | None = None
    debit_credit: DebitCredit = "none"
    review_questions: list[str] = field(default_factory=list)
    note_links: list[str] = field(default_factory=list)
    evidence_refs: list[dict[str, object]] = field(default_factory=list)
