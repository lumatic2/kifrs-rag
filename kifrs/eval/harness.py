"""평가 하네스 오케스트레이션.

실행:
  python -m kifrs.eval.harness --runner kifrs-mcp
  python -m kifrs.eval.harness --runner kifrs-mcp --only Q006 Q007 Q008
  python -m kifrs.eval.harness --runner baseline-noretrieval
  python -m kifrs.eval.harness --compare kifrs-mcp baseline-noretrieval
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from datetime import datetime
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from .models import GoldItem, ItemReport, RunReport
from .runners import KifrsMcpRunner, BaselineRunner, NotebookLmManualRunner
from .scorers import ALL_SCORERS
from .reporter import write_report


ROOT = Path(__file__).resolve().parent.parent.parent
GOLDSET = ROOT / "data" / "eval" / "goldset.json"
RESULTS_DIR = ROOT / "data" / "eval" / "results"


def load_goldset(path: Path = GOLDSET) -> list[GoldItem]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [GoldItem.from_dict(x) for x in data["items"]]


def build_runner(name: str):
    if name == "kifrs-mcp":
        return KifrsMcpRunner()
    if name == "baseline-noretrieval":
        return BaselineRunner()
    if name == "notebooklm-manual":
        return NotebookLmManualRunner()
    raise ValueError(f"unknown runner: {name}")


def run_eval(runner_name: str, items: list[GoldItem], verbose: bool = True) -> RunReport:
    runner = build_runner(runner_name)
    report = RunReport(
        runner=runner_name,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    for i, item in enumerate(items, 1):
        if verbose:
            print(f"  [{i}/{len(items)}] {item.id} — {item.source_ref[:60]}")
        run = runner.run(item)
        if run.error:
            if verbose:
                print(f"    ⚠️  {run.error}")
        scores = [s.score(item, run) for s in ALL_SCORERS]
        report.items.append(ItemReport(item=item, run=run, scores=scores))
        if verbose:
            c = report.items[-1].composite
            print(f"    composite={c:.2f}  " + "  ".join(f"{s.scorer}={s.score:.2f}" for s in scores))
    return report


def main():
    ap = argparse.ArgumentParser(description="K-IFRS RAG 평가 하네스")
    ap.add_argument("--runner", default="kifrs-mcp",
                    choices=["kifrs-mcp", "baseline-noretrieval", "notebooklm-manual"])
    ap.add_argument("--only", nargs="+", help="특정 item id만 (예: --only Q006 Q007)")
    ap.add_argument("--goldset", default=str(GOLDSET))
    ap.add_argument("--out", default=str(RESULTS_DIR))
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    items = load_goldset(Path(args.goldset))
    if args.only:
        wanted = set(args.only)
        items = [x for x in items if x.id in wanted]
        if not items:
            print(f"ERROR: --only {args.only} 에 해당하는 문항 없음", file=sys.stderr)
            sys.exit(1)

    print(f"▸ Runner: {args.runner}")
    print(f"▸ Items: {[x.id for x in items]}")
    print()

    report = run_eval(args.runner, items, verbose=not args.quiet)

    html_p, md_p, json_p = write_report(report, Path(args.out))
    print(f"\n✅ 완료 — composite 평균 = {report.mean_composite:.3f}")
    print(f"   HTML: {html_p.relative_to(ROOT)}")
    print(f"   MD:   {md_p.relative_to(ROOT)}")
    print(f"   JSON: {json_p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
