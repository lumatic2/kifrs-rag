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
from .review_memo import SECTION_TITLES, generate_review_memo
from .review_pack import (
    HumanReviewAction,
    ReviewChecklistItem,
    ReviewPack,
    generate_review_pack,
    render_review_pack_markdown,
)
from .schema import Revenue1115

__all__ = [
    "FIXTURES",
    "AllocationLine",
    "EntryLine",
    "FiveStepConclusion",
    "JournalEntry",
    "HumanReviewAction",
    "NeedsHumanReview",
    "Revenue1115",
    "RevenueDecision",
    "RevenueMeasurement",
    "ReviewChecklistItem",
    "ReviewPack",
    "SECTION_TITLES",
    "ScenarioFixture",
    "draft_journal_entries",
    "evaluate_revenue",
    "generate_review_pack",
    "generate_review_memo",
    "measure_revenue",
    "render_review_pack_markdown",
]
