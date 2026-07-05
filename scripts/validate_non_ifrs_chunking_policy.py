from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.ingestion.source_record import ALLOWED_SOURCE_RECORD_TYPES  # noqa: E402


DEFAULT_POLICY_PATH = ROOT / "docs" / "ingestion" / "non_ifrs_chunking_policy.json"
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-nis4-chunking-embedding-policy.md"

REQUIRED_LANE_FIELDS = {
    "record_type",
    "chunk_strategy",
    "index_strategy",
    "vector_scope",
    "runtime_lookup",
    "citation_role",
    "body_storage_policy",
    "notes",
}


def validate_policy(path: Path = DEFAULT_POLICY_PATH) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []

    policy = raw.get("policy", {})
    if policy.get("protected_material_committed") is not False:
        errors.append("policy.protected_material_committed must be false")
    if policy.get("default_runtime_retriever_unchanged") is not True:
        errors.append("policy.default_runtime_retriever_unchanged must be true")

    lanes = raw.get("lanes", {})
    if set(lanes) != set(ALLOWED_SOURCE_RECORD_TYPES):
        errors.append(f"lanes must cover source record types: {sorted(ALLOWED_SOURCE_RECORD_TYPES)}")

    for lane_name, lane in lanes.items():
        prefix = f"lanes.{lane_name}"
        missing = sorted(REQUIRED_LANE_FIELDS - set(lane))
        errors.extend(f"{prefix}: missing {field}" for field in missing)
        if lane.get("record_type") != lane_name:
            errors.append(f"{prefix}: record_type must match lane name")
        if not isinstance(lane.get("notes"), list) or not lane.get("notes"):
            errors.append(f"{prefix}: notes must be non-empty list")
        if lane_name in {"law_locator", "structured_fact"} and lane.get("vector_scope") != "none_for_public_fixture":
            errors.append(f"{prefix}: public fixture vector_scope must be none_for_public_fixture")
        if lane_name == "client_private_fact" and not str(lane.get("vector_scope", "")).startswith("local_only"):
            errors.append(f"{prefix}: client private vector_scope must stay local_only")

    return {
        "ok": not errors,
        "title": "NIS4 Chunking and Embedding Policy",
        "milestone": "NIS4",
        "policy_path": _display_path(path),
        "total_lanes": len(lanes),
        "lanes": {
            name: {
                "chunk_strategy": lane.get("chunk_strategy"),
                "index_strategy": lane.get("index_strategy"),
                "vector_scope": lane.get("vector_scope"),
                "runtime_lookup": lane.get("runtime_lookup"),
            }
            for name, lane in lanes.items()
        },
        "next_leaf": "NIS5_dataization_gate_and_runtime_handoff",
        "errors": errors,
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# NIS4 Chunking and Embedding Policy",
        "",
        "> Scope: source-lane chunking, indexing, and vector policy for non-IFRS dataization.",
        "",
        "## One-Line Conclusion",
        "",
        "Each non-IFRS source lane now has an explicit chunk/index/vector policy that keeps protected material out of the public repo.",
        "",
        "## Policy",
        "",
        f"- Policy path: `{result['policy_path']}`",
        f"- Total lanes: {result['total_lanes']}",
        "",
        "| Lane | Chunk | Index | Vector Scope | Runtime Lookup |",
        "|---|---|---|---|---|",
    ]
    for lane, item in result["lanes"].items():
        lines.append(
            f"| `{lane}` | `{item['chunk_strategy']}` | `{item['index_strategy']}` | `{item['vector_scope']}` | `{item['runtime_lookup']}` |"
        )
    if result["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in result["errors"])
    lines.extend(
        [
            "",
            "## Next Leaf",
            "",
            result["next_leaf"],
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(result, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH, policy_path: Path = DEFAULT_POLICY_PATH) -> dict[str, Any]:
    result = validate_policy(policy_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate non-IFRS chunking and embedding policy.")
    parser.add_argument("policy_path", nargs="?", type=Path, default=DEFAULT_POLICY_PATH)
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out, args.policy_path) if args.write else validate_policy(args.policy_path)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- policy_path: {result['policy_path']}")
        print(f"- total_lanes: {result['total_lanes']}")
        print(f"- next_leaf: {result['next_leaf']}")
        print(f"- report_path: {result['report_path']}")
        for error in result["errors"]:
            print(f"- {error}")
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
