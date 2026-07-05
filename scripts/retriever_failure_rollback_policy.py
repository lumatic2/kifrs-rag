from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.retriever_regression_latency_gate import build_retriever_regression_latency_gate  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-rpg3-failure-rollback-policy.md"


def build_retriever_failure_rollback_policy() -> dict[str, Any]:
    regression_gate = build_retriever_regression_latency_gate()
    policy = {
        "current_default": regression_gate["current_default"],
        "target_retriever": regression_gate["target_retriever"],
        "safe_fallback": "hybrid",
        "states": [
            {
                "state": "defer",
                "trigger": "missing latency/cost, rollback, authorization, or broad runtime evidence",
                "action": "keep current default and continue opt-in evaluation",
            },
            {
                "state": "block",
                "trigger": "recall/citation regression, default guard failure, or missing critical reports",
                "action": "do not expose target retriever as runtime default",
            },
            {
                "state": "rollback",
                "trigger": "post-promotion runtime regression or operator-reported failure",
                "action": "restore hybrid as default and rerun guard/report gates",
            },
        ],
        "operator_remediation": [
            "run default retriever guard",
            "run regression/latency gate",
            "restore current default mode to hybrid if any promotion check fails",
            "record defer/block reason in promotion command output",
        ],
        "forbidden_actions": [
            "manual runtime default edit without close gate",
            "exposing target retriever in MCP modes before promotion",
            "treating recall@20 success as sufficient for promotion",
        ],
    }
    checks = {
        "regression_gate_ok": regression_gate["ok"],
        "safe_fallback_is_current_default": policy["safe_fallback"] == regression_gate["current_default"],
        "defer_state_present": any(item["state"] == "defer" for item in policy["states"]),
        "block_state_present": any(item["state"] == "block" for item in policy["states"]),
        "rollback_state_present": any(item["state"] == "rollback" for item in policy["states"]),
        "operator_remediation_present": bool(policy["operator_remediation"]),
        "forbidden_manual_promotion_present": any(
            "manual runtime default edit" in item for item in policy["forbidden_actions"]
        ),
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "RPG3 Failure And Rollback Policy",
        "ok": not errors,
        "horizon": "runtime-retriever-promotion-gate",
        "completed_milestone": "RPG3",
        "promotion_gate_result": regression_gate["promotion_gate_result"],
        "policy": policy,
        "checks": checks,
        "errors": errors,
        "next_gate": "operator_promotion_command",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    policy = result["policy"]
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: RPG3 rollback policy for runtime retriever promotion decisions.",
        "",
        "## 한 줄 결론",
        "",
        "Promotion remains reversible: if evidence is missing or runtime checks fail, the operator keeps current default or must restore `hybrid` as the default.",
        "",
        "## Policy",
        "",
        f"- current default: `{policy['current_default']}`",
        f"- target retriever: `{policy['target_retriever']}`",
        f"- safe fallback: `{policy['safe_fallback']}`",
        f"- promotion gate result carried from RPG2: `{result['promotion_gate_result']}`",
        f"- next gate: `{result['next_gate']}`",
        "",
        "## States",
        "",
        "| State | Trigger | Action |",
        "|---|---|---|",
    ]
    for item in policy["states"]:
        lines.append(f"| {item['state']} | {item['trigger']} | {item['action']} |")
    lines.extend(["", "## Operator Remediation", ""])
    lines.extend(f"- {item}" for item in policy["operator_remediation"])
    lines.extend(["", "## Forbidden Actions", ""])
    lines.extend(f"- {item}" for item in policy["forbidden_actions"])
    lines.extend(["", "## Checks", "", "| Check | OK |", "|---|---|"])
    for name, ok in result["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in result["errors"]) if result["errors"] else lines.append("- none")
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(result, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    result = build_retriever_failure_rollback_policy()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build RPG3 failure and rollback policy.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_retriever_failure_rollback_policy()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- safe fallback: {result['policy']['safe_fallback']}")
        print(f"- next gate: {result['next_gate']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
