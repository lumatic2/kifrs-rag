from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.external_source_connector_lane_close_gate import check_external_connector_lane_close_gate  # noqa: E402


NOTE_PATH = ROOT / "docs" / "reports" / "2026-07-05-espdn1-external-source-connector-post-close-demo-packet-note.md"
LANE_CLOSE_REPORT = "2026-07-05-eslsc1-external-source-connector-lane-close-gate.md"
LANE_SUMMARY_REPORT = "2026-07-05-esls1-external-source-connector-lane-summary.md"
ENTRYPOINTS = {
    "demo_index": ROOT / "docs" / "reports" / "demo-poc" / "index.md",
    "demo_manifest": ROOT / "docs" / "reports" / "demo-poc" / "MANIFEST.md",
    "field_feedback_index": ROOT / "docs" / "reports" / "field-feedback" / "INDEX.md",
    "real_accountant_session_packet": ROOT / "docs" / "reports" / "real-accountant-session" / "SESSION_PACKET.md",
}
REQUIRED_NOTE_PHRASES = [
    "metadata-only",
    "supporting interpretation",
    "K-IFRS paragraph DB remains the primary accounting evidence source",
    "does not fetch/cache/chunk/embed/index/answer from external source body text",
    LANE_CLOSE_REPORT,
    LANE_SUMMARY_REPORT,
]


def check_post_close_demo_packet_note() -> dict[str, Any]:
    close_gate = check_external_connector_lane_close_gate()
    errors: list[str] = []

    if close_gate["ok"] is not True:
        errors.extend(f"lane_close_gate: {error}" for error in close_gate["errors"])
    if close_gate["lane_summary"]["lane_status"] != "metadata_and_demo_bridge_closed":
        errors.append(f"lane_close_gate: unexpected lane status {close_gate['lane_summary']['lane_status']}")

    note_exists = NOTE_PATH.exists()
    note_text = NOTE_PATH.read_text(encoding="utf-8") if note_exists else ""
    if not note_exists:
        errors.append(f"note is missing: {_display_path(NOTE_PATH)}")
    for phrase in REQUIRED_NOTE_PHRASES:
        if phrase not in note_text:
            errors.append(f"note missing phrase: {phrase}")

    entrypoint_links = {}
    for name, path in ENTRYPOINTS.items():
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        linked = NOTE_PATH.name in text
        entrypoint_links[name] = {"path": _display_path(path), "linked": linked}
        if not path.exists():
            errors.append(f"entrypoint missing: {_display_path(path)}")
        elif not linked:
            errors.append(f"entrypoint does not link post-close note: {_display_path(path)}")

    for flag in (
        "body_text_stored",
        "body_cache_created",
        "chunks_created",
        "embeddings_created",
        "index_created",
        "answer_time_body_use_enabled",
    ):
        if close_gate["lane_summary"].get(flag) is not False:
            errors.append(f"lane_close_gate: {flag} must be false")

    return {
        "ok": not errors,
        "errors": errors,
        "note_id": "espdn1-external-source-connector-post-close-demo-packet-note",
        "note_path": _display_path(NOTE_PATH),
        "connector_id": close_gate["connector_id"],
        "lane_close_report": LANE_CLOSE_REPORT,
        "lane_summary_report": LANE_SUMMARY_REPORT,
        "entrypoint_links": entrypoint_links,
        "boundary": {
            "metadata_only": True,
            "supporting_interpretation_only": True,
            "primary_accounting_evidence": "K-IFRS paragraph DB",
            "external_text_pipeline_enabled": False,
        },
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or opt-in retriever promotion decision after actual accountant evidence",
    }


def render_note(result: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# ESPDN1 External Source Connector Post-Close Demo Packet Note",
            "",
            "> Scope: reviewer-facing note for the closed KASB/FSS external connector metadata-only lane.",
            "",
            "## 한 줄 결론",
            "",
            "`kasb-fss-interpretive-catalog` is ready to show in the demo packet as metadata-only supporting interpretation evidence. K-IFRS paragraph DB remains the primary accounting evidence source.",
            "",
            "## What This Means in the Demo",
            "",
            "- Use this note before showing the external connector evidence so the reviewer does not mistake it for source-body RAG.",
            "- The closed lane proves that KASB/FSS locator/status evidence can be surfaced in the demo path.",
            "- The external connector supports interpretation boundaries after the K-IFRS paragraph evidence is shown.",
            "- It does not fetch/cache/chunk/embed/index/answer from external source body text.",
            "",
            "## Evidence to Open",
            "",
            f"- `{LANE_CLOSE_REPORT}` — final close gate for the metadata-only connector lane.",
            f"- `{LANE_SUMMARY_REPORT}` — short lane summary from policy record to demo bridge.",
            "- `demo-poc/MANIFEST.md` — reviewer demo bundle entry point.",
            "- `real-accountant-session/SESSION_PACKET.md` — actual session open-file list.",
            "",
            "## Reviewer Wording",
            "",
            "이 외부자료 connector는 아직 KASB/FSS 본문을 가져와서 답변하는 RAG가 아닙니다. 지금 닫힌 범위는 공개 가능한 locator/status metadata를 demo evidence로 보여주는 것입니다. 회계 판단의 1차 근거는 여전히 K-IFRS 문단 DB이고, 외부자료는 보조 해석과 추가 확인 지점을 분리해서 보여주기 위한 레이어입니다.",
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(result, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    ) + "\n"


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# ESPDN1 External Source Connector Post-Close Demo Packet Note Gate",
        "",
        "> Scope: verify that the closed metadata-only connector lane has a reviewer-facing note in demo/session entry points.",
        "",
        "## Result",
        "",
        f"- ok: {result['ok']}",
        f"- note: `{result['note_path']}`",
        f"- connector: `{result['connector_id']}`",
        f"- lane close report: `{result['lane_close_report']}`",
        f"- lane summary report: `{result['lane_summary_report']}`",
        "",
        "## Entrypoint Links",
        "",
        "| Entrypoint | Path | Linked |",
        "|---|---|---:|",
    ]
    for name, link in result["entrypoint_links"].items():
        lines.append(f"| {name} | `{link['path']}` | {link['linked']} |")
    lines.extend([
        "",
        "## Boundary",
        "",
        f"- metadata-only: {result['boundary']['metadata_only']}",
        f"- supporting interpretation only: {result['boundary']['supporting_interpretation_only']}",
        f"- primary accounting evidence: {result['boundary']['primary_accounting_evidence']}",
        f"- source body fetch/cache/chunk/embed/index/answer: {result['boundary']['external_text_pipeline_enabled']}",
        "",
        "## Next Leaf",
        "",
        str(result["next_leaf"]),
        "",
        "## Machine Result",
        "",
        "```json",
        json.dumps(result, ensure_ascii=False, indent=2, default=str),
        "```",
    ])
    return "\n".join(lines) + "\n"


def write_note() -> dict[str, Any]:
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    provisional = {
        "ok": True,
        "errors": [],
        "note_id": "espdn1-external-source-connector-post-close-demo-packet-note",
        "note_path": _display_path(NOTE_PATH),
        "connector_id": "kasb-fss-interpretive-catalog",
        "lane_close_report": LANE_CLOSE_REPORT,
        "lane_summary_report": LANE_SUMMARY_REPORT,
        "entrypoint_links": {},
        "boundary": {
            "metadata_only": True,
            "supporting_interpretation_only": True,
            "primary_accounting_evidence": "K-IFRS paragraph DB",
            "external_text_pipeline_enabled": False,
        },
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or opt-in retriever promotion decision after actual accountant evidence",
    }
    NOTE_PATH.write_text(render_note(provisional), encoding="utf-8")
    result = check_post_close_demo_packet_note()
    NOTE_PATH.write_text(render_note(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify the external connector post-close demo packet note.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true", help=f"Write {NOTE_PATH.relative_to(ROOT)} before checking")
    args = parser.parse_args()

    result = write_note() if args.write else check_post_close_demo_packet_note()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"note_path: {result['note_path']}")
        print(f"connector_id: {result['connector_id']}")
        print(f"next_leaf: {result['next_leaf']}")
        for name, link in result["entrypoint_links"].items():
            print(f"- {name}: linked={link['linked']} path={link['path']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
