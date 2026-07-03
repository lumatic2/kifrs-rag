"""전체 파이프라인 실행 — 회귀 하네스(WA1 Step 8)와 완료율 리포트 스크립트가 공유."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .amortization import amortize_ac_or_fvoci_debt, revalue_fvpl_or_fvoci_equity
from .classify import ClassificationResult, NeedsHumanReview, classify
from .fixtures import ScenarioFixture
from .initial_entry import JournalEntry, initial_recognition_entry
from .review_memo import generate_review_memo
from .subsequent_entry import (
    subsequent_entries_ac_or_fvoci_debt,
    subsequent_entries_fvpl_or_fvoci_equity,
)


@dataclass
class ScenarioOutcome:
    label: str
    status: str  # "automated" | "needs_human_review"
    classification: str | None = None
    initial_total: float | None = None
    initial_entry: JournalEntry | None = None
    classification_result: ClassificationResult | None = None
    subsequent_entry_count: int = 0
    review_memo: str | None = None
    reason: str | None = None


def run_scenario(fixture: ScenarioFixture) -> ScenarioOutcome:
    txn = fixture.txn
    try:
        result = classify(txn)
    except NeedsHumanReview as exc:
        return ScenarioOutcome(label=txn.label, status="needs_human_review", reason=str(exc))

    entry = initial_recognition_entry(txn, result.classification)

    subsequent_rows: list[Any] = []
    subsequent_entries: list[JournalEntry] = []
    if txn.periods:
        if result.classification in ("AC", "FVOCI_DEBT"):
            subsequent_rows = amortize_ac_or_fvoci_debt(txn, result.classification)
            subsequent_entries = subsequent_entries_ac_or_fvoci_debt(
                txn.label, result.classification, subsequent_rows,
            )
        else:
            subsequent_rows = revalue_fvpl_or_fvoci_equity(txn, result.classification)
            subsequent_entries = subsequent_entries_fvpl_or_fvoci_equity(
                txn.label, result.classification, subsequent_rows,
            )

    memo = generate_review_memo(txn, result, entry, subsequent_rows or None)

    return ScenarioOutcome(
        label=txn.label, status="automated",
        classification=result.classification, initial_total=entry.total_debit,
        initial_entry=entry, classification_result=result,
        subsequent_entry_count=len(subsequent_entries), review_memo=memo,
    )
