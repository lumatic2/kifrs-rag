from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.feedback.case_intake import (  # noqa: E402
    ClientPrivateDeletionAttestation,
    ClientPrivateParserDryRunFixture,
    RedactedClientPrivateSummary,
    RoutingCandidate,
)
from kifrs.feedback.local_parser import LocalPrivateParserPrototypeResult  # noqa: E402
from kifrs.runtime.client_private_deletion import (  # noqa: E402
    build_runtime_client_private_deletion_gate,
    render_runtime_client_private_deletion_gate,
)
from kifrs.runtime.client_private_parser import contract_from_parser_prototype_result  # noqa: E402
from scripts.client_private_local_parser_adapter_contract_check import (  # noqa: E402
    check_local_parser_adapter_contract,
)


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-cp4-private-runtime-deletion-gate.md"


def build_deletion_gate_report() -> dict[str, Any]:
    prototype = _prototype_result(check_local_parser_adapter_contract()["prototype_result"])
    contract = contract_from_parser_prototype_result(prototype)
    gate = build_runtime_client_private_deletion_gate(contract, prototype.deletion_attestation)
    rendered = render_runtime_client_private_deletion_gate(gate)
    return {
        "title": "CP4 Private Runtime Deletion Gate",
        "ok": gate.ok and _public_safe(rendered),
        "horizon": "client-private-parser-runtime",
        "milestone": "CP4",
        "gate": gate.to_dict(),
        "public_safe": _public_safe(rendered),
        "next_leaf": "CP5_private_runtime_close_demo",
        "report_path": _display_path(REPORT_PATH),
        "rendered_gate": rendered,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# {report['title']}",
        "",
        "> Scope: CP4 runtime close gate for client-private deletion and retention state.",
        "",
        "## Result",
        "",
        f"- ok: {report['ok']}",
        f"- horizon: `{report['horizon']}`",
        f"- milestone: `{report['milestone']}`",
        f"- public safe: {report['public_safe']}",
        f"- next leaf: `{report['next_leaf']}`",
        "",
        "## Runtime Gate",
        "",
        report["rendered_gate"],
        "",
        "## Boundary Meaning",
        "",
        "- Client-private parser runtime cannot close unless deletion state is explicit.",
        "- The gate blocks raw file, parsed body, OCR text, and private embedding presence.",
        "- The public report records state only, not private content.",
        "",
        "## Machine Result",
        "",
        "```json",
        json.dumps({key: value for key, value in report.items() if key != "rendered_gate"}, ensure_ascii=False, indent=2, default=str),
        "```",
    ]
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    report = build_deletion_gate_report()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(report), encoding="utf-8")
    return report


def _prototype_result(data: dict[str, object]) -> LocalPrivateParserPrototypeResult:
    return LocalPrivateParserPrototypeResult(
        parser_run_id=str(data["parser_run_id"]),
        fixture=ClientPrivateParserDryRunFixture(**data["fixture"]),
        redacted_summary=RedactedClientPrivateSummary(**data["redacted_summary"]),
        route=RoutingCandidate(**data["route"]),
        deletion_attestation=ClientPrivateDeletionAttestation(**data["deletion_attestation"]),
    )


def _public_safe(rendered: str) -> bool:
    forbidden = ("api_key", "token", "source_body", "raw_contract", "contract_body", "full_text")
    return not any(item in rendered for item in forbidden)


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Render CP4 private runtime deletion gate report.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    report = write_report(args.out) if args.write else build_deletion_gate_report()
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(report), end="")
    else:
        print(report["title"])
        print(f"- ok: {report['ok']}")
        print(f"- public safe: {report['public_safe']}")
        print(f"- next leaf: {report['next_leaf']}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
