"""F-ACC review pack composition for K-IFRS 1109.

This module mirrors the 1116 review pack pattern for financial instruments. It
does not add new classification logic; it wraps the existing 1109 runner,
review memo, and journal entry outputs into one Accounting Advisory workpaper
draft.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import re

from .initial_entry import JournalEntry
from .reclassification import generate_reclassification_memo
from .runner import ScenarioOutcome, run_scenario
from .fixtures import ScenarioFixture


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
    classification: str | None
    judgment_summary: str
    journal_entry: JournalEntry | None
    review_memo: str | None
    review_checklist: list[ReviewChecklistItem] = field(default_factory=list)
    needs_human_review: list[HumanReviewAction] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)


def _extract_citations(*texts: str | None) -> list[str]:
    citations: set[str] = set()
    for text in texts:
        if not text:
            continue
        citations.update(re.findall(r"\[\d{4}-[A-Za-z0-9()~.,·/\- ]+\]", text))
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


def _summary_from_outcome(outcome: ScenarioOutcome) -> str:
    if outcome.status == "needs_human_review":
        return outcome.reason or "사람 검토 필요"
    return (
        f"{outcome.label}: {outcome.classification} 분류로 자동 판단. "
        f"최초인식 {outcome.initial_total:,.0f}, 후속분개 {outcome.subsequent_entry_count}개 산출."
    )


def _human_review_actions(fixture: ScenarioFixture, outcome: ScenarioOutcome) -> list[HumanReviewAction]:
    txn = fixture.txn
    if output_reason := outcome.reason if outcome.status == "needs_human_review" else None:
        special_case = txn.special_case or "unknown"
        if special_case == "ifric19_debt_equity_swap":
            return [
                HumanReviewAction(
                    issue="IFRIC 19 부채-지분 스왑",
                    why_blocked="채무자가 금융부채를 지분상품 발행으로 소멸시키는 거래는 WA1 1109 core pipeline 밖이다.",
                    required_inputs=["교환되는 금융부채 장부금액", "발행 지분상품 공정가치", "기존 채무조건 변경 내역"],
                    review_questions=["기존 금융부채가 제거되는지?", "발행 지분상품 공정가치를 신뢰성 있게 측정할 수 있는지?"],
                    candidate_guidance=["K-IFRS 1109 제거 판단과 IFRIC 19 적용 여부를 별도 검토"],
                )
            ]
        if special_case == "sppi_reset_mismatch":
            return [
                HumanReviewAction(
                    issue="변동금리 재설정 불일치 SPPI 판단",
                    why_blocked="이자율 재설정 주기와 기준금리 테너가 불일치하는 경우 현금흐름 특성 판단이 추가로 필요하다.",
                    required_inputs=["계약상 기준금리", "재설정 주기", "이자 산정기간", "시장금리 보정 조항"],
                    review_questions=["시간가치 요소 변형이 유의적인지?", "benchmark cash flow와 비교가 필요한지?"],
                    candidate_guidance=["[1109-B4.1.7~7B] 이자 구성요소와 시간가치 판단"],
                )
            ]
        if special_case == "reclassification":
            return [
                HumanReviewAction(
                    issue="사업모형 변경에 따른 재분류",
                    why_blocked="금융자산 재분류는 사업모형 변경의 사실, 재분류일, 공정가치 입력이 필요해 자동 결론 대신 skeleton을 제공한다.",
                    required_inputs=[
                        "사업모형 변경 승인 자료",
                        "변경일 및 재분류일",
                        "변경 전후 보유 목적",
                        "재분류일 공정가치",
                        "기존 장부금액과 유효이자율",
                        "변경 전후 분류 후보(AC/FVOCI/FVPL)",
                    ],
                    review_questions=[
                        "사업모형 변경이 외부적으로 관찰 가능한지?",
                        "경영진 의도 변경만이 아니라 실제 사업 활동 변경인지?",
                        "재분류일 이후 전진 적용이 맞는지?",
                        "재분류일 공정가치를 신뢰성 있게 측정할 수 있는지?",
                    ],
                    candidate_guidance=["K-IFRS 1109 재분류 규정, 재분류일, 전진 적용 여부 검토"],
                )
            ]
        if special_case == "fx_dual_track":
            return [
                HumanReviewAction(
                    issue="외화 금융상품 1109+1021 이중 트랙",
                    why_blocked="분류·측정은 1109, 외화환산은 1021 판단이 함께 필요해 WA1 core pipeline 밖이다.",
                    required_inputs=["기능통화", "계약통화", "취득일·보고일 환율", "공정가치 변동과 환산차이 분해 자료"],
                    review_questions=["환산차이와 공정가치 변동을 어느 손익/OCI 라인에 표시할지?", "FVOCI 부채상품인지 FVPL인지?"],
                    candidate_guidance=["K-IFRS 1109 분류 결과와 K-IFRS 1021 외화환산 표시를 함께 검토"],
                )
            ]
        return [
            HumanReviewAction(
                issue="자동 판단 중단 사유",
                why_blocked=output_reason,
                required_inputs=["계약 원문", "거래 구조 요약", "경영진 보유 목적", "측정 입력값"],
                review_questions=["WA1 core pipeline 밖 특수 사실관계가 무엇인지?"],
            )
        ]

    classification = outcome.classification or "미정"
    return [
        HumanReviewAction(
            issue="회사 보유 목적과 회계정책 확인",
            why_blocked="자동 분류는 fixture 입력에 근거한 초안이며 실제 회사의 사업모형 evidence와 회계정책 문구는 별도 확인이 필요하다.",
            required_inputs=["금융상품 보유 목적 문서", "성과평가 방식", "매각 빈도와 사유", "위험관리 정책"],
            review_questions=[f"{classification} 분류가 회사의 실제 보유 목적과 일치하는지?", "회계정책 주석 문구가 필요한지?"],
        ),
        HumanReviewAction(
            issue="후속측정 입력값 검토",
            why_blocked="유효이자율, 기말 공정가치, 배당/이자 현금흐름은 외부 자료 또는 회사 자료 대사가 필요하다.",
            required_inputs=["유효이자율 산정 근거", "기말 공정가치 자료", "이자·배당 현금흐름", "거래원가 증빙"],
            review_questions=["후속측정 분개가 회사 원장과 대사되는지?", "FVOCI/FVPL 평가손익 표시가 맞는지?"],
        ),
    ]


def _checklist(outcome: ScenarioOutcome, needs_review: list[HumanReviewAction]) -> list[ReviewChecklistItem]:
    if outcome.status == "needs_human_review":
        issue = needs_review[0].issue if needs_review else "자동 판단 중단 사유"
        return [
            ReviewChecklistItem("중단 사유 식별", "needs_human_review", issue),
            ReviewChecklistItem("추가자료 수집", "needs_human_review", "사람 검토 필요 항목의 필요한 추가자료 수집"),
            ReviewChecklistItem("판단 질문 답변", "needs_human_review", "사람 검토 필요 항목의 리뷰 질문에 결론 기재"),
        ]

    return [
        ReviewChecklistItem("SPPI/사업모형 판단", "ready", f"분류: {outcome.classification}"),
        ReviewChecklistItem("최초분개 검토", "ready", "초안 금액, 거래원가 처리, 차대 일치 확인"),
        ReviewChecklistItem("후속측정 검토", "ready", f"후속분개 {outcome.subsequent_entry_count}개 산출"),
        ReviewChecklistItem("검토메모 문구 검토", "ready", "회사 보유 목적, 공정가치 출처, 회계정책 표현 보완"),
    ]


def generate_review_pack(fixture: ScenarioFixture) -> ReviewPack:
    """Run the 1109 pipeline and compose a F-ACC workpaper pack."""
    outcome = run_scenario(fixture)
    needs_review = _human_review_actions(fixture, outcome)
    review_memo = outcome.review_memo
    if fixture.txn.special_case == "reclassification":
        review_memo = generate_reclassification_memo(fixture.txn)
    citations = _extract_citations(review_memo)
    for action in needs_review:
        citations.extend(_extract_citations(*action.candidate_guidance))
    citations = sorted(set(citations))

    return ReviewPack(
        standard="KIFRS1109",
        case_id=fixture.txn.label,
        status=outcome.status,
        classification=outcome.classification,
        judgment_summary=_summary_from_outcome(outcome),
        journal_entry=outcome.initial_entry,
        review_memo=review_memo,
        review_checklist=_checklist(outcome, needs_review),
        needs_human_review=needs_review,
        citations=citations,
    )


def render_review_pack_markdown(pack: ReviewPack) -> str:
    """Render a 1109 review pack into a workpaper-style markdown draft."""
    md: list[str] = [
        f"# F-ACC Review Pack — {pack.case_id}",
        "",
        f"- 기준서: {pack.standard}",
        f"- 상태: {pack.status}",
        f"- 분류: {pack.classification or '사람 검토 필요'}",
        f"- 판단 요약: {pack.judgment_summary}",
        "",
        "## 1. 검토메모",
        pack.review_memo or "- 자동 검토메모 없음",
        "",
        "## 2. 분개 초안",
        _entry_markdown(pack.journal_entry),
        "",
        "## 3. 리뷰 체크리스트",
    ]
    for item in pack.review_checklist:
        md.append(f"- [{item.status}] {item.label}: {item.note}")
    md.extend(["", "## 4. 사람 검토 필요 항목"])
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
    md.extend(["", "## 5. 인용"])
    for citation in pack.citations:
        md.append(f"- {citation}")
    return "\n".join(md)
