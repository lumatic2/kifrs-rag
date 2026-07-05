from __future__ import annotations

import argparse
import inspect
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs import mcp_server  # noqa: E402
from kifrs.eval.retrieval import RETRIEVERS  # noqa: E402
from scripts.rag_quality_final_gate import TARGET_RETRIEVER  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-default-retriever-guard.md"
DEFAULT_PROMOTION_REPORT = ROOT / "docs" / "reports" / "2026-07-05-orpd1-opt-in-retriever-promotion-decision-gate.md"
EXPECTED_DEFAULT_MODE = "hybrid"


def check_default_retriever_guard(*, promotion_report: Path = DEFAULT_PROMOTION_REPORT) -> dict[str, Any]:
    errors: list[str] = []
    signature = inspect.signature(mcp_server.search)
    mode_default = signature.parameters["mode"].default
    search_modes = list(mcp_server._SEARCH_MODES)
    promotion = load_cached_promotion_decision(promotion_report)

    if mode_default != EXPECTED_DEFAULT_MODE:
        errors.append(f"mcp search default mode must remain {EXPECTED_DEFAULT_MODE}, got {mode_default}")
    if TARGET_RETRIEVER not in RETRIEVERS:
        errors.append(f"{TARGET_RETRIEVER} must remain available as an opt-in eval retriever")
    if TARGET_RETRIEVER in search_modes:
        errors.append(f"{TARGET_RETRIEVER} must not be exposed as an MCP search mode before promotion")
    if promotion["errors"]:
        errors.extend(f"promotion_report: {error}" for error in promotion["errors"])
    if promotion["promote_to_default"] is True:
        errors.append("promotion gate says promote; default retriever implementation must be reviewed separately")

    return {
        "ok": not errors,
        "errors": errors,
        "title": "Default Retriever Guard",
        "default_mode": mode_default,
        "expected_default_mode": EXPECTED_DEFAULT_MODE,
        "mcp_search_modes": search_modes,
        "target_retriever": TARGET_RETRIEVER,
        "target_retriever_opt_in_available": TARGET_RETRIEVER in RETRIEVERS,
        "target_retriever_exposed_in_mcp": TARGET_RETRIEVER in search_modes,
        "promotion_report": _display_path(promotion_report),
        "promotion_decision": promotion["decision"],
        "promote_to_default": promotion["promote_to_default"],
        "report_path": _display_path(REPORT_PATH),
        "next_leaf": promotion["next_leaf"],
    }


def load_cached_promotion_decision(path: Path = DEFAULT_PROMOTION_REPORT) -> dict[str, Any]:
    if not path.exists():
        return {
            "decision": "unknown",
            "promote_to_default": False,
            "next_leaf": "run opt-in retriever promotion decision gate",
            "errors": [f"missing promotion report: {_display_path(path)}"],
        }
    text = path.read_text(encoding="utf-8")
    match = re.search(r"## Machine Result\s+```json\s+(\{.*?\})\s+```", text, re.DOTALL)
    if not match:
        return {
            "decision": "unknown",
            "promote_to_default": False,
            "next_leaf": "rerun opt-in retriever promotion decision gate",
            "errors": [f"promotion report has no parseable Machine Result: {_display_path(path)}"],
        }
    try:
        payload = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        return {
            "decision": "unknown",
            "promote_to_default": False,
            "next_leaf": "rerun opt-in retriever promotion decision gate",
            "errors": [f"promotion report Machine Result JSON is invalid: {exc}"],
        }
    decision = payload.get("decision", {})
    return {
        "decision": decision.get("decision", "unknown"),
        "promote_to_default": decision.get("promote_to_default") is True,
        "next_leaf": payload.get("next_leaf", "unknown"),
        "errors": [],
    }


def render_markdown(result: dict[str, Any]) -> str:
    conclusion = (
        "The runtime default remains `hybrid`; the repair retriever is still opt-in only."
        if result["ok"]
        else "Default retriever guard failed; fix the listed errors before changing search defaults."
    )
    lines = [
        "# Default Retriever Guard",
        "",
        "> Scope: code-level invariant that prevents accidental default promotion of the opt-in repair retriever.",
        "",
        "## One-Line Result",
        "",
        conclusion,
        "",
        "## Runtime Boundary",
        "",
        f"- MCP search default mode: `{result['default_mode']}`",
        f"- Expected default mode: `{result['expected_default_mode']}`",
        f"- MCP search modes: `{', '.join(result['mcp_search_modes'])}`",
        f"- Opt-in target retriever: `{result['target_retriever']}`",
        f"- Target available in eval retrievers: {result['target_retriever_opt_in_available']}",
        f"- Target exposed in MCP modes: {result['target_retriever_exposed_in_mcp']}",
        f"- Promotion decision: {result['promotion_decision']}",
        f"- Promote to default: {result['promote_to_default']}",
        "",
        "## Boundary",
        "",
        "- This guard does not change runtime defaults.",
        "- The target repair stack remains an opt-in evaluation/demo path.",
        "- A future default change requires actual accountant evidence, explicit authorization, and a separate implementation.",
    ]
    if result["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in result["errors"])
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
    result = check_default_retriever_guard()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify that the default search retriever remains hybrid until promotion is approved.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    parser.add_argument("--promotion-report", type=Path, default=DEFAULT_PROMOTION_REPORT)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else check_default_retriever_guard(promotion_report=args.promotion_report)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"default_mode: {result['default_mode']}")
        print(f"target_retriever: {result['target_retriever']}")
        print(f"target_exposed_in_mcp: {result['target_retriever_exposed_in_mcp']}")
        print(f"promotion_decision: {result['promotion_decision']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
