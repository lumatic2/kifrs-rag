import importlib.util
import sys
from pathlib import Path

from kifrs.eval.models import Citation, GoldItem


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "ifrs1115_subquery_candidate_eval", ROOT / "scripts" / "ifrs1115_subquery_candidate_eval.py"
)
ifrs1115_subquery_candidate_eval = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = ifrs1115_subquery_candidate_eval
SPEC.loader.exec_module(ifrs1115_subquery_candidate_eval)


def _item():
    return GoldItem(
        id="QX",
        source="test",
        source_ref="test",
        question="baseline question",
        must_cite=[Citation("1115", "22"), Citation("1115", "27")],
    )


def test_evaluate_subqueries_accepts_recovered_target_and_preserved_hit():
    candidate = ifrs1115_subquery_candidate_eval.SubqueryCandidate(
        "QX",
        "candidate",
        "1115-27",
        "1115",
        "subquery",
        "test",
    )

    def baseline_search_fn(query, standard, limit):
        return [{"standard": "1115", "no": "22"}]

    def subquery_search_fn(query, standard, limit):
        return [{"standard": "1115", "no": "27"}, {"standard": "1115", "no": "22"}]

    report = ifrs1115_subquery_candidate_eval.evaluate_subqueries(
        [_item()],
        (candidate,),
        baseline_search_fn=baseline_search_fn,
        subquery_search_fn=subquery_search_fn,
        k=20,
        limit=20,
        subquery_weight=1,
    )

    row = report["rows"][0]
    assert row["candidate"] is True
    assert row["target_recovered"] is True
    assert row["preserves_existing_hits"] is True


def test_evaluate_subqueries_rejects_when_existing_hit_is_lost():
    candidate = ifrs1115_subquery_candidate_eval.SubqueryCandidate(
        "QX",
        "candidate",
        "1115-27",
        "1115",
        "subquery",
        "test",
    )

    def baseline_search_fn(query, standard, limit):
        return [{"standard": "1115", "no": "22"}]

    def subquery_search_fn(query, standard, limit):
        return [{"standard": "1115", "no": "27"}]

    report = ifrs1115_subquery_candidate_eval.evaluate_subqueries(
        [_item()],
        (candidate,),
        baseline_search_fn=baseline_search_fn,
        subquery_search_fn=subquery_search_fn,
        k=1,
        limit=1,
        subquery_weight=2,
    )

    row = report["rows"][0]
    assert row["candidate"] is False
    assert row["target_recovered"] is True
    assert row["preserves_existing_hits"] is False


def test_render_markdown_includes_candidate_decision():
    text = ifrs1115_subquery_candidate_eval.render_markdown(
        {
            "k": 20,
            "limit": 100,
            "subquery_weight": 2,
            "rows": [
                {
                    "item_id": "Q001",
                    "candidate_id": "q001-performance-obligation-criteria",
                    "target_citation": "1115-27",
                    "target_rank_before": None,
                    "target_rank_after": 15,
                    "candidate": True,
                    "subquery": "subquery",
                    "baseline_ranks": {"1115-27": None},
                    "subquery_ranks": {"1115-27": 1},
                    "fused_ranks": {"1115-27": 15},
                    "preserves_existing_hits": True,
                    "rationale": "test",
                }
            ],
        }
    )

    assert "# IFRS 1115 Subquery Candidate Evaluation" in text
    assert "| Q001 | `q001-performance-obligation-criteria` | `1115-27` | absent | 15 | candidate |" in text
