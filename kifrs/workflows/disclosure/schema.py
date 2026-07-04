"""Common disclosure checklist schema used across K-IFRS workflows."""

from dataclasses import dataclass, field
from typing import Literal

FillStatus = Literal["auto", "needs_human_review", "not_applicable"]


@dataclass(frozen=True)
class DisclosureChecklistItem:
    standard: str
    item_id: str
    label: str
    citation: str
    source_kind: str
    source_field: str
    fill_status: FillStatus
    draft_value: str | None = None
    required_inputs: list[str] = field(default_factory=list)
    review_questions: list[str] = field(default_factory=list)
