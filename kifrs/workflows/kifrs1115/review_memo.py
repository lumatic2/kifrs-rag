"""Review memo renderer for 1115 revenue decisions."""

from .classify import RevenueDecision, evaluate_revenue
from .journal_entry import JournalEntry, draft_journal_entries
from .measurement import RevenueMeasurement, measure_revenue
from .schema import Revenue1115

SECTION_TITLES = [
    "거래 개요",
    "5단계 수익인식 판단",
    "측정",
    "분개 초안",
    "결론",
]


def _entry_lines_md(entry: JournalEntry) -> list[str]:
    return [
        f"- {'(차)' if line.debit else '(대)'} {line.account}  {line.debit or line.credit:,.0f}"
        for line in entry.lines
    ]


def generate_review_memo(
    txn: Revenue1115,
    decision: RevenueDecision | None = None,
    measurement: RevenueMeasurement | None = None,
    entries: list[JournalEntry] | None = None,
) -> str:
    decision = decision or evaluate_revenue(txn)
    measurement = measurement or measure_revenue(txn, decision)
    entries = entries or draft_journal_entries(txn, decision, measurement)

    md: list[str] = [f"# 검토 메모 — {txn.label}", ""]

    md.append(f"## 1. {SECTION_TITLES[0]}")
    md.append(f"- 시나리오 유형: {txn.scenario_type}")
    md.append(f"- 판단 경로: {decision.path}")
    md.append(f"- 계약금액: {txn.contract_price:,.0f}")
    md.append("")

    md.append(f"## 2. {SECTION_TITLES[1]}")
    for step in decision.five_step:
        md.append(
            f"- Step {step.step} {step.name}: {step.conclusion} "
            f"[{', '.join(step.citations)}]"
        )
    md.append("")

    md.append(f"## 3. {SECTION_TITLES[2]}")
    md.append(f"- 당기 수익 초안: {measurement.recognized_revenue:,.0f}")
    if measurement.deferred_revenue:
        md.append(f"- 이연/계약부채 초안: {measurement.deferred_revenue:,.0f}")
    if measurement.financing_effect:
        md.append(f"- 금융요소/스프레드 초안: {measurement.financing_effect:,.0f}")
    if measurement.repurchase_liability:
        md.append(f"- 재매입 관련 부채 초안: {measurement.repurchase_liability:,.0f}")
    if measurement.allocation:
        md.append("- 배분:")
        for line in measurement.allocation:
            md.append(
                f"  - {line.obligation}: SSP {line.standalone_selling_price:,.0f}, "
                f"배분 {line.allocated_transaction_price:,.0f}"
            )
    if measurement.notes:
        md.append(f"- 측정 메모: {'; '.join(measurement.notes)}")
    md.append("")

    md.append(f"## 4. {SECTION_TITLES[3]}")
    for entry in entries:
        md.append(f"### {entry.label}")
        md.extend(_entry_lines_md(entry))
    md.append("")

    md.append(f"## 5. {SECTION_TITLES[4]}")
    md.append(f"- {txn.label}: {decision.path} 경로.")
    md.append(f"- 주요 근거: {', '.join(decision.citations)}")
    md.append("- 잔존 의문점: 입력 사실과 추정치 검토 필요(R15 자동 산출 초안).")

    return "\n".join(md)
