from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.workflows.source_aware_rebuild import (
    assert_public_safe_report,
    build_default_rebuild_report,
    render_rebuild_report_markdown,
)


DEFAULT_OUT = Path("docs/reports/2026-07-05-wr3-source-aware-rebuild-report.md")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a source-aware F-ACC workflow rebuild report.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    report = build_default_rebuild_report()
    assert_public_safe_report(report.to_dict())

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_rebuild_report_markdown(report), encoding="utf-8")
    print(f"wrote {args.out}")
    print(f"total_packs: {report.total_packs}")
    print(f"automated_packs: {report.automated_packs}")
    print(f"human_review_packs: {report.human_review_packs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
