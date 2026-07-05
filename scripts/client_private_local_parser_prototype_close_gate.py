from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.client_private_local_parser_close_gate import run_local_parser_close_gate  # noqa: E402
from scripts.client_private_local_parser_prototype_spike import check_local_parser_prototype  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-lpc1-local-parser-prototype-close-gate.md"


def run_local_parser_prototype_close_gate(*, run_quality_preflight: bool = False) -> dict[str, object]:
    checks = {
        "parser_readiness": run_local_parser_close_gate(run_quality_preflight=False),
        "parser_prototype": check_local_parser_prototype(),
    }
    errors: list[str] = []
    for name, result in checks.items():
        if not result["ok"]:
            errors.extend(f"{name}: {error}" for error in result["errors"])

    prototype = checks["parser_prototype"]
    route_status = prototype["route"].get("status")
    route = prototype["route"].get("route")
    deletion_status = prototype["prototype_result"].get("deletion_attestation", {}).get("deletion_status")
    if route_status != "candidate":
        errors.append(f"parser_prototype: route_status must be candidate, got {route_status}")
    if route != "kifrs1116_review_pack":
        errors.append(f"parser_prototype: route must be kifrs1116_review_pack, got {route}")
    if deletion_status != "deleted":
        errors.append(f"parser_prototype: deletion_status must be deleted, got {deletion_status}")

    quality_preflight: dict[str, object] = {"ran": False}
    if run_quality_preflight:
        completed = subprocess.run(
            [sys.executable, "scripts/quality_preflight.py", "--format", "json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        quality_preflight = {
            "ran": True,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
        if completed.returncode != 0:
            errors.append("quality_preflight failed")
        else:
            try:
                parsed = json.loads(completed.stdout)
            except json.JSONDecodeError:
                errors.append("quality_preflight did not return JSON")
            else:
                quality_preflight["ok"] = parsed.get("ok")
                quality_preflight["public_safe"] = parsed.get("public_safe")
                if parsed.get("ok") is not True or parsed.get("public_safe") is not True:
                    errors.append("quality_preflight did not pass public-safe gate")

    return {
        "ok": not errors,
        "errors": errors,
        "checks": checks,
        "quality_preflight": quality_preflight,
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "closed_scope": [
            "client-private parser readiness contract",
            "synthetic local parser prototype",
            "review-pack route candidate",
            "deletion attestation after prototype run",
            "public-safe quality preflight when requested",
        ],
        "not_implemented": [
            "real file upload UI",
            "OCR",
            "real private document parser adapter",
            "real file deletion automation",
            "private embedding/index namespace",
        ],
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or local parser adapter contract",
    }


def render_close_report(result: dict[str, object]) -> str:
    lines = [
        "# LPC1 Local Parser Prototype Close Gate",
        "",
        "> Scope: close the first synthetic local parser prototype against the client-private safety gates.",
        "",
        "## 한 줄 결론",
        "",
        "The first local parser prototype is closed at the public-safe prototype level: parser readiness passes, the synthetic parser output routes to a KIFRS1116 review-pack candidate, deletion attestation is present, and optional quality preflight remains public-safe. Real upload, OCR, private-file parsing, deletion automation, and private embeddings are still not implemented.",
        "",
        "## Check Results",
        "",
        "| Check | Status |",
        "|---|---|",
    ]
    for name, check in result["checks"].items():
        lines.append(f"| {name} | {'ok' if check['ok'] else 'failed'} |")
    qp = result["quality_preflight"]
    if qp.get("ran"):
        lines.append(f"| quality_preflight | {'ok' if qp.get('ok') and qp.get('public_safe') else 'failed'} |")

    prototype = result["checks"]["parser_prototype"]
    lines.extend([
        "",
        "## Prototype Route",
        "",
        f"- Route: {prototype['route'].get('route')}",
        f"- Route status: {prototype['route'].get('status')}",
        f"- Deletion status: {prototype['prototype_result'].get('deletion_attestation', {}).get('deletion_status')}",
        "",
        "## Closed Scope",
        "",
    ])
    lines.extend(f"- {item}" for item in result["closed_scope"])
    lines.extend([
        "",
        "## Still Not Implemented",
        "",
    ])
    lines.extend(f"- {item}" for item in result["not_implemented"])
    lines.extend([
        "",
        "## What This Means",
        "",
        "- The next parser work can focus on an adapter contract instead of reopening safety boundaries.",
        "- Public artifacts now show a complete synthetic parser path from extracted fields to route candidate.",
        "- Real private-file handling remains blocked until a separate local-only adapter gate exists.",
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


def write_close_report(*, run_quality_preflight: bool = False) -> dict[str, object]:
    result = run_local_parser_prototype_close_gate(run_quality_preflight=run_quality_preflight)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_close_report(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local parser prototype close gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--run-quality-preflight", action="store_true")
    args = parser.parse_args()

    result = (
        write_close_report(run_quality_preflight=args.run_quality_preflight)
        if args.write
        else run_local_parser_prototype_close_gate(run_quality_preflight=args.run_quality_preflight)
    )
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_close_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        for name, check in result["checks"].items():
            print(f"{name}: {check['ok']}")
        qp = result["quality_preflight"]
        if qp.get("ran"):
            print(f"quality_preflight: {qp.get('ok')} public_safe={qp.get('public_safe')}")
        print(f"route: {result['checks']['parser_prototype']['route'].get('route')}")
        print(f"route_status: {result['checks']['parser_prototype']['route'].get('status')}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
