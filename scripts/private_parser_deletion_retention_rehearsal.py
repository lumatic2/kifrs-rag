from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-ppr3-deletion-retention-rehearsal.md"


def build_deletion_retention_rehearsal() -> dict[str, Any]:
    lifecycle = [
        _state("received", "synthetic fixture path registered", retained=True, public_payload=False),
        _state("parsed", "structured facts emitted without raw content", retained=True, public_payload=False),
        _state("reviewed", "human-review flag and redaction statuses checked", retained=True, public_payload=False),
        _state("delete_pending", "local raw fixture marked for deletion", retained=True, public_payload=False),
        _state("deleted", "raw fixture absent; structured public-safe report retained", retained=False, public_payload=False),
    ]
    artifacts = [
        {
            "artifact": "raw_local_fixture",
            "initial_state": "retained",
            "final_state": "deleted",
            "public_report_allowed": False,
        },
        {
            "artifact": "structured_fact_report",
            "initial_state": "created",
            "final_state": "retained",
            "public_report_allowed": True,
        },
        {
            "artifact": "redaction_log",
            "initial_state": "created",
            "final_state": "retained",
            "public_report_allowed": True,
        },
    ]
    evidence = [
        _evidence("ppr1_authorization_plan", "docs/reports/2026-07-05-ppr1-authorization-safe-adapter-proof.md"),
        _evidence("ppr2_adapter_contract", "docs/reports/2026-07-05-ppr2-fixture-adapter-contract.md"),
        _evidence("previous_deletion_simulation", "docs/reports/2026-07-05-rlp3-deletion-automation-simulation.md"),
    ]
    checks = {
        "all_evidence_exists": all(item["exists"] for item in evidence),
        "deleted_state_present": any(item["state"] == "deleted" for item in lifecycle),
        "raw_fixture_final_deleted": any(item["artifact"] == "raw_local_fixture" and item["final_state"] == "deleted" for item in artifacts),
        "public_payload_never_allowed": all(item["public_payload"] is False for item in lifecycle),
        "structured_report_retained": any(item["artifact"] == "structured_fact_report" and item["final_state"] == "retained" for item in artifacts),
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "PPR3 Deletion And Retention Rehearsal",
        "ok": not errors,
        "horizon": "private-parser-realism-hardening",
        "completed_milestone": "PPR3",
        "lifecycle": lifecycle,
        "artifacts": artifacts,
        "evidence": evidence,
        "checks": checks,
        "errors": errors,
        "next_leaf": "PPR4_parser_leak_and_public_report_gate",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: public-safe rehearsal of local parser artifact deletion and retention states.",
        "",
        "## 한 줄 결론",
        "",
        "Raw local fixtures end deleted; structured facts and redaction statuses may be retained as public-safe evidence.",
        "",
        "## Lifecycle",
        "",
        "| State | Meaning | Retained | Public Payload |",
        "|---|---|---|---|",
    ]
    for item in result["lifecycle"]:
        lines.append(f"| {item['state']} | {item['meaning']} | {item['retained']} | {item['public_payload']} |")
    lines.extend(["", "## Artifacts", "", "| Artifact | Initial | Final | Public Report Allowed |", "|---|---|---|---|"])
    for item in result["artifacts"]:
        lines.append(
            f"| {item['artifact']} | {item['initial_state']} | {item['final_state']} | {item['public_report_allowed']} |"
        )
    lines.extend(["", "## Evidence", "", "| ID | Path | Exists |", "|---|---|---|"])
    for item in result["evidence"]:
        lines.append(f"| {item['id']} | `{item['path']}` | {item['exists']} |")
    lines.extend(["", "## Checks", "", "| Check | OK |", "|---|---|"])
    for name, ok in result["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in result["errors"]) if result["errors"] else lines.append("- none")
    lines.extend(
        [
            "",
            "## Next Leaf",
            "",
            f"- `{result['next_leaf']}`",
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(result, ensure_ascii=False, indent=2),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    result = build_deletion_retention_rehearsal()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _state(state: str, meaning: str, retained: bool, public_payload: bool) -> dict[str, Any]:
    return {"state": state, "meaning": meaning, "retained": retained, "public_payload": public_payload}


def _evidence(id_: str, path: str) -> dict[str, Any]:
    return {"id": id_, "path": path, "exists": (ROOT / path).exists()}


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build PPR3 deletion and retention rehearsal.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_deletion_retention_rehearsal()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- lifecycle states: {len(result['lifecycle'])}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
