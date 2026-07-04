import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "rag_quality_final_gate", ROOT / "scripts" / "rag_quality_final_gate.py"
)
rag_quality_final_gate = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(rag_quality_final_gate)


def test_render_text_includes_gate_summary():
    text = rag_quality_final_gate.render_text(
        {
            "ok": True,
            "n_items": 50,
            "k": 20,
            "baseline_recall20": 0.887,
            "target_recall20": 1.0,
            "baseline_buckets": {"hit@5": 45, "hit@10": 14, "hit@20": 14, "beyond@20": 0, "absent": 9},
            "target_buckets": {"hit@5": 47, "hit@10": 18, "hit@20": 17, "beyond@20": 0, "absent": 0},
            "target_misses": [],
            "failures": [],
        }
    )

    assert "ok: True" in text
    assert "target_recall@20: 1.000" in text
    assert "target_misses: []" in text


def test_build_report_shape_from_fake_evaluate(monkeypatch):
    class Item:
        pass

    monkeypatch.setattr(rag_quality_final_gate, "_load_goldset", lambda goldset: [Item()])
    monkeypatch.setattr(
        rag_quality_final_gate,
        "evaluate",
        lambda items, retrievers, k: {
            "n_items": 1,
            "retrievers": {
                "hybrid": {
                    "aggregate": {"recall@20": 0.0},
                    "per_item": [{"id": "QX", "miss": [("S", "1")], "gold_ranks": {"S-1": None}}],
                },
                "ifrs1109_classification_hybrid": {
                    "aggregate": {"recall@20": 1.0},
                    "per_item": [{"id": "QX", "miss": [], "gold_ranks": {"S-1": 3}}],
                },
            },
        },
    )

    payload = rag_quality_final_gate.build_report()

    assert payload["ok"] is True
    assert payload["target_recall20"] == 1.0
    assert payload["target_misses"] == []
