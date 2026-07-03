"""최초인식 분개 생성 (WORKFLOW.md §4).

AC/FVOCI(부채)/FVOCI(자본): 거래원가를 최초인식가에 포함 [1109-5.1.1].
FVPL: 거래원가는 즉시 비용 처리 — 취득원가에 포함하지 않는다.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .classify import Classification
from .schema import Transaction1109

_ACCOUNT_BY_CLASSIFICATION = {
    "AC": "AC금융자산",
    "FVOCI_DEBT": "FVOCI금융자산",
    "FVOCI_EQUITY": "FVOCI금융자산(자본)",
    "FVPL": "FVPL금융자산",
}


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


def initial_recognition_entry(txn: Transaction1109, classification: Classification) -> JournalEntry:
    account = _ACCOUNT_BY_CLASSIFICATION[classification]
    fv = txn.purchase_price
    cost = txn.transaction_cost

    if classification == "FVPL":
        lines = [EntryLine(account=account, debit=fv)]
        if cost:
            lines.append(EntryLine(account="수수료비용", debit=cost))
        lines.append(EntryLine(account="현금", credit=fv + cost))
        return JournalEntry(label=f"{txn.label} 최초인식", lines=lines)

    amount = fv + cost
    return JournalEntry(
        label=f"{txn.label} 최초인식",
        lines=[
            EntryLine(account=account, debit=amount),
            EntryLine(account="현금", credit=amount),
        ],
    )
