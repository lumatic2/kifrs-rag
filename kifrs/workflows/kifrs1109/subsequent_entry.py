"""후속측정 분개 생성 (WORKFLOW.md §5) — amortization.py의 산출행을 분개로 변환."""
from __future__ import annotations

from .amortization import AmortizationRow, RevaluationRow
from .classify import Classification
from .initial_entry import EntryLine, JournalEntry

_AC_ACCOUNT = {"AC": "AC금융자산", "FVOCI_DEBT": "FVOCI금융자산"}
_FV_ACCOUNT = {"FVPL": "FVPL금융자산", "FVOCI_EQUITY": "FVOCI금융자산(자본)"}


def subsequent_entries_ac_or_fvoci_debt(
    label: str, classification: Classification, rows: list[AmortizationRow]
) -> list[JournalEntry]:
    """이자수익(유효이자율법) + (FVOCI_DEBT만) OCI 조정 분개."""
    account = _AC_ACCOUNT[classification]
    entries: list[JournalEntry] = []
    for row in rows:
        lines = [EntryLine(account="현금", debit=row.coupon_cash)]
        if row.amortization >= 0:
            lines.append(EntryLine(account=account, debit=row.amortization))
        else:
            lines.append(EntryLine(account=account, credit=-row.amortization))
        lines.append(EntryLine(account="이자수익", credit=row.effective_interest))
        entries.append(JournalEntry(label=f"{label} {row.label} 이자수익", lines=lines))

        if classification == "FVOCI_DEBT" and row.oci_delta is not None:
            oci_lines = (
                [EntryLine(account=account, debit=row.oci_delta),
                 EntryLine(account="평가이익(OCI)", credit=row.oci_delta)]
                if row.oci_delta >= 0 else
                [EntryLine(account="평가손실(OCI)", debit=-row.oci_delta),
                 EntryLine(account=account, credit=-row.oci_delta)]
            )
            entries.append(JournalEntry(label=f"{label} {row.label} 공정가치평가(OCI)", lines=oci_lines))
    return entries


def subsequent_entries_fvpl_or_fvoci_equity(
    label: str, classification: Classification, rows: list[RevaluationRow]
) -> list[JournalEntry]:
    """표시이자(명목) + 기말FV 변동 분개 — FVPL은 PL, FVOCI_EQUITY는 OCI로."""
    account = _FV_ACCOUNT[classification]
    gain_account = "평가이익(PL)" if classification == "FVPL" else "평가이익(OCI)"
    loss_account = "평가손실(PL)" if classification == "FVPL" else "평가손실(OCI)"
    income_account = "이자수익" if classification == "FVPL" else "배당수익(PL)"

    entries: list[JournalEntry] = []
    for row in rows:
        if row.coupon_cash:
            entries.append(JournalEntry(
                label=f"{label} {row.label} {income_account}",
                lines=[EntryLine(account="현금", debit=row.coupon_cash),
                       EntryLine(account=income_account, credit=row.coupon_cash)],
            ))
        if row.fv_delta >= 0:
            fv_lines = [EntryLine(account=account, debit=row.fv_delta),
                        EntryLine(account=gain_account, credit=row.fv_delta)]
        else:
            fv_lines = [EntryLine(account=loss_account, debit=-row.fv_delta),
                        EntryLine(account=account, credit=-row.fv_delta)]
        entries.append(JournalEntry(label=f"{label} {row.label} 공정가치평가", lines=fv_lines))
    return entries
