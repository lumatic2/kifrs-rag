from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.private_parser_authorization_safe_adapter_proof import build_authorization_safe_adapter_proof  # noqa: E402
from scripts.private_parser_deletion_retention_rehearsal import build_deletion_retention_rehearsal  # noqa: E402
from scripts.private_parser_fixture_adapter_contract import build_fixture_adapter_contract  # noqa: E402
from scripts.private_parser_public_report_leak_gate import build_public_report_leak_gate  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-private-parser-realism-hardening-close-report.md"


def build_close_gate() -> dict[str, Any]:
    ppr1 = build_authorization_safe_adapter_proof()
    ppr2 = build_fixture_adapter_contract()
    ppr3 = build_deletion_retention_rehearsal()
    ppr4 = build_public_report_leak_gate()
    evidence = [
        _evidence("PPR1", "authorization-safe adapter proof", "docs/reports/2026-07-05-ppr1-authorization-safe-adapter-proof.md", ppr1["ok"]),
        _evidence("PPR2", "fixture adapter contract", "docs/reports/2026-07-05-ppr2-fixture-adapter-contract.md", ppr2["ok"]),
        _evidence("PPR3", "deletion retention rehearsal", "docs/reports/2026-07-05-ppr3-deletion-retention-rehearsal.md", ppr3["ok"]),
        _evidence("PPR4", "public report leak gate", "docs/reports/2026-07-05-ppr4-public-report-leak-gate.md", ppr4["ok"]),
    ]
    checks = {
        "all_evidence_exists": all(item["exists"] for item in evidence),
        "all_gates_ok": all(item["gate_ok"] for item in evidence),
        "real_payload_ingestion_not_claimed": True,
        "public_reports_leak_free": ppr4["ok"] and not ppr4["hits"],
        "next_gap_handoff_present": True,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "Private Parser Realism Hardening Close Report",
        "ok": not errors,
        "horizon": "private-parser-realism-hardening",
        "completed_milestone": "PPR5",
        "close_result": "realism_contract_ready",
        "evidence": evidence,
        "checks": checks,
        "errors": errors,
        "residual_risks": [
            "No real protected payload has been ingested.",
            "Actual OCR/parser/deletion automation still requires explicit authorization.",
            "The next objective gap is external source body connector expansion.",
        ],
        "next_horizon": "external-source-body-connector-expansion",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: close gate for private parser realism hardening.",
        "",
        "## 한 줄 결론",
        "",
        f"Close result: `{result['close_result']}`. Real private payload ingestion remains explicitly gated.",
        "",
        f"- Next horizon: `{result['next_horizon']}`",
        "",
        "## Evidence",
        "",
        "| Milestone | Evidence | Exists | Gate OK |",
        "|---|---|---|---|",
    ]
    for item in result["evidence"]:
        lines.append(f"| {item['id']} {item['name']} | `{item['path']}` | {item['exists']} | {item['gate_ok']} |")
    lines.extend(["", "## Checks", "", "| Check | OK |", "|---|---|"])
    for name, ok in result["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Residual Risks", ""])
    lines.extend(f"- {risk}" for risk in result["residual_risks"])
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in result["errors"]) if result["errors"] else lines.append("- none")
    lines.extend(
        [
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
    result = build_close_gate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _evidence(id_: str, name: str, path: str, gate_ok: bool) -> dict[str, Any]:
    return {"id": id_, "name": name, "path": path, "exists": (ROOT / path).exists(), "gate_ok": gate_ok}


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Close private parser realism hardening horizon.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_close_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- close result: {result['close_result']}")
        print(f"- next horizon: {result['next_horizon']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
