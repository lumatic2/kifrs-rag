"""Schema for audit analytical procedure fixtures and metric outputs."""

from dataclasses import dataclass
from typing import Literal

StatementKind = Literal["balance_sheet", "income_statement"]


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
