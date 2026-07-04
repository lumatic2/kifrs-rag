"""Turn validated feedback queue records into product incorporation actions."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Iterable

from .queue import FeedbackQueueRecord, split_queue, summarize_queue


ACTION_TYPES = {
    "add_review_question",
    "update_review_pack_checklist",
    "create_eval_seed",
    "create_backlog_item",
    "record_no_action",
}


@dataclass(frozen=True)
class IncorporationAction:
    action_id: str
    record_id: str
    case_id: str
    domain: str
    action_type: str
    target: str
    priority: str
    rationale: str
    suggested_change: str
    evidence_required: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def plan_incorporation(records: Iterable[FeedbackQueueRecord]) -> list[IncorporationAction]:
    """Create deterministic incorporation actions from feedback queue records."""
    actions: list[IncorporationAction] = []
    for record in records:
        priority = _priority(record)
        if record.disposition == "candidate":
            actions.append(_action(record, "create_eval_seed", "eval-suite", priority))
        elif record.disposition == "backlog_candidate":
            actions.append(_action(record, "create_backlog_item", "product-backlog", priority))
        elif record.disposition == "no_action":
            actions.append(_action(record, "record_no_action", "feedback-ledger", "low"))

        for output in record.affected_outputs:
            if output == "human_review_questions":
                actions.append(_action(record, "add_review_question", "field-feedback-questionnaire", priority))
            elif output == "review_pack":
                actions.append(_action(record, "update_review_pack_checklist", "f-acc-review-pack", priority))
    return actions


def render_incorporation_report(
    records: Iterable[FeedbackQueueRecord],
    *,
    title: str = "Accountant Feedback Incorporation Report",
) -> str:
    items = list(records)
    actions = plan_incorporation(items)
    summary = summarize_queue(items)
    split = split_queue(items)
    lines = [
        f"# {title}",
        "",
        "> Public-safe incorporation plan generated from validated feedback queue records.",
        "",
        "## Summary",
        "",
        f"- Queue records: {summary.total}",
        f"- Eval seed candidates: {len(split['eval_seed_candidate'])}",
        f"- Backlog candidates: {len(split['backlog_candidate'])}",
        f"- No-action records: {len(split['no_action'])}",
        f"- Incorporation actions: {len(actions)}",
        "",
        "## Actions",
        "",
        "| Action | Record | Type | Target | Priority | Suggested change |",
        "|---|---|---|---|---|---|",
    ]
    for action in actions:
        lines.append(
            f"| {action.action_id} | {action.record_id} | {action.action_type} | {action.target} | "
            f"{action.priority} | {action.suggested_change} |"
        )

    review_question_actions = [action for action in actions if action.action_type == "add_review_question"]
    if review_question_actions:
        lines.extend(["", "## Review Question Additions", ""])
        lines.extend(f"- {render_review_question(action)}" for action in review_question_actions)

    lines.extend([
        "",
        "## Eval/Backlog Rules",
        "",
        "- `candidate` queue records become eval seed actions.",
        "- `backlog_candidate` queue records become product backlog actions.",
        "- `no_action` records remain in the feedback ledger without changing demo assets.",
        "- High/blocker severity records are priority actions.",
        "",
        "## Boundary",
        "",
        "- This report uses queue metadata only.",
        "- It does not store raw contracts, customer identifiers, copied source bodies, private filings, parsed standards, embeddings, or workpaper payloads.",
    ])
    return "\n".join(lines) + "\n"


def render_review_question_supplement(
    records: Iterable[FeedbackQueueRecord],
    *,
    title: str = "Incorporated Review Question Supplement",
) -> str:
    actions = [action for action in plan_incorporation(records) if action.action_type == "add_review_question"]
    lines = [
        f"# {title}",
        "",
        "> Supplement for `docs/reports/field-feedback/2026-07-05-feedback-questionnaire.md`.",
        "> Generated from validated feedback queue records. This does not replace the original questionnaire.",
        "",
        "## Added Questions",
        "",
    ]
    if not actions:
        lines.append("- No new review questions.")
    else:
        for index, action in enumerate(actions, start=1):
            lines.append(f"{index}. {render_review_question(action)}")
            if action.evidence_required:
                lines.append(f"   - Required evidence: {', '.join(action.evidence_required)}")

    lines.extend([
        "",
        "## Boundary",
        "",
        "- These questions are candidates for the next field-feedback run.",
        "- They are not final accounting conclusions.",
    ])
    return "\n".join(lines) + "\n"


def render_review_question(action: IncorporationAction) -> str:
    if action.evidence_required:
        evidence = ", ".join(action.evidence_required)
        return f"Does the review pack explicitly request and evaluate {evidence}?"
    return f"Does the review pack address: {action.suggested_change}?"


def _action(
    record: FeedbackQueueRecord,
    action_type: str,
    target: str,
    priority: str,
) -> IncorporationAction:
    if action_type not in ACTION_TYPES:
        raise ValueError(f"unsupported incorporation action_type: {action_type}")
    return IncorporationAction(
        action_id=f"{record.record_id}:{action_type}",
        record_id=record.record_id,
        case_id=record.case_id,
        domain=record.domain,
        action_type=action_type,
        target=target,
        priority=priority,
        rationale=record.issue,
        suggested_change=record.expected_improvement,
        evidence_required=list(record.missing_evidence),
    )


def _priority(record: FeedbackQueueRecord) -> str:
    if record.severity in {"high", "blocker"}:
        return "high"
    if record.severity == "medium":
        return "medium"
    return "low"
