"""K-IFRS 1115 revenue-recognition decision engine.

R15 starts with a narrow public fixture inventory: four contract-pattern
branches from the private 1115 workflow are represented as structured facts,
expected decision paths, and citation ids only. Later R15 milestones extend this
surface into measurement, journal entries, review memo, and review pack.
"""

from .classify import (
    FiveStepConclusion,
    NeedsHumanReview,
    RevenueDecision,
    evaluate_revenue,
)
from .fixtures import FIXTURES, ScenarioFixture
from .journal_entry import EntryLine, JournalEntry, draft_journal_entries
from .measurement import AllocationLine, RevenueMeasurement, measure_revenue
from .schema import Revenue1115

__all__ = [
    "FIXTURES",
    "AllocationLine",
    "EntryLine",
    "FiveStepConclusion",
    "JournalEntry",
    "NeedsHumanReview",
    "Revenue1115",
    "RevenueDecision",
    "RevenueMeasurement",
    "ScenarioFixture",
    "draft_journal_entries",
    "evaluate_revenue",
    "measure_revenue",
]
