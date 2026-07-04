"""검토 메모 생성 (WORKFLOW.md §6 — 7섹션 템플릿)."""
from __future__ import annotations

from .classify import PathResult
from .identification import IdentificationResult
from .initial_entry import JournalEntry
from .schema import Lease1116

SECTION_TITLES = [
    "거래 개요", "리스 식별", "분류 / 면제 검토", "최초 측정",
    "후속 측정 방침", "변경/종료 시나리오 대비", "결론",
]


def _entry_lines_md(entry: JournalEntry) -> list[str]:
    return [
        f"- {'(차)' if line.debit else '(대)'} {line.account}  {line.debit or line.credit:,.0f}"
        for line in entry.lines
    ]


def generate_review_memo(
    lease: Lease1116,
    identification: IdentificationResult,
    path: PathResult,
    headlines: dict,
    initial_entry: JournalEntry | None,
    measurement_reasons: list[str],
) -> str:
    md: list[str] = [f"# 검토 메모 — {lease.label}", ""]

    md.append(f"## 1. {SECTION_TITLES[0]}")
    md.append(f"- 입장: {'리스이용자' if lease.party == 'lessee' else '리스제공자'}")
    if lease.lease_term_years is not None:
        md.append(f"- 리스기간: {lease.lease_term_years}년 / 할인율: {lease.discount_rate:.0%}"
                  if lease.discount_rate is not None else f"- 리스기간: {lease.lease_term_years}년")
    if lease.annual_payment is not None:
        md.append(f"- 정기리스료: {lease.annual_payment:,.0f}")
    md.append("")

    md.append(f"## 2. {SECTION_TITLES[1]}")
    md.append(f"- 결론: {'리스' if identification.is_lease else '리스 아님(서비스 계약)'}")
    md.append(f"- 근거: {'; '.join(identification.reasons)}")
    md.append("")

    md.append(f"## 3. {SECTION_TITLES[2]}")
    md.append(f"- 경로: {path.path}")
    md.append(f"- 근거: {'; '.join(path.reasons)}")
    md.append("")

    md.append(f"## 4. {SECTION_TITLES[3]}")
    for key, val in headlines.items():
        md.append(f"- {key}: {val:,.0f}")
    if measurement_reasons:
        md.append(f"- 근거: {'; '.join(measurement_reasons)}")
    md.append("")

    md.append(f"## 5. {SECTION_TITLES[4]}")
    if path.path == "lessee_recognition":
        md.append("- 사용권자산 원가모형 정액 감가 [1116-29], 리스부채 유효이자율 후속 [1116-36]")
    elif path.path == "lessee_exemption":
        md.append("- 면제 — 리스료 정액 비용, 사용권자산·리스부채 미인식 [1116-6]")
    elif path.path == "lessor_finance":
        md.append("- 리스순투자에 일정 기간수익률 금융수익 인식 [1116-75]")
    else:
        md.append("- 운용리스자산 감가 계속, 리스료수익 정액 인식 [1116-81, 84]")
    md.append("")

    md.append(f"## 6. {SECTION_TITLES[5]}")
    if lease.events:
        for e in lease.events:
            md.append(f"- {e.effective} {e.kind} — §5 재측정/변경 처리 적용")
    else:
        md.append("- 변경·재평가 이벤트 없음 (재측정 트리거 발생 시 §5 적용)")
    md.append("")

    md.append(f"## 7. {SECTION_TITLES[6]}")
    if initial_entry is not None:
        md.append(f"- {lease.label}: {path.path} 경로, 최초인식 차변 {initial_entry.total_debit:,.0f}.")
    else:
        md.append(f"- {lease.label}: {path.path} 경로.")
    md.append("- 잔존 의문점: 없음(AE1 core pipeline 자동 산출).")

    return "\n".join(md)
