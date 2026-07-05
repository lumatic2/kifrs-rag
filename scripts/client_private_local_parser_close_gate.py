from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.client_private_close_gate import run_client_private_close_gate  # noqa: E402
from scripts.client_private_deletion_attestation_check import check_deletion_attestation  # noqa: E402
from scripts.client_private_parser_dry_run_fixture_check import check_parser_dry_run_fixture  # noqa: E402
from scripts.client_private_upload_storage_policy_check import check_upload_storage_policy  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-cpl1-client-private-local-parser-close-gate.md"


def run_local_parser_close_gate(*, run_quality_preflight: bool = False) -> dict[str, object]:
    checks = {
        "local_only_close_gate": run_client_private_close_gate(run_quality_preflight=False),
        "upload_storage_policy": check_upload_storage_policy(),
        "parser_dry_run_fixture": check_parser_dry_run_fixture(),
        "deletion_attestation": check_deletion_attestation(),
    }
    errors: list[str] = []
    for name, result in checks.items():
        if not result["ok"]:
            errors.extend(f"{name}: {error}" for error in result["errors"])

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
            "local-only client-private control record",
            "public-safe redaction and review-pack routing",
            "upload/parser storage policy",
            "synthetic parser dry-run output contract",
            "local deletion attestation contract",
        ],
        "not_implemented": [
            "real file upload UI",
            "OCR",
            "real private document parser",
            "real file deletion automation",
            "private embedding/index namespace",
        ],
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or first local parser prototype spike",
    }


def render_close_report(result: dict[str, object]) -> str:
    lines = [
        "# CPL1 Client-Private Local Parser Close Gate",
        "",
        "> Scope: close the public-safe readiness path for future local client-private parser work.",
        "",
        "## 한 줄 결론",
        "",
        "The client-private local parser readiness path is now closed at the contract level: local-only intake, redaction, routing, storage policy, synthetic parser output, and deletion attestation all pass. This still does not implement real upload, OCR, parsing, deletion automation, or private embeddings.",
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

    lines.extend([
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
        "- The next parser work can start as a controlled local prototype instead of reopening safety policy decisions.",
        "- Public reports can prove readiness without storing source bodies or identifiers.",
        "- The gap audit can now move from policy/fixture/attestation readiness to prototype implementation or actual reviewer evidence.",
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
    result = run_local_parser_close_gate(run_quality_preflight=run_quality_preflight)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_close_report(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run client-private local parser close gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--run-quality-preflight", action="store_true")
    args = parser.parse_args()

    result = (
        write_close_report(run_quality_preflight=args.run_quality_preflight)
        if args.write
        else run_local_parser_close_gate(run_quality_preflight=args.run_quality_preflight)
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
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
