"""F-ACC review pack composition for K-IFRS 1116.

This module does not add new lease judgment logic. It wraps the existing 1116
runner, review memo, journal entry, and lessee disclosure draft into one
Accounting Advisory workpaper-style output.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import re

from .disclosure import aggregate_portfolio, generate_disclosure_note
from .initial_entry import JournalEntry
from .runner import LeaseOutcome, run_lease
from .schema import Lease1116


@dataclass(frozen=True)
class ReviewChecklistItem:
    label: str
    status: str  # "ready" | "needs_human_review" | "not_applicable"
    note: str


@dataclass(frozen=True)
class ReviewPack:
    standard: str
    case_id: str
    status: str  # "automated" | "needs_human_review"
    judgment_summary: str
    journal_entry: JournalEntry | None
    review_memo: str | None
    disclosure_draft: str | None
    review_checklist: list[ReviewChecklistItem] = field(default_factory=list)
    needs_human_review: list[str] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)


def _extract_citations(*texts: str | None) -> list[str]:
    citations: set[str] = set()
    for text in texts:
        if not text:
            continue
        citations.update(re.findall(r"\[\d{4}-[A-Za-z0-9()~.,·\- ]+\]", text))
    return sorted(citations)


def _entry_markdown(entry: JournalEntry | None) -> str:
    if entry is None:
        return "- 최초분개: 없음"
    lines = [f"- {entry.label}"]
    for line in entry.lines:
        if line.debit:
            lines.append(f"  - (차) {line.account}: {line.debit:,.0f}")
        if line.credit:
            lines.append(f"  - (대) {line.account}: {line.credit:,.0f}")
    return "\n".join(lines)


def _summary_from_outcome(outcome: LeaseOutcome) -> str:
    if outcome.status == "needs_human_review":
        return outcome.reason or "사람 검토 필요"
    return (
        f"{outcome.label}: {outcome.path} 경로로 자동 판단. "
        f"headline {len(outcome.headlines)}개, 후속분개 {outcome.subsequent_entry_count}개 산출."
    )


def _checklist(lease: Lease1116, outcome: LeaseOutcome, disclosure_draft: str | None) -> list[ReviewChecklistItem]:
    if outcome.status == "needs_human_review":
        return [
            ReviewChecklistItem(
                label="자동 판단 중단 사유 확인",
                status="needs_human_review",
                note=outcome.reason or "사람 검토 필요",
            )
        ]

    items = [
        ReviewChecklistItem("리스 식별/분류 판단", "ready", f"경로: {outcome.path}"),
        ReviewChecklistItem("최초분개 검토", "ready", "최초분개 금액과 차대 일치 여부 확인"),
        ReviewChecklistItem("검토메모 문구 검토", "ready", "회사 특수 사실관계와 표현 보완"),
    ]
    if lease.party == "lessee":
        items.append(
            ReviewChecklistItem(
                "리스 주석 초안 검토",
                "ready" if disclosure_draft else "needs_human_review",
                "변동리스료·전대리스·판매후리스 등 조건부 항목은 회사 자료로 보완",
            )
        )
    else:
        items.append(
            ReviewChecklistItem(
                "리스제공자 주석",
                "not_applicable",
                "RP1 disclosure draft는 리스이용자 주석 파일럿만 포함",
            )
        )
    return items


def generate_review_pack(lease: Lease1116) -> ReviewPack:
    """Run the 1116 pipeline and compose a F-ACC workpaper pack."""
    outcome = run_lease(lease)

    disclosure_draft: str | None = None
    if outcome.status == "automated" and lease.party == "lessee":
        disclosure_draft = generate_disclosure_note(aggregate_portfolio([lease]))

    needs_review = []
    if outcome.status == "needs_human_review":
        needs_review.append(outcome.reason or "사람 검토 필요")
    elif lease.party == "lessee":
        needs_review.extend([
            "회사 특수 리스 정책 서술",
            "변동리스료·전대리스·판매후리스 해당 여부",
        ])
    else:
        needs_review.append("리스제공자 주석 초안은 RP1 범위 밖")

    citations = _extract_citations(outcome.review_memo, disclosure_draft)
    return ReviewPack(
        standard="KIFRS1116",
        case_id=lease.label,
        status=outcome.status,
        judgment_summary=_summary_from_outcome(outcome),
        journal_entry=outcome.initial_entry,
        review_memo=outcome.review_memo,
        disclosure_draft=disclosure_draft,
        review_checklist=_checklist(lease, outcome, disclosure_draft),
        needs_human_review=needs_review,
        citations=citations,
    )


def render_review_pack_markdown(pack: ReviewPack) -> str:
    """Render a review pack into a workpaper-style markdown draft."""
    md: list[str] = [
        f"# F-ACC Review Pack — {pack.case_id}",
        "",
        f"- 기준서: {pack.standard}",
        f"- 상태: {pack.status}",
        f"- 판단 요약: {pack.judgment_summary}",
        "",
        "## 1. 검토메모",
        pack.review_memo or "- 자동 검토메모 없음",
        "",
        "## 2. 분개 초안",
        _entry_markdown(pack.journal_entry),
        "",
        "## 3. 주석 초안",
        pack.disclosure_draft or "- RP1 범위에서 자동 주석 초안 없음",
        "",
        "## 4. 리뷰 체크리스트",
    ]
    for item in pack.review_checklist:
        md.append(f"- [{item.status}] {item.label}: {item.note}")
    md.extend(["", "## 5. 사람 검토 필요 항목"])
    for item in pack.needs_human_review:
        md.append(f"- {item}")
    md.extend(["", "## 6. 인용"])
    for citation in pack.citations:
        md.append(f"- {citation}")
    return "\n".join(md)
