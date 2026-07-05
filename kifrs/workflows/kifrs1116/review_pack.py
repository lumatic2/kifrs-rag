"""F-ACC review pack composition for K-IFRS 1116.

This module does not add new lease judgment logic. It wraps the existing 1116
runner, review memo, journal entry, and lessee disclosure draft into one
Accounting Advisory workpaper-style output.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import re

from kifrs.runtime.authority_boundary import (
    RuntimeAuthorityBoundary,
    authority_boundary_references,
    render_runtime_authority_boundary_data,
)
from kifrs.runtime.evidence import EvidenceBundle
from kifrs.runtime.evidence_panel import evidence_references, render_external_evidence_panel

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
class HumanReviewAction:
    issue: str
    why_blocked: str
    required_inputs: list[str] = field(default_factory=list)
    review_questions: list[str] = field(default_factory=list)
    candidate_guidance: list[str] = field(default_factory=list)


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
    needs_human_review: list[HumanReviewAction] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)
    external_evidence: list[dict[str, object]] = field(default_factory=list)
    authority_boundary: dict[str, list[dict[str, object]]] = field(default_factory=dict)


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


def _human_review_actions(lease: Lease1116, outcome: LeaseOutcome) -> list[HumanReviewAction]:
    if outcome.status == "needs_human_review":
        if lease.special_case == "modification_expand_shrink_two_dimensional":
            return [
                HumanReviewAction(
                    issue="리스범위 확장+축소 동시 변경",
                    why_blocked=(
                        "축소분 손익 인식과 잔여/확장분 재측정을 분리해야 해서 "
                        "RP1/RP2 단일 변경 경로로 자동 판단하지 않는다."
                    ),
                    required_inputs=[
                        "변경 전 리스부채와 사용권자산 장부금액",
                        "축소되는 사용권 범위와 축소 비율",
                        "확장되는 사용권 범위, 기간, 대가",
                        "변경일 현재 수정 할인율",
                        "변경 전후 리스료 지급 스케줄",
                    ],
                    review_questions=[
                        "축소분이 별도 리스 종료 또는 부분 종료인지?",
                        "확장분이 별도 리스인지 기존 리스 변경인지?",
                        "축소분 사용권자산 제거 비율과 손익 계산 근거는?",
                        "잔여/확장분 리스부채 재측정에 적용할 할인율은?",
                    ],
                    candidate_guidance=[
                        "[1116-45] 변경 리스료를 수정 할인율로 할인해 리스부채를 재측정",
                        "[1116-46(a)] 범위 축소는 사용권자산 장부금액을 감소시키고 관련 손익 인식",
                        "[1116-46(b)] 그 밖의 변경은 사용권자산 조정",
                    ],
                )
            ]
        return [
            HumanReviewAction(
                issue="자동 판단 중단 사유",
                why_blocked=outcome.reason or "사람 검토 필요",
                required_inputs=["중단 사유와 관련된 계약 원문, 변경 합의서, 지급 스케줄"],
                review_questions=["현재 fixture/엔진 경계 밖 특수 사실관계가 무엇인지?"],
            )
        ]

    if lease.party == "lessee":
        return [
            HumanReviewAction(
                issue="회사 특수 리스 정책 서술",
                why_blocked="자동 산출물은 기준서 기반 초안이며 회사 회계정책 문구와 중요성 판단은 별도 확인이 필요하다.",
                required_inputs=["회사의 리스 회계정책 문구", "중요성 기준", "단기리스·소액기초자산 면제 적용 정책"],
                review_questions=["초안 문구가 회사 기존 주석 문체와 일관되는지?", "면제 규정 적용 여부가 누락되지 않았는지?"],
            ),
            HumanReviewAction(
                issue="조건부 리스 주석 항목",
                why_blocked="변동리스료, 전대리스, 판매후리스는 fixture 입력만으로 회사 전체 주석 완결성을 보장할 수 없다.",
                required_inputs=["변동리스료 내역", "전대리스 계약 목록", "판매후리스 거래 여부", "만기분석용 지급 스케줄"],
                review_questions=["변동리스료가 당기손익 또는 사용권자산에 반영될 성격인지?", "전대리스·판매후리스 공시가 필요한지?"],
                candidate_guidance=["[1116-53] 리스이용자 주석 요구사항", "[1116-59] 추가 질적·양적 정보 제공"],
            ),
        ]

    return [
        HumanReviewAction(
            issue="리스제공자 주석 초안",
            why_blocked="RP1~RP3 review pack은 리스이용자 주석 초안만 자동화 범위에 포함한다.",
            required_inputs=["리스제공자 금융리스/운용리스 분류", "수익 인식 스케줄", "리스채권 또는 기초자산 관련 주석 자료"],
            review_questions=["리스제공자 주석 자동화가 이번 PoC 범위에 필요한지?"],
        )
    ]


def _checklist(
    lease: Lease1116,
    outcome: LeaseOutcome,
    disclosure_draft: str | None,
    needs_review: list[HumanReviewAction],
) -> list[ReviewChecklistItem]:
    if outcome.status == "needs_human_review":
        issue = needs_review[0].issue if needs_review else "자동 판단 중단 사유"
        return [
            ReviewChecklistItem(
                label="중단 사유 식별",
                status="needs_human_review",
                note=issue,
            ),
            ReviewChecklistItem("추가자료 수집", "needs_human_review", "사람 검토 필요 항목의 필요한 추가자료를 먼저 수집"),
            ReviewChecklistItem("판단 질문 답변", "needs_human_review", "사람 검토 필요 항목의 리뷰 질문에 근거와 결론 기재"),
            ReviewChecklistItem("기준서 처리 방향 검토", "needs_human_review", "후보 기준서 방향을 확인한 뒤 수동 workpaper 작성"),
        ]

    items = [
        ReviewChecklistItem("리스 식별/분류 판단", "ready", f"자동 판단 경로: {outcome.path}"),
        ReviewChecklistItem("최초분개 검토", "ready", "초안 금액, 차대 일치, 지급시점 가정 확인"),
        ReviewChecklistItem("검토메모 문구 검토", "ready", "계약명, 날짜, 회사 특수 사실관계, 결론 문구 보완"),
    ]
    if lease.party == "lessee":
        items.append(
            ReviewChecklistItem(
                "리스 주석 초안 검토",
                "ready" if disclosure_draft else "needs_human_review",
                "만기분석, 변동리스료, 전대리스, 판매후리스, 단기·소액 면제 항목을 회사 자료로 보완",
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


def generate_review_pack(
    lease: Lease1116,
    evidence_bundle: EvidenceBundle | None = None,
    authority_boundary: RuntimeAuthorityBoundary | None = None,
) -> ReviewPack:
    """Run the 1116 pipeline and compose a F-ACC workpaper pack."""
    outcome = run_lease(lease)

    disclosure_draft: str | None = None
    if outcome.status == "automated" and lease.party == "lessee":
        disclosure_draft = generate_disclosure_note(aggregate_portfolio([lease]))

    needs_review = _human_review_actions(lease, outcome)

    citations = _extract_citations(outcome.review_memo, disclosure_draft)
    return ReviewPack(
        standard="KIFRS1116",
        case_id=lease.label,
        status=outcome.status,
        judgment_summary=_summary_from_outcome(outcome),
        journal_entry=outcome.initial_entry,
        review_memo=outcome.review_memo,
        disclosure_draft=disclosure_draft,
        review_checklist=_checklist(lease, outcome, disclosure_draft, needs_review),
        needs_human_review=needs_review,
        citations=citations,
        external_evidence=evidence_references(evidence_bundle),
        authority_boundary=authority_boundary_references(authority_boundary),
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
    for action in pack.needs_human_review:
        md.append(f"### {action.issue}")
        md.append(f"- 왜 멈췄나: {action.why_blocked}")
        if action.required_inputs:
            md.append("- 필요한 추가자료:")
            md.extend(f"  - {item}" for item in action.required_inputs)
        if action.review_questions:
            md.append("- 리뷰 질문:")
            md.extend(f"  - {item}" for item in action.review_questions)
        if action.candidate_guidance:
            md.append("- 기준서 처리 방향:")
            md.extend(f"  - {item}" for item in action.candidate_guidance)
    md.extend(["", *render_external_evidence_panel(pack.external_evidence)])
    if pack.authority_boundary:
        md.extend(["", render_runtime_authority_boundary_data(pack.authority_boundary)])
    md.extend(["", "## 6. 인용"])
    for citation in pack.citations:
        md.append(f"- {citation}")
    return "\n".join(md)
