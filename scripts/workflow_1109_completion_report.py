"""WA1 완료율 리포트 생성 — 10개 1109 시나리오를 실행하고 결과를 docs/reports/에 남긴다.

(docs/plans/2026-07-03-wa1-1109-pilot-engine.md Step 8 통합 검증)
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.workflows.kifrs1109.fixtures import FIXTURES
from kifrs.workflows.kifrs1109.runner import run_scenario

DEFAULT_OUT = ROOT / "docs" / "reports" / "2026-07-03-wa1-completion-rate.md"


def build_report(report_date: str) -> str:
    outcomes = [run_scenario(f) for f in FIXTURES]
    automated = [o for o in outcomes if o.status == "automated"]
    needs_review = [o for o in outcomes if o.status == "needs_human_review"]
    rate = len(automated) / len(outcomes)

    lines = [
        "# WA1 — 1109 파일럿 완료율 리포트",
        "",
        f"> Generated: {report_date}",
        f"> Objective 움직이는 축: 시나리오 완료율 (`docs/OBJECTIVE.md`)",
        f"> Horizon: `docs/horizons/workflow-automation.md`",
        "",
        f"## 완료율: {len(automated)}/{len(outcomes)} ({rate:.0%})",
        "",
        "\"완료\" = 구조화 거래 입력 -> SPPI/사업모형 판단 -> 최초인식 분개 -> 후속측정 -> 검토메모까지",
        "사람 개입·수정 없이 코드가 끝까지 산출. 100% 미달은 실패가 아니다 — 이번 milestone의",
        "목표는 \"측정 가능한 상태\"이지 100% 통과가 아니다(docs/plans/2026-07-03-wa1-1109-pilot-engine.md).",
        "",
        "## 자동화됨",
        "",
        "| 시나리오 | 분류 | 최초인식 | 후속측정 분개 수 |",
        "|---|---|---|---|",
    ]
    for o in automated:
        lines.append(f"| {o.label} | {o.classification} | {o.initial_total:,.0f} | {o.subsequent_entry_count} |")

    lines += [
        "",
        "## 사람 개입 필요 (WA1 core pipeline 밖)",
        "",
        "| 시나리오 | 사유 |",
        "|---|---|",
    ]
    for o in needs_review:
        lines.append(f"| {o.label} | {o.reason} |")

    lines += [
        "",
        "## 다음",
        "",
        "- 사람 개입 필요 4건(IFRIC19 발행자 부채소멸, SPPI 변동금리 재설정 불일치, 재분류,",
        "  외화 이중트랙)은 각자 별도 결정 로직이 필요 — WA2/WA3 후보로 승격 검토",
        "  (`docs/horizons/workflow-automation.md`).",
        "- 자동화 6건은 회귀 테스트로 고정(`tests/test_workflow_1109_regression.py`) —",
        "  향후 리팩토링이 숫자를 바꾸면 테스트가 먼저 실패한다.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--date", default=str(date.today()))
    args = parser.parse_args()

    report = build_report(args.date)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    print(f"[ok] wrote {out_path}")
    print(report)


if __name__ == "__main__":
    main()
