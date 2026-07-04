import importlib.util
import sys
from pathlib import Path

from kifrs.eval.models import Citation, GoldItem


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "hard_miss_candidate_eval", ROOT / "scripts" / "hard_miss_candidate_eval.py"
)
hard_miss_candidate_eval = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = hard_miss_candidate_eval
SPEC.loader.exec_module(hard_miss_candidate_eval)


def _item():
    return GoldItem(
        id="QX",
        source="test",
        source_ref="test",
        question="test question",
        must_cite=[Citation("1115", "27"), Citation("1115", "22")],
    )


def test_evaluate_candidates_accepts_recovered_target_with_existing_hit_preserved():
    candidate = hard_miss_candidate_eval.HardMissCandidate(
        "QX", "candidate", "1115-27", "expanded terms", "test"
    )

    def search_fn(query, standard, limit):
        if "expanded" in query:
            return [
                {"standard": "1115", "no": "22"},
                {"standard": "1115", "no": "27"},
            ]
        return [{"standard": "1115", "no": "22"}]

    report = hard_miss_candidate_eval.evaluate_candidates(
        [_item()],
        (candidate,),
        search_fn=search_fn,
        limit=20,
        gate_k=20,
    )

    row = report["rows"][0]
    assert row["candidate"] is True
    assert row["target_improved"] is True
    assert row["preserves_existing_hits"] is True


def test_evaluate_candidates_rejects_lost_existing_hit():
    candidate = hard_miss_candidate_eval.HardMissCandidate(
        "QX", "candidate", "1115-27", "expanded terms", "test"
    )

    def search_fn(query, standard, limit):
        if "expanded" in query:
            return [{"standard": "1115", "no": "27"}]
        return [{"standard": "1115", "no": "22"}]

    report = hard_miss_candidate_eval.evaluate_candidates(
        [_item()],
        (candidate,),
        search_fn=search_fn,
        limit=20,
        gate_k=20,
    )

    row = report["rows"][0]
    assert row["candidate"] is False
    assert row["target_improved"] is True
    assert row["preserves_existing_hits"] is False


def test_render_markdown_includes_decision_table():
    text = hard_miss_candidate_eval.render_markdown(
        {
            "limit": 20,
            "gate_k": 20,
            "rows": [
                {
                    "item_id": "QX",
                    "candidate_id": "candidate",
                    "target_citation": "1115-27",
                    "expansion": "expanded terms",
                    "target_rank_before": None,
                    "target_rank_after": 3,
                    "candidate": True,
                    "baseline_ranks": {"1115-27": None},
                    "expanded_ranks": {"1115-27": 3},
                    "target_improved": True,
                    "preserves_existing_hits": True,
                    "rationale": "test",
                }
            ],
        }
    )

    assert "# Hard Miss Candidate Evaluation" in text
    assert "| QX | `candidate` | `1115-27` | absent | 3 | candidate |" in text
