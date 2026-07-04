"""후속측정 분개 생성 (WORKFLOW.md §4A/§4B) — 상각표·감가를 분개로 변환.

이용자: 매기 이자비용 + 리스료 지급 + 감가상각. 제공자 금융: 매기 이자수익 + 리스료 수령.
변경 이벤트가 있으면 변경 유효일까지(periods_elapsed)만 생성한다 — 변경 후는 modification.py가
headline으로 검증.
"""
from __future__ import annotations

from .amortization import AmortizationRow
from .initial_entry import EntryLine, JournalEntry
from .money import won


def lessee_subsequent_entries(
    label: str, rows: list[AmortizationRow], annual_depreciation: int
) -> list[JournalEntry]:
    entries: list[JournalEntry] = []
    for row in rows:
        entries.append(JournalEntry(
            label=f"{label} {row.label} 결산",
            lines=[
                EntryLine(account="이자비용", debit=row.interest),
                EntryLine(account="리스부채", credit=row.interest),
                EntryLine(account="리스부채", debit=row.payment),
                EntryLine(account="현금", credit=row.payment),
                EntryLine(account="감가상각비", debit=annual_depreciation),
                EntryLine(account="감가상각누계액", credit=annual_depreciation),
            ],
        ))
    return entries


def lessor_finance_subsequent_entries(
    label: str, rows: list[AmortizationRow]
) -> list[JournalEntry]:
    entries: list[JournalEntry] = []
    for row in rows:
        principal = won(row.payment) - row.interest
        entries.append(JournalEntry(
            label=f"{label} {row.label} 금융수익",
            lines=[
                EntryLine(account="현금", debit=row.payment),
                EntryLine(account="이자수익", credit=row.interest),
                EntryLine(account="리스채권", credit=principal),
            ],
        ))
    return entries
