import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "ifrs1109_classification_gate", ROOT / "scripts" / "ifrs1109_classification_gate.py"
)
ifrs1109_classification_gate = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(ifrs1109_classification_gate)


def _report(*, classification_still_misses=False, preserved_regresses=False):
    per_baseline = []
    per_target = []
    for item_id in ifrs1109_classification_gate.PRESERVED_ITEMS:
        per_baseline.append({"id": item_id, "miss": []})
        per_target.append({"id": item_id, "miss": [("P", item_id)] if preserved_regresses else []})
    for item_id in ifrs1109_classification_gate.RECOVERED_CLASSIFICATION_ITEMS:
        per_baseline.append({"id": item_id, "miss": [("1109", "4.1.4")]})
        per_target.append({"id": item_id, "miss": [("1109", "4.1.4")] if classification_still_misses else []})
    return {
        "k": 20,
        "retrievers": {
            "ifrs1109_scope_hybrid": {
                "aggregate": {"recall@20": 0.9},
                "per_item": per_baseline,
            },
            "ifrs1109_classification_hybrid": {
                "aggregate": {"recall@20": 1.0},
                "per_item": per_target,
            },
        },
    }


def test_evaluate_gate_passes_when_classification_recovers_and_boundaries_hold():
    payload = ifrs1109_classification_gate.evaluate_gate(_report())

    assert payload["ok"] is True
    assert payload["failures"] == []


def test_evaluate_gate_fails_when_classification_item_still_misses():
    payload = ifrs1109_classification_gate.evaluate_gate(_report(classification_still_misses=True))

    assert payload["ok"] is False
    assert any("1109 classification subquery did not recover" in failure for failure in payload["failures"])


def test_evaluate_gate_fails_when_preserved_item_regresses():
    payload = ifrs1109_classification_gate.evaluate_gate(_report(preserved_regresses=True))

    assert payload["ok"] is False
    assert any("preserved item regressed" in failure for failure in payload["failures"])
