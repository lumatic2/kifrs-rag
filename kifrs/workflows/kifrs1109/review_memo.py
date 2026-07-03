"""검토 메모 생성 (WORKFLOW.md §6 — 7섹션 템플릿)."""
from __future__ import annotations

from .amortization import AmortizationRow, RevaluationRow
from .classify import ClassificationResult
from .initial_entry import JournalEntry
from .schema import Transaction1109

SECTION_TITLES = [
    "거래 개요", "SPPI 테스트", "사업모형 평가", "분류 결정",
    "최초 인식 분개", "후속 측정 방침", "결론",
]


def _entry_lines_md(entry: JournalEntry) -> list[str]:
    return [
        f"- {'(차)' if line.debit else '(대)'} {line.account}  {line.debit or line.credit:,.0f}"
        for line in entry.lines
    ]


def generate_review_memo(
    txn: Transaction1109,
    result: ClassificationResult,
    initial_entry: JournalEntry,
    subsequent_rows: list[AmortizationRow] | list[RevaluationRow] | None = None,
) -> str:
    """WORKFLOW.md §6 템플릿을 classify()/initial_recognition_entry()/amortization.py
    산출물로 채운다. subsequent_rows는 회계처리 방침 서술용 — 이번 범위는 §6은 방침
    서술까지만, 상각표 자체는 subsequent_entry.py 분개로 별도 확인한다."""
    md: list[str] = [f"# 검토 메모 — {txn.label}", ""]

    md.append(f"## 1. {SECTION_TITLES[0]}")
    md.append(f"- 자산 종류: {txn.instrument_type}")
    if txn.principal is not None:
        md.append(f"- 명목금액: {txn.principal:,.0f}")
    md.append(f"- 취득 공정가치: {txn.purchase_price:,.0f} / 거래원가: {txn.transaction_cost:,.0f}")
    md.append("")

    md.append(f"## 2. {SECTION_TITLES[1]}")
    if result.sppi is not None:
        md.append(f"- 결정: {'Pass' if result.sppi.passed else 'Fail'}")
        md.append(f"- 근거: {'; '.join(result.sppi.reasons)}")
    else:
        md.append("- 해당 없음 (지분증권 — §1B 별도 분기)")
    md.append("")

    md.append(f"## 3. {SECTION_TITLES[2]}")
    if result.business_model is not None:
        md.append(f"- 결정: 사업모형 {result.business_model.model}")
        md.append(f"- 근거: {'; '.join(result.business_model.reasons)}")
    else:
        md.append("- 해당 없음 (SPPI Fail, 지분증권, 또는 지정 오버라이드로 사업모형 평가 불필요)")
    md.append("")

    md.append(f"## 4. {SECTION_TITLES[3]}")
    md.append(f"- 분류: **{result.classification}**")
    md.append(f"- 근거: {'; '.join(result.reasons)}")
    md.append("")

    md.append(f"## 5. {SECTION_TITLES[4]}")
    md.extend(_entry_lines_md(initial_entry))
    md.append("")

    md.append(f"## 6. {SECTION_TITLES[5]}")
    if subsequent_rows:
        if isinstance(subsequent_rows[0], AmortizationRow):
            md.append("- 유효이자율법 상각 — 매기 실효이자를 이자수익으로 인식")
            if result.classification == "FVOCI_DEBT":
                md.append("- 상각후원가 기준 장부금액과 기말 공정가치 차이를 누적 OCI로 인식, 처분 시 PL 재분류 [1109-5.7.10]")
        else:
            income = "매기 표시이자를 명목 이자수익으로 인식" if result.classification == "FVPL" else "배당은 PL에 인식 [1109-5.7.6]"
            md.append(f"- {income}, 기말 공정가치 변동 전액을 {'PL' if result.classification == 'FVPL' else 'OCI(처분 시에도 PL 재분류 없음)'}로 인식")
    else:
        md.append("- 후속측정 기간 관측치 없음(최초인식만 확인)")
    md.append("")

    md.append(f"## 7. {SECTION_TITLES[6]}")
    md.append(
        f"- {txn.label}: {result.classification} 분류, 최초인식 {initial_entry.total_debit:,.0f}. "
        "잔존 의문점: 없음(WA1 core pipeline 자동 산출)."
    )

    return "\n".join(md)
