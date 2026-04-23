"""평가 하네스 데이터 모델."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Citation:
    standard: str
    no: str


@dataclass
class GoldItem:
    id: str
    source: str
    source_ref: str
    question: str
    must_cite: list[Citation]
    may_cite: list[Citation] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    forbidden_keywords: list[str] = field(default_factory=list)
    notes: str = ""

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "GoldItem":
        def _cites(raw: list[dict]) -> list[Citation]:
            out = []
            for c in raw or []:
                std = c["standard"]
                nos = c["no"] if isinstance(c["no"], list) else [c["no"]]
                for n in nos:
                    out.append(Citation(standard=std, no=n))
            return out

        return cls(
            id=d["id"],
            source=d.get("source", "unknown"),
            source_ref=d.get("source_ref", ""),
            question=d["question"],
            must_cite=_cites(d.get("must_cite", [])),
            may_cite=_cites(d.get("may_cite", [])),
            keywords=list(d.get("keywords", [])),
            forbidden_keywords=list(d.get("forbidden_keywords", [])),
            notes=d.get("notes", ""),
        )


@dataclass
class RunResult:
    """단일 runner가 특정 문항에 반환한 raw 답변."""
    item_id: str
    runner: str
    question: str
    answer: str
    retrieved_context: list[dict[str, Any]] = field(default_factory=list)
    latency_seconds: float = 0.0
    model: str = ""
    error: str | None = None


@dataclass
class ScoreResult:
    """단일 scorer가 (item, run) 쌍에 부여한 점수."""
    scorer: str
    score: float  # 0.0 ~ 1.0
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ItemReport:
    item: GoldItem
    run: RunResult
    scores: list[ScoreResult] = field(default_factory=list)

    @property
    def composite(self) -> float:
        if not self.scores:
            return 0.0
        return sum(s.score for s in self.scores) / len(self.scores)


@dataclass
class RunReport:
    runner: str
    timestamp: str
    items: list[ItemReport] = field(default_factory=list)

    @property
    def mean_composite(self) -> float:
        if not self.items:
            return 0.0
        return sum(i.composite for i in self.items) / len(self.items)
