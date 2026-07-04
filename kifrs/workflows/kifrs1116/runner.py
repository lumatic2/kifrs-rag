"""전체 파이프라인 실행 (AE1) — 회귀 하네스와 완료율 리포트가 공유.

식별(§1) → 분류/면제(§2) → 최초측정(§3) → 후속측정 분개(§4) → 재평가·변경 headline(§5) →
런타임 grounding(RGA1) → 검토메모(§6). 반환 직전 모든 reasons의 인용을 DB로 존재 검증하고,
실패하면 NeedsHumanReview로 escalate.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .amortization import amortize
from .classify import NeedsHumanReview, classify_path, exemption_expenses
from .grounding import GroundingFailure, ground_reasons
from .identification import identify_lease
from .initial_entry import (
    JournalEntry,
    lessee_exemption_entries,
    lessee_recognition_entry,
    lessor_initial_entry,
)
from .measurement import measure_lessee, measure_lessor
from .modification import apply_event
from .review_memo import generate_review_memo
from .schema import Lease1116
from .subsequent_entry import lessee_subsequent_entries, lessor_finance_subsequent_entries


@dataclass
class LeaseOutcome:
    label: str
    status: str  # "automated" | "needs_human_review"
    path: str | None = None
    headlines: dict[str, Any] = field(default_factory=dict)
    initial_entry: JournalEntry | None = None
    subsequent_entry_count: int = 0
    review_memo: str | None = None
    reason: str | None = None


def run_lease(lease: Lease1116) -> LeaseOutcome:
    if lease.special_case:
        return LeaseOutcome(
            label=lease.label, status="needs_human_review",
            reason=NeedsHumanReview(lease.special_case, lease.label).args[0],
        )

    identification = identify_lease(lease)
    if not identification.is_lease:
        return LeaseOutcome(
            label=lease.label, status="needs_human_review",
            reason=f"{lease.label}: 리스 아님 판정 — 서비스 계약 회계는 범위 밖",
        )

    path = classify_path(lease)
    headlines: dict[str, Any] = {}
    reasons: list[str] = list(identification.reasons) + list(path.reasons)
    initial_entry: JournalEntry | None = None
    subsequent_count = 0

    if path.path == "lessee_exemption":
        expenses = exemption_expenses(lease.exemption_cases)
        for e in expenses:
            headlines[f"{e.label}_annual_expense"] = e.annual_expense
            headlines[f"{e.label}_total_expense"] = e.total_expense
        entries = lessee_exemption_entries(lease.label, expenses)
        initial_entry = entries[0] if entries else None
        subsequent_count = len(entries)

    elif path.path == "lessee_recognition":
        m = measure_lessee(lease)
        reasons += m.reasons
        headlines.update(
            lease_liability=m.lease_liability, rou_asset=m.rou_asset,
            annual_depreciation=m.annual_depreciation,
        )
        if m.restoration_provision:
            headlines["restoration_provision"] = m.restoration_provision
        initial_entry = lessee_recognition_entry(lease.label, m)
        periods = lease.events[0].periods_elapsed if lease.events else (lease.lease_term_years or 0)
        rows = amortize(m.lease_liability, lease.discount_rate, lease.annual_payment, periods)
        subsequent_count = len(lessee_subsequent_entries(lease.label, rows, m.annual_depreciation))
        for event in lease.events:
            eh, er = apply_event(lease, event)
            headlines.update(eh)
            reasons += er

    elif path.path == "lessor_finance":
        m = measure_lessor(lease)
        reasons += m.reasons
        headlines["net_investment"] = m.net_investment
        initial_entry = lessor_initial_entry(lease.label, m)
        periods = lease.events[0].periods_elapsed if lease.events else (lease.lease_term_years or 0)
        rows = amortize(m.net_investment, lease.discount_rate, lease.annual_payment, periods)
        subsequent_count = len(lessor_finance_subsequent_entries(lease.label, rows))
        for event in lease.events:
            eh, er = apply_event(lease, event)
            headlines.update(eh)
            reasons += er

    else:  # lessor_operating
        m = measure_lessor(lease)
        reasons += m.reasons
        headlines["operating_asset_initial"] = m.operating_asset
        initial_entry = lessor_initial_entry(lease.label, m)
        for event in lease.events:
            eh, er = apply_event(lease, event)
            headlines.update(eh)
            reasons += er

    try:
        ground_reasons(reasons)
    except GroundingFailure as exc:
        return LeaseOutcome(
            label=lease.label, status="needs_human_review",
            reason=f"citation_grounding_failed: {exc}",
        )

    memo = generate_review_memo(
        lease, identification, path, headlines, initial_entry, reasons
    )
    return LeaseOutcome(
        label=lease.label, status="automated", path=path.path, headlines=headlines,
        initial_entry=initial_entry, subsequent_entry_count=subsequent_count, review_memo=memo,
    )
