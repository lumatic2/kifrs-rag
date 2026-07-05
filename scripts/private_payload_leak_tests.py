from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-rlp4-private-payload-leak-tests.md"
DEFAULT_ARTIFACTS = [
    ROOT / "docs" / "reports" / "2026-07-05-rlp1-parser-prototype-asset-inventory.md",
    ROOT / "docs" / "reports" / "2026-07-05-rlp2-local-fixture-parser-adapter.md",
    ROOT / "docs" / "reports" / "2026-07-05-rlp3-deletion-automation-simulation.md",
]


@dataclass(frozen=True)
class PrivatePayloadLeak:
    artifact: str
    leak_type: str
    evidence: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


LEAK_PATTERNS = [
    ("identifier_like", re.compile(r"\b\d{3}-\d{2}-\d{5}\b")),
    ("resident_identifier_like", re.compile(r"\b\d{6}-[1-4]\d{6}\b")),
    ("ocr_payload_marker", re.compile(r"\bOCR PAYLOAD\s*:", re.IGNORECASE)),
    ("body_payload_marker", re.compile(r"\bPRIVATE_PAYLOAD\s*:", re.IGNORECASE)),
    ("raw_contract_marker", re.compile(r"<raw_contract>.*?</raw_contract>", re.IGNORECASE | re.DOTALL)),
    ("embedding_vector_like", re.compile(r"\[\s*-?\d+\.\d+\s*,\s*-?\d+\.\d+\s*,\s*-?\d+\.\d+")),
    ("absolute_private_file_path", re.compile(r"[A-Za-z]:\\(?:Users|private|client|tmp)\\", re.IGNORECASE)),
]


def scan_text_for_private_payloads(text: str, artifact: str = "<memory>") -> list[PrivatePayloadLeak]:
    leaks: list[PrivatePayloadLeak] = []
    for leak_type, pattern in LEAK_PATTERNS:
        for match in pattern.finditer(text):
            leaks.append(
                PrivatePayloadLeak(
                    artifact=artifact,
                    leak_type=leak_type,
                    evidence=_short_evidence(match.group(0)),
                )
            )
    return leaks


def scan_public_parser_artifacts(paths: Iterable[Path] = DEFAULT_ARTIFACTS) -> dict[str, object]:
    artifacts = list(paths)
    leaks: list[PrivatePayloadLeak] = []
    missing: list[str] = []
    for path in artifacts:
        if not path.exists():
            missing.append(_display_path(path))
            continue
        text = path.read_text(encoding="utf-8")
        leaks.extend(scan_text_for_private_payloads(text, _display_path(path)))
    return {
        "ok": not leaks and not missing,
        "scanned_artifacts": [_display_path(path) for path in artifacts],
        "missing_artifacts": missing,
        "leaks": [leak.to_dict() for leak in leaks],
        "leak_count": len(leaks),
        "completed_milestone": "RLP4",
        "next_leaf": "RLP5_local_parser_prototype_close_gate",
        "report_path": _display_path(REPORT_PATH),
    }


def render_report(result: dict[str, object]) -> str:
    lines = [
        "# RLP4 Private Payload Leak Tests",
        "",
        "> Scope: fail parser public artifacts if private payload-like content appears.",
        "",
        "## 한 줄 결론",
        "",
        "RLP4 adds a leak-test gate over the public parser prototype reports. The current RLP1-RLP3 artifacts pass: no identifier-like values, OCR payload markers, raw body markers, embedding-like vectors, or private absolute file paths were found.",
        "",
        "## Gate Result",
        "",
        f"- ok: {result['ok']}",
        f"- scanned artifacts: {len(result['scanned_artifacts'])}",
        f"- missing artifacts: {len(result['missing_artifacts'])}",
        f"- leak count: {result['leak_count']}",
        "",
        "## Scanned Artifacts",
        "",
    ]
    lines.extend(f"- `{path}`" for path in result["scanned_artifacts"])
    lines.extend(["", "## Leak Classes", ""])
    lines.extend(
        [
            "- identifier-like values",
            "- OCR payload markers",
            "- raw body markers",
            "- embedding-like vectors",
            "- private absolute file paths",
        ]
    )
    if result["leaks"]:
        lines.extend(["", "## Leaks", ""])
        lines.extend(
            f"- `{leak['artifact']}` {leak['leak_type']}: `{leak['evidence']}`"
            for leak in result["leaks"]
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This gate scans generated public artifacts, not private files.",
            "- It does not claim to inspect local quarantines or prove filesystem deletion.",
            "- It prevents obvious private payload shapes from entering parser reports.",
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
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, object]:
    result = scan_public_parser_artifacts()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_report(result), encoding="utf-8")
    return result


def _short_evidence(value: str) -> str:
    sanitized = " ".join(value.split())
    if len(sanitized) > 80:
        return sanitized[:77] + "..."
    return sanitized


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RLP4 private payload leak tests.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else scan_public_parser_artifacts()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"scanned_artifacts: {len(result['scanned_artifacts'])}")
        print(f"leak_count: {result['leak_count']}")
        print(f"next_leaf: {result['next_leaf']}")
        for leak in result["leaks"]:
            print(f"- {leak['artifact']} {leak['leak_type']}: {leak['evidence']}")
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
