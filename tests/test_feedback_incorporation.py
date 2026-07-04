from __future__ import annotations

from kifrs.feedback.queue import FeedbackQueueRecord
from kifrs.feedback.incorporation import (
    plan_incorporation,
    render_incorporation_report,
    render_review_question_supplement,
)


def _record(
    *,
    disposition: str = "candidate",
    severity: str = "medium",
    affected_outputs: list[str] | None = None,
) -> FeedbackQueueRecord:
    return FeedbackQueueRecord(
        record_id="anon-lease-poc-001:eval_seed_candidate:lease-term",
        case_id="anon-lease-poc-001",
        domain="KIFRS1116",
        route="kifrs1116_review_pack",
        disposition=disposition,
        severity=severity,
        issue="Lease term evidence question should be explicit",
        expected_improvement="Add a required reviewer question for lease term evidence.",
        missing_evidence=["lease term approval evidence"],
        affected_outputs=["human_review_questions", "review_pack"] if affected_outputs is None else affected_outputs,
        source="test",
    )


def test_plan_incorporation_creates_eval_and_output_actions() -> None:
    actions = plan_incorporation([_record()])

    assert [action.action_type for action in actions] == [
        "create_eval_seed",
        "add_review_question",
        "update_review_pack_checklist",
    ]
    assert {action.priority for action in actions} == {"medium"}


def test_plan_incorporation_routes_backlog_and_high_priority() -> None:
    actions = plan_incorporation([_record(disposition="backlog_candidate", severity="high", affected_outputs=[])])

    assert len(actions) == 1
    assert actions[0].action_type == "create_backlog_item"
    assert actions[0].priority == "high"


def test_plan_incorporation_records_no_action_without_product_update() -> None:
    actions = plan_incorporation([_record(disposition="no_action", affected_outputs=[])])

    assert len(actions) == 1
    assert actions[0].action_type == "record_no_action"
    assert actions[0].target == "feedback-ledger"


def test_render_incorporation_report_contains_rules_and_boundary() -> None:
    rendered = render_incorporation_report([_record()])

    assert "Incorporation actions: 3" in rendered
    assert "Review Question Additions" in rendered
    assert "candidate` queue records become eval seed actions" in rendered
    assert "raw contracts" in rendered


def test_render_review_question_supplement_uses_missing_evidence() -> None:
    rendered = render_review_question_supplement([_record()])

    assert "Does the review pack explicitly request and evaluate lease term approval evidence?" in rendered
    assert "This does not replace the original questionnaire" in rendered
