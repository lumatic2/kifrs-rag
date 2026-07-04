"""F-ACC review pack composition for K-IFRS 1115."""

from dataclasses import dataclass, field

from .classify import NeedsHumanReview, RevenueDecision, evaluate_revenue
from .fixtures import ScenarioFixture
from .journal_entry import JournalEntry, draft_journal_entries
from .measurement import RevenueMeasurement, measure_revenue
from .review_memo import generate_review_memo
from .schema import Revenue1115


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
    path: str | None
    judgment_summary: str
    journal_entries: list[JournalEntry] = field(default_factory=list)
    review_memo: str | None = None
    measurement: RevenueMeasurement | None = None
    review_checklist: list[ReviewChecklistItem] = field(default_factory=list)
    needs_human_review: list[HumanReviewAction] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)


def generate_review_pack(source: ScenarioFixture | Revenue1115) -> ReviewPack:
    txn = source.txn if isinstance(source, ScenarioFixture) else source
    try:
        decision = evaluate_revenue(txn)
        measurement = measure_revenue(txn, decision)
        entries = draft_journal_entries(txn, decision, measurement)
        memo = generate_review_memo(txn, decision, measurement, entries)
    except NeedsHumanReview as exc:
        actions = _needs_human_review_actions(txn, str(exc))
        return ReviewPack(
            standard="KIFRS1115",
            case_id=txn.label,
            status="needs_human_review",
            path=None,
            judgment_summary=str(exc),
            review_checklist=_needs_review_checklist(actions),
            needs_human_review=actions,
        )

    actions = _automated_human_review_actions(txn, decision)
    return ReviewPack(
        standard="KIFRS1115",
        case_id=txn.label,
        status="automated",
        path=decision.path,
        judgment_summary=_summary_from_decision(decision, measurement, entries),
        journal_entries=entries,
        review_memo=memo,
        measurement=measurement,
        review_checklist=_automated_checklist(decision, measurement, entries),
        needs_human_review=actions,
        citations=_collect_citations(decision),
    )


def render_review_pack_markdown(pack: ReviewPack) -> str:
    md: list[str] = [
        f"# F-ACC Review Pack — {pack.case_id}",
        "",
        f"- 기준서: {pack.standard}",
        f"- 상태: {pack.status}",
        f"- 판단 경로: {pack.path or '사람 검토 필요'}",
        f"- 판단 요약: {pack.judgment_summary}",
        "",
        "## 1. 검토메모",
        pack.review_memo or "- 자동 검토메모 없음",
        "",
        "## 2. 분개 초안",
    ]
    if pack.journal_entries:
        for entry in pack.journal_entries:
            md.extend(_entry_markdown(entry))
    else:
        md.append("- 자동 분개 초안 없음")

    md.extend(["", "## 3. 리뷰 체크리스트"])
    for item in pack.review_checklist:
        md.append(f"- [{item.status}] {item.label}: {item.note}")

    md.extend(["", "## 4. 사람 검토 필요 항목"])
    for action in pack.needs_human_review:
        md.append(f"### {action.issue}")
        md.append(f"- 왜 필요한가: {action.why_blocked}")
        if action.required_inputs:
            md.append("- 필요한 추가자료:")
            md.extend(f"  - {item}" for item in action.required_inputs)
        if action.review_questions:
            md.append("- 리뷰 질문:")
            md.extend(f"  - {item}" for item in action.review_questions)
        if action.candidate_guidance:
            md.append("- 기준서 처리 방향:")
            md.extend(f"  - {item}" for item in action.candidate_guidance)

    md.extend(["", "## 5. 인용"])
    for citation in pack.citations:
        md.append(f"- {citation}")
    return "\n".join(md)


def _summary_from_decision(
    decision: RevenueDecision,
    measurement: RevenueMeasurement,
    entries: list[JournalEntry],
) -> str:
    return (
        f"{decision.label}: {decision.path} 경로로 자동 판단. "
        f"수익 초안 {measurement.recognized_revenue:,.0f}, 분개 초안 {len(entries)}개 산출."
    )


def _collect_citations(decision: RevenueDecision) -> list[str]:
    citations = set(decision.citations)
    for step in decision.five_step:
        citations.update(step.citations)
    return sorted(citations)


def _automated_checklist(
    decision: RevenueDecision,
    measurement: RevenueMeasurement,
    entries: list[JournalEntry],
) -> list[ReviewChecklistItem]:
    return [
        ReviewChecklistItem("5단계 판단", "ready", f"{len(decision.five_step)}개 step 결론 산출"),
        ReviewChecklistItem("측정표", "ready", f"수익 {measurement.recognized_revenue:,.0f}, 이연 {measurement.deferred_revenue:,.0f}"),
        ReviewChecklistItem("분개 초안", "ready", f"분개 {len(entries)}개, 차대 일치 확인"),
        ReviewChecklistItem("검토메모", "ready", "거래개요, 판단, 측정, 분개, 결론 섹션 포함"),
    ]


def _needs_review_checklist(actions: list[HumanReviewAction]) -> list[ReviewChecklistItem]:
    issue = actions[0].issue if actions else "자동 판단 중단"
    return [
        ReviewChecklistItem("중단 사유 식별", "needs_human_review", issue),
        ReviewChecklistItem("추가자료 수집", "needs_human_review", "필수 입력값과 계약 원문 확인"),
        ReviewChecklistItem("수동 판단 메모", "needs_human_review", "리뷰 질문에 답한 뒤 workpaper 작성"),
    ]


def _automated_human_review_actions(
    txn: Revenue1115, decision: RevenueDecision
) -> list[HumanReviewAction]:
    return [
        HumanReviewAction(
            issue="입력 사실과 추정치 검토",
            why_blocked="자동 산출물은 구조화 fixture 입력에 근거한 초안이며 실제 계약 원문, 확률, SSP, 지급조건은 사람이 확인해야 한다.",
            required_inputs=["계약 원문", "독립판매가격 근거", "권리 행사 확률", "지급조건", "경영진 판단 메모"],
            review_questions=[
                f"{decision.path} 경로가 실제 계약 조건과 일치하는지?",
                "금액 산정에 사용한 SSP/확률/현금판매가격이 외부 증거와 일치하는지?",
            ],
        )
    ]


def _needs_human_review_actions(txn: Revenue1115, reason: str) -> list[HumanReviewAction]:
    return [
        HumanReviewAction(
            issue="1115 자동 판단 중단",
            why_blocked=reason,
            required_inputs=["계약 식별 조건", "수행의무 목록", "거래가격 입력값", "지급조건", "재매입/선택권 조항"],
            review_questions=["어떤 1115 path로 분기해야 하는지?", "필수 입력값 중 누락된 항목은 무엇인지?"],
            candidate_guidance=["R15 엔진이 지원하지 않는 사실관계면 별도 수동 검토메모 작성"],
        )
    ]


def _entry_markdown(entry: JournalEntry) -> list[str]:
    lines = [f"- {entry.label}"]
    for line in entry.lines:
        if line.debit:
            lines.append(f"  - (차) {line.account}: {line.debit:,.0f}")
        if line.credit:
            lines.append(f"  - (대) {line.account}: {line.credit:,.0f}")
    return lines
