"""최초인식 분개 생성 (WORKFLOW.md §3A/§3B).

이용자 인식: (차) 사용권자산 / (대) 리스부채 + 복구충당부채 + 현금(선급·개설직접원가 − 인센티브).
이용자 면제: (차) 리스료비용 / (대) 현금 (케이스별 정액). 제공자 금융: (차) 리스채권 / (대) 현금·자산.
제공자 운용: (차) 운용리스자산 / (대) 현금.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .classify import ExemptionExpense
from .measurement import LesseeMeasurement, LessorMeasurement


@dataclass
class EntryLine:
    account: str
    debit: float = 0.0
    credit: float = 0.0


@dataclass
class JournalEntry:
    label: str
    lines: list[EntryLine] = field(default_factory=list)

    @property
    def total_debit(self) -> float:
        return sum(line.debit for line in self.lines)

    @property
    def total_credit(self) -> float:
        return sum(line.credit for line in self.lines)


def lessee_recognition_entry(label: str, m: LesseeMeasurement) -> JournalEntry:
    lines = [
        EntryLine(account="사용권자산", debit=m.rou_asset),
        EntryLine(account="리스부채", credit=m.lease_liability),
    ]
    if m.restoration_provision:
        lines.append(EntryLine(account="복구충당부채", credit=m.restoration_provision))
    cash = m.rou_asset - m.lease_liability - m.restoration_provision
    if cash:
        lines.append(EntryLine(account="현금(선급·개설직접원가 − 인센티브)", credit=cash))
    return JournalEntry(label=f"{label} 최초인식", lines=lines)


def lessee_exemption_entries(label: str, expenses: list[ExemptionExpense]) -> list[JournalEntry]:
    return [
        JournalEntry(
            label=f"{label} {e.label} 리스료비용",
            lines=[
                EntryLine(account="리스료비용", debit=e.annual_expense),
                EntryLine(account="현금", credit=e.annual_expense),
            ],
        )
        for e in expenses
    ]


def lessor_initial_entry(label: str, m: LessorMeasurement) -> JournalEntry:
    if m.kind == "finance":
        return JournalEntry(
            label=f"{label} 최초인식(금융리스)",
            lines=[
                EntryLine(account="리스채권", debit=m.net_investment),
                EntryLine(account="현금·기초자산", credit=m.net_investment),
            ],
        )
    return JournalEntry(
        label=f"{label} 최초인식(운용리스)",
        lines=[
            EntryLine(account="운용리스자산", debit=m.operating_asset),
            EntryLine(account="현금", credit=m.operating_asset),
        ],
    )
