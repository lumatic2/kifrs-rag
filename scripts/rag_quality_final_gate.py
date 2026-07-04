from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from kifrs.eval.retrieval import _load_goldset, evaluate, must_cite_rank_summary
except ModuleNotFoundError:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from kifrs.eval.retrieval import _load_goldset, evaluate, must_cite_rank_summary


DEFAULT_GOLDSET = Path("data/eval/goldset.json")
BASELINE_RETRIEVER = "hybrid"
TARGET_RETRIEVER = "ifrs1109_classification_hybrid"
DEFAULT_K = 20


def build_report(*, goldset: Path = DEFAULT_GOLDSET, k: int = DEFAULT_K) -> dict[str, Any]:
    items = _load_goldset(goldset)
    report = evaluate(items, [BASELINE_RETRIEVER, TARGET_RETRIEVER], k)
    target = report["retrievers"][TARGET_RETRIEVER]
    baseline = report["retrievers"][BASELINE_RETRIEVER]
    target_misses = [
        {"id": row["id"], "miss": row["miss"]}
        for row in target["per_item"]
        if row["miss"]
    ]
    buckets = must_cite_rank_summary(report)
    failures: list[str] = []
    if target["aggregate"]["recall@20"] < 1.0:
        failures.append(f"{TARGET_RETRIEVER} recall@20 is {target['aggregate']['recall@20']:.3f}, expected 1.000")
    if buckets[TARGET_RETRIEVER]["absent"] != 0:
        failures.append(f"{TARGET_RETRIEVER} absent citations: {buckets[TARGET_RETRIEVER]['absent']}")
    if target_misses:
        failures.append(f"{TARGET_RETRIEVER} still has top-{k} misses: {target_misses}")
    return {
        "ok": not failures,
        "k": k,
        "n_items": report["n_items"],
        "baseline_recall20": baseline["aggregate"]["recall@20"],
        "target_recall20": target["aggregate"]["recall@20"],
        "baseline_buckets": buckets[BASELINE_RETRIEVER],
        "target_buckets": buckets[TARGET_RETRIEVER],
        "target_misses": target_misses,
        "failures": failures,
    }


def render_text(payload: dict[str, Any]) -> str:
    lines = [
        f"ok: {payload['ok']}",
        f"items: {payload['n_items']}",
        f"k: {payload['k']}",
        f"baseline_recall@20: {payload['baseline_recall20']:.3f}",
        f"target_recall@20: {payload['target_recall20']:.3f}",
        f"baseline_buckets: {payload['baseline_buckets']}",
        f"target_buckets: {payload['target_buckets']}",
        f"target_misses: {payload['target_misses']}",
    ]
    if payload["failures"]:
        lines.append("failures:")
        lines.extend(f"  - {failure}" for failure in payload["failures"])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Final RAG quality gate for opt-in repair retriever.")
    parser.add_argument("--goldset", type=Path, default=DEFAULT_GOLDSET)
    parser.add_argument("--k", type=int, default=DEFAULT_K)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    payload = build_report(goldset=args.goldset, k=args.k)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(payload))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
