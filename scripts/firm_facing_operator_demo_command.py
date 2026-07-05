from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.runtime.authority_boundary import AUTHORITY_ROLES, build_runtime_authority_boundary  # noqa: E402
from kifrs.workflows.kifrs1116.fixtures import FIXTURES  # noqa: E402
from kifrs.workflows.kifrs1116.review_pack import (  # noqa: E402
    generate_review_pack,
    render_review_pack_markdown,
)


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-fps2-operator-demo-command.md"
PRIVATE_RUNTIME_CLOSE_REPORT = ROOT / "docs" / "reports" / "2026-07-05-client-private-parser-runtime-close-report.md"
MULTI_AUTHORITY_CLOSE_REPORT = ROOT / "docs" / "reports" / "2026-07-05-multi-authority-runtime-hardening-close-report.md"
RAG_QUALITY_CLOSE_REPORT = ROOT / "docs" / "reports" / "2026-07-05-rag-quality-refresh-close-report.md"
DEFAULT_RETRIEVER_GUARD_REPORT = ROOT / "docs" / "reports" / "2026-07-05-default-retriever-guard.md"


def build_demo_packet() -> dict[str, Any]:
    boundary = build_runtime_authority_boundary(primary_citations=["[1116-53]", "[1116-59]"])
    fixture = next(item for item in FIXTURES if item.txn.label == "scenario_01_simple_office_lease")
    pack = generate_review_pack(fixture.txn, authority_boundary=boundary)
    rendered_pack = render_review_pack_markdown(pack)
    authority_counts = {role: len(pack.authority_boundary.get(role, [])) for role in AUTHORITY_ROLES}
    verification = _build_verification_status()
    private_runtime = _build_private_runtime_boundary()

    packet = {
        "title": "FPS2 Operator Demo Command",
        "ok": True,
        "horizon": "firm-facing-product-surface",
        "milestone": "FPS2",
        "demo_flow": {
            "id": "lease-review-pack-authority-private-boundary",
            "label": "1116 lease review pack with authority and private-runtime boundary",
            "operator_command": "python scripts\\firm_facing_operator_demo_command.py --format markdown --write",
        },
        "workflow_result": {
            "standard": pack.standard,
            "case_id": pack.case_id,
            "status": pack.status,
            "journal_entry_present": pack.journal_entry is not None,
            "review_memo_present": pack.review_memo is not None,
            "disclosure_draft_present": pack.disclosure_draft is not None,
            "review_checklist_count": len(pack.review_checklist),
            "human_review_action_count": len(pack.needs_human_review),
            "citations": pack.citations,
        },
        "authority_boundary": {
            "roles": list(AUTHORITY_ROLES),
            "role_counts": authority_counts,
            "all_roles_present": all(authority_counts[role] >= 1 for role in AUTHORITY_ROLES),
        },
        "private_runtime_boundary": {
            "ok": private_runtime["ok"],
            "public_safe": private_runtime["public_safe"],
            "runtime_path": private_runtime["runtime_path"],
            "checks": private_runtime["checks"],
            "gate_report": private_runtime["report_path"],
        },
        "verification_status": verification,
        "public_safe": _public_safe(rendered_pack),
        "review_pack_markdown": rendered_pack,
        "report_path": _display_path(REPORT_PATH),
        "next_leaf": "FPS3_readiness_checklist_and_local_install_path",
    }
    packet["ok"] = (
        packet["workflow_result"]["status"] == "automated"
        and packet["authority_boundary"]["all_roles_present"]
        and packet["private_runtime_boundary"]["ok"]
        and all(packet["verification_status"].values())
        and packet["public_safe"]
    )
    return packet


def render_markdown(packet: dict[str, Any]) -> str:
    lines = [
        f"# {packet['title']}",
        "",
        "> Scope: FPS2 one-command public-safe walkthrough packet for a firm-side operator.",
        "",
        "## One-Line Result",
        "",
        (
            "The operator demo command produces a 1116 lease review-pack walkthrough with authority and private-runtime boundaries."
            if packet["ok"]
            else "The operator demo packet is not ready; fix failed checks before using it."
        ),
        "",
        "## Demo Flow",
        "",
        f"- id: `{packet['demo_flow']['id']}`",
        f"- label: {packet['demo_flow']['label']}",
        f"- command: `{packet['demo_flow']['operator_command']}`",
        "",
        "## Workflow Result",
        "",
        f"- standard: {packet['workflow_result']['standard']}",
        f"- case: `{packet['workflow_result']['case_id']}`",
        f"- status: {packet['workflow_result']['status']}",
        f"- journal entry: {packet['workflow_result']['journal_entry_present']}",
        f"- review memo: {packet['workflow_result']['review_memo_present']}",
        f"- disclosure draft: {packet['workflow_result']['disclosure_draft_present']}",
        f"- checklist items: {packet['workflow_result']['review_checklist_count']}",
        f"- human review actions: {packet['workflow_result']['human_review_action_count']}",
        "",
        "## Authority Boundary",
        "",
        f"- all roles present: {packet['authority_boundary']['all_roles_present']}",
        "",
        "| Role | Count |",
        "|---|---:|",
    ]
    for role, count in packet["authority_boundary"]["role_counts"].items():
        lines.append(f"| {role} | {count} |")
    lines.extend(
        [
            "",
            "## Client-Private Runtime Boundary",
            "",
            f"- ok: {packet['private_runtime_boundary']['ok']}",
            f"- public safe: {packet['private_runtime_boundary']['public_safe']}",
            f"- gate report: `{packet['private_runtime_boundary']['gate_report']}`",
            "",
        ]
    )
    lines.extend(f"- {step}" for step in packet["private_runtime_boundary"]["runtime_path"])
    lines.extend(
        [
            "",
            "## Verification Status",
            "",
            "| Check | OK |",
            "|---|---|",
        ]
    )
    for name, ok in packet["verification_status"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(
        [
            "",
            "## Review Pack Walkthrough",
            "",
            packet["review_pack_markdown"],
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps({key: value for key, value in packet.items() if key != "review_pack_markdown"}, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    packet = build_demo_packet()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(packet), encoding="utf-8")
    return packet


def _build_verification_status() -> dict[str, bool]:
    return {
        "multi_authority_runtime_close_report": _report_contains(MULTI_AUTHORITY_CLOSE_REPORT, "close status: closed"),
        "client_private_parser_runtime_close_report": _report_contains(PRIVATE_RUNTIME_CLOSE_REPORT, "close status: closed"),
        "rag_quality_refresh_close_report": RAG_QUALITY_CLOSE_REPORT.exists(),
        "default_retriever_guard_report": _report_contains(DEFAULT_RETRIEVER_GUARD_REPORT, "The runtime default remains `hybrid`"),
    }


def _build_private_runtime_boundary() -> dict[str, Any]:
    return {
        "ok": _report_contains(PRIVATE_RUNTIME_CLOSE_REPORT, "close status: closed"),
        "public_safe": _report_contains(PRIVATE_RUNTIME_CLOSE_REPORT, "no public private-source payload"),
        "runtime_path": [
            "synthetic parser-shaped structured facts",
            "runtime parser contract",
            "client_private_fact authority reference",
            "review-pack client-private authority panel",
            "runtime deletion gate",
        ],
        "checks": {
            "structured_facts_only": True,
            "client_private_fact_reference_only": True,
            "deletion_gated_close": True,
            "no_public_private_source_payload": _report_contains(PRIVATE_RUNTIME_CLOSE_REPORT, "no public private-source payload"),
        },
        "report_path": _display_path(PRIVATE_RUNTIME_CLOSE_REPORT),
    }


def _report_contains(path: Path, text: str) -> bool:
    return path.exists() and text in path.read_text(encoding="utf-8")


def _public_safe(text: str) -> bool:
    lowered = text.lower()
    forbidden = ("api_key", "source_body", "full_text", "raw_xml", "xbrl_dump", "secret")
    return not any(item in lowered for item in forbidden)


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the firm-facing FPS2 operator demo packet.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    packet = write_report(args.out) if args.write else build_demo_packet()
    if args.format == "json":
        print(json.dumps(packet, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(packet), end="")
    else:
        print(packet["title"])
        print(f"- ok: {packet['ok']}")
        print(f"- flow: {packet['demo_flow']['id']}")
        print(f"- case: {packet['workflow_result']['case_id']}")
        print(f"- all authority roles present: {packet['authority_boundary']['all_roles_present']}")
        print(f"- private runtime ok: {packet['private_runtime_boundary']['ok']}")
        print(f"- next leaf: {packet['next_leaf']}")
    return 0 if packet["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
