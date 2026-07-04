from __future__ import annotations

from kifrs.eval.models import Citation, GoldItem
from scripts.term_bridge_candidate_eval import (
    TermBridgeCandidate,
    evaluate_candidates,
    render_markdown,
)


def _item(item_id: str = "QX") -> GoldItem:
    return GoldItem(
        id=item_id,
        question="원 질문",
        must_cite=[Citation("1037", "14"), Citation("1116", "24")],
        may_cite=[],
        source="test",
        source_ref="test",
        keywords=[],
        forbidden_keywords=[],
        notes="",
    )


def test_evaluate_candidates_marks_absent_target_recovered() -> None:
    candidate = TermBridgeCandidate(
        item_id="QX",
        candidate_id="candidate-1",
        trigger="충당부채",
        expansion="현재의무",
        target_citation="1037-14",
        rationale="test",
    )

    def fake_search(query: str, standard: str | None, limit: int) -> list[dict]:
        if "현재의무" in query:
            return [{"standard": "1037", "no": "14"}, {"standard": "1116", "no": "24"}]
        return [{"standard": "1116", "no": "24"}]

    report = evaluate_candidates([_item()], (candidate,), search_fn=fake_search)

    row = report["rows"][0]
    assert row["target_rank_before"] is None
    assert row["target_rank_after"] == 1
    assert row["target_improved"] is True
    assert row["preserves_existing_hits"] is True
    assert row["candidate"] is True


def test_evaluate_candidates_rejects_candidate_that_loses_target() -> None:
    candidate = TermBridgeCandidate(
        item_id="QX",
        candidate_id="candidate-1",
        trigger="충당부채",
        expansion="현재의무",
        target_citation="1037-14",
        rationale="test",
    )

    def fake_search(query: str, standard: str | None, limit: int) -> list[dict]:
        if "현재의무" in query:
            return [{"standard": "1116", "no": "24"}]
        return [{"standard": "1037", "no": "14"}, {"standard": "1116", "no": "24"}]

    report = evaluate_candidates([_item()], (candidate,), search_fn=fake_search)

    row = report["rows"][0]
    assert row["target_rank_before"] == 1
    assert row["target_rank_after"] is None
    assert row["candidate"] is False


def test_evaluate_candidates_rejects_candidate_that_loses_existing_hit() -> None:
    candidate = TermBridgeCandidate(
        item_id="QX",
        candidate_id="candidate-1",
        trigger="충당부채",
        expansion="현재의무",
        target_citation="1037-14",
        rationale="test",
    )

    def fake_search(query: str, standard: str | None, limit: int) -> list[dict]:
        if "현재의무" in query:
            return [{"standard": "1037", "no": "14"}]
        return [{"standard": "1116", "no": "24"}]

    report = evaluate_candidates([_item()], (candidate,), search_fn=fake_search)

    row = report["rows"][0]
    assert row["target_improved"] is True
    assert row["preserves_existing_hits"] is False
    assert row["candidate"] is False


def test_render_markdown_summarizes_candidate_decisions() -> None:
    report = {
        "limit": 50,
        "gate_k": 20,
        "rows": [
            {
                "item_id": "QX",
                "candidate_id": "candidate-1",
                "trigger": "충당부채",
                "expansion": "현재의무",
                "target_citation": "1037-14",
                "target_rank_before": None,
                "target_rank_after": 3,
                "target_improved": True,
                "preserves_existing_hits": True,
                "candidate": True,
                "base_ranks": {"1037-14": None},
                "candidate_ranks": {"1037-14": 3},
                "rationale": "test",
            }
        ],
    }

    rendered = render_markdown(report)

    assert "# Term Bridge Candidate Evaluation" in rendered
    assert "`candidate-1`" in rendered
    assert "candidate" in rendered
