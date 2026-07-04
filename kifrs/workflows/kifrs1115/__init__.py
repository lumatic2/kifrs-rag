"""K-IFRS 1115 revenue-recognition decision engine.

R15 starts with a narrow public fixture inventory: four contract-pattern
branches from the private 1115 workflow are represented as structured facts,
expected decision paths, and citation ids only. Later R15 milestones extend this
surface into measurement, journal entries, review memo, and review pack.
"""

from .classify import NeedsHumanReview, RevenueDecision, evaluate_revenue
from .fixtures import FIXTURES, ScenarioFixture
from .schema import Revenue1115

__all__ = [
    "FIXTURES",
    "NeedsHumanReview",
    "Revenue1115",
    "RevenueDecision",
    "ScenarioFixture",
    "evaluate_revenue",
]
