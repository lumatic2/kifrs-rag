"""Schema for audit analytical procedure fixtures and metric outputs."""

from dataclasses import dataclass, field
from typing import Literal

StatementKind = Literal["balance_sheet", "income_statement"]
FindingSeverity = Literal["info", "warning", "critical"]


@dataclass(frozen=True)
class FinancialStatementLine:
    period: str
    statement: StatementKind
    line_item: str
    amount: float


@dataclass(frozen=True)
class AnalyticalProcedureInput:
    entity: str
    periods: list[str]
    lines: list[FinancialStatementLine]


@dataclass(frozen=True)
class AnalyticalMetric:
    metric_id: str
    label: str
    current_value: float
    prior_value: float | None = None
    change_amount: float | None = None
    change_pct: float | None = None


@dataclass(frozen=True)
class AnomalyFinding:
    finding_id: str
    severity: FindingSeverity
    metric_id: str
    message: str
    review_questions: list[str]
    linked_statement_candidates: list[str]


@dataclass(frozen=True)
class LinkedStatementCandidate:
    finding_id: str
    source_standard: str
    source_case_id: str
    source_field: str
    statement: str
    line_item: str
    amount: float | None
    presentation_status: str
    evidence_refs: list[dict[str, object]] = field(default_factory=list)
