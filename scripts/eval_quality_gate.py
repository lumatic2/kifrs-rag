from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.eval.gates import GateThresholds, evaluate_report_gate
from kifrs.eval.harness import load_goldset, run_eval


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local eval and enforce score thresholds.")
    parser.add_argument("--runner", default="local-rag")
    parser.add_argument("--only", nargs="+", default=["Q019", "Q020", "Q021"])
    parser.add_argument("--min-composite", type=float, default=0.6)
    parser.add_argument("--min-cite", type=float, default=0.45)
    parser.add_argument("--min-global-rules", type=float, default=0.95)
    parser.add_argument("--format", choices=["json", "text"], default="json")
    args = parser.parse_args()

    wanted = set(args.only)
    items = [item for item in load_goldset() if item.id in wanted]
    missing = sorted(wanted - {item.id for item in items})
    if missing:
        raise SystemExit(f"missing goldset ids: {missing}")

    report = run_eval(args.runner, items, verbose=False)
    result = evaluate_report_gate(
        report,
        GateThresholds(
            min_composite=args.min_composite,
            min_cite=args.min_cite,
            min_global_rules=args.min_global_rules,
        ),
    )
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"ok: {result['ok']}")
        print(f"mean_composite: {result['mean_composite']}")
        print(f"mean_cite: {result['mean_cite']}")
        print(f"mean_global_rules: {result['mean_global_rules']}")
        print(f"failing_items: {len(result['failing_items'])}")
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
