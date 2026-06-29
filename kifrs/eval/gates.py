"""Quality gates for local evaluation reports."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .models import RunReport


@dataclass(frozen=True)
class GateThresholds:
    min_composite: float = 0.6
    min_cite: float = 0.45
    min_global_rules: float = 0.95


def evaluate_report_gate(report: RunReport, thresholds: GateThresholds) -> dict[str, Any]:
    cite_scores: list[float] = []
    global_scores: list[float] = []
    failing_items: list[dict[str, Any]] = []

    for item_report in report.items:
        score_by_name = {score.scorer: score.score for score in item_report.scores}
        cite_scores.append(score_by_name.get("cite", 0.0))
        global_scores.append(score_by_name.get("global_rules", 0.0))
        reasons = []
        if item_report.composite < thresholds.min_composite:
            reasons.append(f"composite<{thresholds.min_composite}")
        if score_by_name.get("cite", 0.0) < thresholds.min_cite:
            reasons.append(f"cite<{thresholds.min_cite}")
        if score_by_name.get("global_rules", 0.0) < thresholds.min_global_rules:
            reasons.append(f"global_rules<{thresholds.min_global_rules}")
        if reasons:
            failing_items.append({
                "id": item_report.item.id,
                "composite": round(item_report.composite, 3),
                "scores": {k: round(v, 3) for k, v in score_by_name.items()},
                "reasons": reasons,
            })

    mean_cite = sum(cite_scores) / len(cite_scores) if cite_scores else 0.0
    mean_global = sum(global_scores) / len(global_scores) if global_scores else 0.0
    ok = (
        report.mean_composite >= thresholds.min_composite
        and mean_cite >= thresholds.min_cite
        and mean_global >= thresholds.min_global_rules
        and not failing_items
    )
    return {
        "ok": ok,
        "runner": report.runner,
        "items": len(report.items),
        "mean_composite": round(report.mean_composite, 3),
        "mean_cite": round(mean_cite, 3),
        "mean_global_rules": round(mean_global, 3),
        "thresholds": {
            "min_composite": thresholds.min_composite,
            "min_cite": thresholds.min_cite,
            "min_global_rules": thresholds.min_global_rules,
        },
        "failing_items": failing_items,
    }
