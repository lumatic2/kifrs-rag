from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.external_source_body_ingestion_authorization_gate import (  # noqa: E402
    check_authorization_gate,
    load_authorization_record,
)


DEFAULT_TEMPLATE_PATH = (
    ROOT
    / "docs"
    / "reports"
    / "external-source-body-authorization-record.template.json"
)
REPORT_PATH = (
    ROOT
    / "docs"
    / "reports"
    / "2026-07-05-esars1-external-source-body-authorization-record-scaffold.md"
)


def build_authorization_template() -> dict[str, Any]:
    return {
        "authorized_by": "",
        "authorization_scope": "synthetic_dry_run_only",
        "risk_acknowledgement": True,
        "source_review_required": True,
        "public_repo_body_commit_allowed": False,
        "live_fetch_allowed": False,
        "chunking_allowed": False,
        "embedding_allowed": False,
        "operator_note": "Fill authorized_by and change scope/actions only after explicit user approval and source-specific review.",
    }


def build_scaffold_result(
    *,
    template_path: Path = DEFAULT_TEMPLATE_PATH,
    report_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    template = build_authorization_template()
    authorization = None
    load_error = None
    gate = None
    try:
        if template_path.exists():
            authorization = load_authorization_record(template_path)
            gate = check_authorization_gate(
                authorization=authorization,
                authorization_record_path=template_path,
            )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        load_error = str(exc)

    template_gate_expected = "defer"
    return {
        "ok": load_error is None and (gate is None or gate["decision"] == template_gate_expected),
        "errors": [] if load_error is None else [load_error],
        "template_path": _display_path(template_path),
        "template": template,
        "template_exists": template_path.exists(),
        "template_gate_decision": gate["decision"] if gate else None,
        "template_allowed_to_implement": gate["allowed_to_implement"] if gate else None,
        "template_blockers": gate["blockers"] if gate else [],
        "expected_template_decision": template_gate_expected,
        "boundary": [
            "This scaffold is not an authorization record.",
            "The generated template intentionally leaves authorized_by empty.",
            "Live fetch, chunking, embedding, indexing, and public body commits remain disabled.",
            "A real record must be source-specific and operator-approved before the authorization gate can proceed.",
        ],
        "report_path": _display_path(report_path),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or user-approved source-specific external body authorization record",
    }


def write_scaffold(
    *,
    template_path: Path = DEFAULT_TEMPLATE_PATH,
    report_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    template_path.parent.mkdir(parents=True, exist_ok=True)
    template_path.write_text(
        json.dumps(build_authorization_template(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    result = build_scaffold_result(template_path=template_path, report_path=report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(result), encoding="utf-8")
    return result


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# ESARS1 External Source Body Authorization Record Scaffold",
        "",
        "> Scope: create a non-authorizing JSON template for future source-specific body-ingestion approval.",
        "",
        "## 한 줄 결론",
        "",
        "The authorization record template exists, but it is intentionally not an approval. The authorization gate must still defer until a user-approved source-specific record fills `authorized_by` and passes all policy checks.",
        "",
        "## Scaffold Result",
        "",
        f"- ok: {result['ok']}",
        f"- template path: `{result['template_path']}`",
        f"- template exists: {result['template_exists']}",
        f"- template gate decision: {result['template_gate_decision']}",
        f"- template allowed to implement: {result['template_allowed_to_implement']}",
        f"- expected template decision: {result['expected_template_decision']}",
        "",
        "## Template Blockers",
        "",
    ]
    lines.extend(f"- {blocker}" for blocker in result["template_blockers"])
    lines.extend(
        [
            "",
            "## Boundary",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in result["boundary"])
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


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a non-authorizing external source body authorization template.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--template-path", type=Path, default=DEFAULT_TEMPLATE_PATH)
    args = parser.parse_args()

    result = write_scaffold(template_path=args.template_path) if args.write else build_scaffold_result(template_path=args.template_path)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"template_path: {result['template_path']}")
        print(f"template_exists: {result['template_exists']}")
        print(f"template_gate_decision: {result['template_gate_decision']}")
        print(f"template_allowed_to_implement: {result['template_allowed_to_implement']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
