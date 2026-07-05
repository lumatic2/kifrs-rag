from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.external_source_body_ingestion_authorization_gate import check_authorization_gate  # noqa: E402
from scripts.external_source_synthetic_parser_chunker_dry_run import run_synthetic_parser_chunker_dry_run  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-essc1-external-source-synthetic-parser-chunker-close-gate.md"


def check_synthetic_parser_chunker_close_gate(*, run_quality_preflight: bool = False) -> dict[str, Any]:
    dry_run = run_synthetic_parser_chunker_dry_run()
    authorization = check_authorization_gate()
    quality = _run_quality_preflight() if run_quality_preflight else {"ran": False, "ok": None, "public_safe": None, "errors": []}

    errors: list[str] = []
    if dry_run["ok"] is not True:
        errors.extend(f"dry_run: {error}" for error in dry_run["errors"])
    if dry_run["live_fetch_performed"] is not False:
        errors.append("dry_run: live_fetch_performed must be false")
    if dry_run["body_text_stored"] is not False:
        errors.append("dry_run: body_text_stored must be false")
    if dry_run["embedding_created"] is not False:
        errors.append("dry_run: embedding_created must be false")
    if authorization["ok"] is not True:
        errors.extend(f"authorization_gate: {error}" for error in authorization["errors"])
    if authorization["allowed_to_implement"] is not False:
        errors.append("authorization_gate: live ingestion must remain disabled for synthetic close")
    if run_quality_preflight and quality["ok"] is not True:
        errors.extend(f"quality_preflight: {error}" for error in quality["errors"])
    if run_quality_preflight and quality["public_safe"] is not True:
        errors.append("quality_preflight: public_safe must be true")

    return {
        "ok": not errors,
        "errors": errors,
        "close_gate_id": "essc1-external-source-synthetic-parser-chunker-close-gate",
        "closed_scope": [
            "external source body policy/plan prerequisites",
            "external source body authorization gate",
            "synthetic parser/chunker metadata-only dry-run",
        ],
        "still_not_implemented": [
            "live external body fetching/crawling",
            "source body cache",
            "source-specific live chunking",
            "external body embeddings",
            "external body index namespace",
        ],
        "dry_run": {
            "ok": dry_run["ok"],
            "chunk_count": dry_run["chunk_count"],
            "live_fetch_performed": dry_run["live_fetch_performed"],
            "body_text_stored": dry_run["body_text_stored"],
            "embedding_created": dry_run["embedding_created"],
            "report_path": dry_run["report_path"],
        },
        "authorization_gate": {
            "ok": authorization["ok"],
            "decision": authorization["decision"],
            "allowed_to_implement": authorization["allowed_to_implement"],
            "authorization_present": authorization["authorization_present"],
            "report_path": authorization["report_path"],
        },
        "quality_preflight": quality,
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source connector-specific policy record",
    }


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# ESSC1 External Source Synthetic Parser/Chunker Close Gate",
        "",
        "> Scope: close gate for synthetic-only external source parser/chunker readiness.",
        "",
        "## 한 줄 결론",
        "",
        "The synthetic external-source parser/chunker lane is closed at the public-safe dry-run level. It proves metadata-only chunk records can be produced from author-written synthetic input, while live body ingestion, caching, chunking, embeddings, and indexing remain unimplemented.",
        "",
        "## Close Result",
        "",
        f"- ok: {result['ok']}",
        f"- dry-run chunk count: {result['dry_run']['chunk_count']}",
        f"- live fetch performed: {result['dry_run']['live_fetch_performed']}",
        f"- body text stored: {result['dry_run']['body_text_stored']}",
        f"- embedding created: {result['dry_run']['embedding_created']}",
        f"- authorization decision: {result['authorization_gate']['decision']}",
        f"- live ingestion allowed: {result['authorization_gate']['allowed_to_implement']}",
        "",
        "## Closed Scope",
        "",
    ]
    lines.extend(f"- {item}" for item in result["closed_scope"])
    lines.extend([
        "",
        "## Still Not Implemented",
        "",
    ])
    lines.extend(f"- {item}" for item in result["still_not_implemented"])
    lines.extend([
        "",
        "## Quality Preflight",
        "",
        f"- ran: {result['quality_preflight']['ran']}",
        f"- ok: {result['quality_preflight']['ok']}",
        f"- public_safe: {result['quality_preflight']['public_safe']}",
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


def write_report(*, run_quality_preflight: bool = False) -> dict[str, Any]:
    result = check_synthetic_parser_chunker_close_gate(run_quality_preflight=run_quality_preflight)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _run_quality_preflight() -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, "scripts/quality_preflight.py", "--format", "json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return {
            "ran": True,
            "ok": False,
            "public_safe": None,
            "errors": [completed.stderr.strip() or completed.stdout.strip() or f"exit {completed.returncode}"],
        }
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return {"ran": True, "ok": False, "public_safe": None, "errors": [f"invalid quality_preflight json: {exc}"]}
    return {
        "ran": True,
        "ok": payload.get("ok") is True,
        "public_safe": payload.get("public_safe") is True,
        "errors": payload.get("errors", []),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Close synthetic external source parser/chunker dry-run lane.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--run-quality-preflight", action="store_true")
    args = parser.parse_args()

    result = (
        write_report(run_quality_preflight=args.run_quality_preflight)
        if args.write
        else check_synthetic_parser_chunker_close_gate(run_quality_preflight=args.run_quality_preflight)
    )
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"chunk_count: {result['dry_run']['chunk_count']}")
        print(f"live_fetch_performed: {result['dry_run']['live_fetch_performed']}")
        print(f"body_text_stored: {result['dry_run']['body_text_stored']}")
        print(f"embedding_created: {result['dry_run']['embedding_created']}")
        print(f"live_ingestion_allowed: {result['authorization_gate']['allowed_to_implement']}")
        print(f"quality_preflight: {result['quality_preflight']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
