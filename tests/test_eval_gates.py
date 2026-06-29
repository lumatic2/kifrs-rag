from kifrs.eval.gates import GateThresholds, evaluate_report_gate
from kifrs.eval.models import Citation, GoldItem, ItemReport, RunReport, RunResult, ScoreResult


def _item_report(composite_scores):
    item = GoldItem(
        id="T",
        source="test",
        source_ref="",
        question="",
        must_cite=[Citation("1115", "27")],
    )
    run = RunResult(item_id="T", runner="test", question="", answer="")
    scores = [ScoreResult(name, value) for name, value in composite_scores.items()]
    return ItemReport(item=item, run=run, scores=scores)


def test_evaluate_report_gate_passes_thresholds():
    report = RunReport(runner="test", timestamp="", items=[
        _item_report({"cite": 0.8, "keyword": 0.7, "global_rules": 1.0}),
    ])
    result = evaluate_report_gate(report, GateThresholds(min_composite=0.6, min_cite=0.5))
    assert result["ok"]
    assert result["failing_items"] == []


def test_evaluate_report_gate_reports_failing_items():
    report = RunReport(runner="test", timestamp="", items=[
        _item_report({"cite": 0.2, "keyword": 0.5, "global_rules": 1.0}),
    ])
    result = evaluate_report_gate(report, GateThresholds(min_composite=0.6, min_cite=0.5))
    assert not result["ok"]
    assert result["failing_items"][0]["id"] == "T"
