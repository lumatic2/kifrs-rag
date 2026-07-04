import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "retrieval_must_cite_report", ROOT / "scripts" / "retrieval_must_cite_report.py"
)
retrieval_must_cite_report = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(retrieval_must_cite_report)


def test_render_markdown_includes_summary_and_rows():
    text = retrieval_must_cite_report.render_markdown(
        {
            "n_items": 2,
            "k": 20,
            "summary": {
                "hybrid": {
                    "hit@5": 1,
                    "hit@10": 0,
                    "hit@20": 1,
                    "beyond@20": 0,
                    "absent": 1,
                }
            },
            "rows": [
                {
                    "retriever": "hybrid",
                    "item_id": "Q039",
                    "citation": "1037-14",
                    "rank": 16,
                    "bucket": "hit@20",
                },
                {
                    "retriever": "hybrid",
                    "item_id": "Q048",
                    "citation": "1036-18",
                    "rank": None,
                    "bucket": "absent",
                },
            ],
        }
    )

    assert "# Must-Cite Retrieval Rank Report" in text
    assert "| hybrid | 1 | 0 | 1 | 0 | 1 |" in text
    assert "| hybrid | Q039 | `1037-14` | 16 | hit@20 |" in text
    assert "| hybrid | Q048 | `1036-18` | absent | absent |" in text
