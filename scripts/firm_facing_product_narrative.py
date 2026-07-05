from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


README_PATH = ROOT / "README.md"
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-fps4-product-narrative.md"

REQUIRED_PHRASES = [
    "Firm-Facing Local Demo",
    "python scripts/firm_facing_operator_demo_command.py --format markdown --write",
    "What it can do now",
    "What it does not do",
    "does not replace accountant judgment",
    "not a packaged SaaS product yet",
]


def build_narrative_check() -> dict[str, Any]:
    text = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else ""
    missing = [phrase for phrase in REQUIRED_PHRASES if phrase not in text]
    forbidden_hits = [item for item in ("source_body", "api_key", "secret", "raw_xml", "xbrl_dump") if item in text.lower()]
    return {
        "title": "FPS4 Product Narrative README Surface",
        "ok": not missing and not forbidden_hits,
        "horizon": "firm-facing-product-surface",
        "milestone": "FPS4",
        "readme_path": _display_path(README_PATH),
        "required_phrases": REQUIRED_PHRASES,
        "missing_phrases": missing,
        "forbidden_hits": forbidden_hits,
        "narrative_claims": [
            "The product is a local accounting-intelligence toolkit prototype for firm-side PoC.",
            "The current showable surface is the K-IFRS 1116 operator walkthrough packet.",
            "The output is decision-support only; accountant judgment and sign-off remain human.",
            "Protected standards, embeddings, dogfood material, and private client payloads are not published.",
        ],
        "report_path": _display_path(REPORT_PATH),
        "next_leaf": "FPS5_firm_facing_surface_close_gate",
    }


def render_markdown(check: dict[str, Any]) -> str:
    lines = [
        f"# {check['title']}",
        "",
        "> Scope: FPS4 README/product narrative check for the firm-facing local demo surface.",
        "",
        "## One-Line Result",
        "",
        (
            "The README now explains the current firm-facing demo command, capability boundary, and non-goals."
            if check["ok"]
            else "The README product narrative is incomplete or not public-safe."
        ),
        "",
        "## README",
        "",
        f"- path: `{check['readme_path']}`",
        f"- ok: {check['ok']}",
        "",
        "## Narrative Claims",
        "",
    ]
    lines.extend(f"- {claim}" for claim in check["narrative_claims"])
    lines.extend(["", "## Missing Phrases", ""])
    lines.extend(f"- {phrase}" for phrase in check["missing_phrases"]) if check["missing_phrases"] else lines.append("- none")
    lines.extend(["", "## Forbidden Hits", ""])
    lines.extend(f"- {hit}" for hit in check["forbidden_hits"]) if check["forbidden_hits"] else lines.append("- none")
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(check, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    check = build_narrative_check()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(check), encoding="utf-8")
    return check


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Check FPS4 firm-facing product narrative surface.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    check = write_report(args.out) if args.write else build_narrative_check()
    if args.format == "json":
        print(json.dumps(check, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(check), end="")
    else:
        print(check["title"])
        print(f"- ok: {check['ok']}")
        print(f"- missing phrases: {check['missing_phrases']}")
        print(f"- forbidden hits: {check['forbidden_hits']}")
        print(f"- next leaf: {check['next_leaf']}")
    return 0 if check["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
