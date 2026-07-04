"""Journal-entry drafts for 1115 revenue decisions."""

from dataclasses import dataclass, field

from .classify import RevenueDecision, evaluate_revenue
from .measurement import RevenueMeasurement, measure_revenue
from .schema import Revenue1115


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


def draft_journal_entries(
    txn: Revenue1115,
    decision: RevenueDecision | None = None,
    measurement: RevenueMeasurement | None = None,
) -> list[JournalEntry]:
    decision = decision or evaluate_revenue(txn)
    measurement = measurement or measure_revenue(txn, decision)

    if decision.path in {"material_right_renewal_option", "material_right_discount_option"}:
        return [_material_right_entry(txn, measurement)]
    if decision.path == "significant_financing_component":
        return [_significant_financing_entry(txn, measurement)]
    if decision.path in {"repurchase_financing_arrangement", "repurchase_lease_arrangement"}:
        return _repurchase_entries(txn, measurement)

    raise ValueError(f"{txn.label}: unsupported 1115 path={decision.path!r}")


def _material_right_entry(
    txn: Revenue1115, measurement: RevenueMeasurement
) -> JournalEntry:
    return JournalEntry(
        label=f"{txn.label} 수익인식 초안",
        lines=[
            EntryLine(account="현금", debit=txn.contract_price),
            EntryLine(account="수익", credit=measurement.recognized_revenue),
            EntryLine(account="계약부채(중요한 권리)", credit=measurement.deferred_revenue),
        ],
    )


def _significant_financing_entry(
    txn: Revenue1115, measurement: RevenueMeasurement
) -> JournalEntry:
    promised = txn.promised_consideration or txn.contract_price
    return JournalEntry(
        label=f"{txn.label} 수익인식 초안(유의적 금융요소)",
        lines=[
            EntryLine(account="매출채권", debit=promised),
            EntryLine(account="수익", credit=measurement.recognized_revenue),
            EntryLine(account="이연금융수익", credit=measurement.financing_effect),
        ],
    )


def _repurchase_entries(
    txn: Revenue1115, measurement: RevenueMeasurement
) -> list[JournalEntry]:
    entries = [
        JournalEntry(
            label=f"{txn.label} 재매입약정 초안",
            lines=[
                EntryLine(account="현금", debit=txn.contract_price),
                EntryLine(account="금융부채", credit=measurement.repurchase_liability),
            ],
        )
    ]
    if measurement.financing_effect:
        entries.append(
            JournalEntry(
                label=f"{txn.label} 재매입스프레드 초안",
                lines=[
                    EntryLine(account="금융비용", debit=measurement.financing_effect),
                    EntryLine(account="금융부채", credit=measurement.financing_effect),
                ],
            )
        )
    return entries
