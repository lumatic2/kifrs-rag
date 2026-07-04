from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.client_private_contract_check import check_client_private_contract  # noqa: E402
from scripts.client_private_intake_readiness_check import check_client_private_intake_readiness  # noqa: E402
from scripts.client_private_redaction_gate_check import check_client_private_redaction_gate  # noqa: E402
from scripts.client_private_routing_bridge_check import check_client_private_routing_bridge  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-cp4-client-private-close-report.md"


def run_client_private_close_gate(*, run_quality_preflight: bool = False) -> dict[str, object]:
    checks = {
        "contract": check_client_private_contract(),
        "redaction": check_client_private_redaction_gate(),
        "routing": check_client_private_routing_bridge(),
        "readiness": check_client_private_intake_readiness(),
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
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or live external source/retriever validation",
    }


def render_close_report(result: dict[str, object]) -> str:
    checks = result["checks"]
    lines = [
        "# CP4 Client-Private Close Report",
        "",
        "> Scope: local-only client-private intake contract, redaction gate, and review-pack routing bridge.",
        "",
        "## 한 줄 결론",
        "",
        "Client-private local-only path is closed for public-safe planning. It still does not implement upload, OCR, private document parsing, or storage of raw source bodies.",
        "",
        "## Check Results",
        "",
        "| Check | Status |",
        "|---|---|",
    ]
    for name, check in checks.items():
        lines.append(f"| {name} | {'ok' if check['ok'] else 'failed'} |")

    lines.extend([
        "",
        "## What Is Now Possible",
        "",
        "- Define a local-only client-private control record.",
        "- Reject raw private payload fields before public output.",
        "- Redact local-only locator and notes from public summaries.",
        "- Route redacted structured facts to 1109/1115/1116 review-pack candidates.",
        "",
        "## Still Not Implemented",
        "",
        "- file upload",
        "- OCR",
        "- private document parsing",
        "- committed private source body",
        "- live customer data storage",
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
    result = run_client_private_close_gate(run_quality_preflight=run_quality_preflight)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_close_report(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run CP4 local-only client-private close gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--run-quality-preflight", action="store_true")
    args = parser.parse_args()

    result = write_close_report(run_quality_preflight=args.run_quality_preflight) if args.write else run_client_private_close_gate(run_quality_preflight=args.run_quality_preflight)
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
