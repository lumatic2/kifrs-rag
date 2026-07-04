"""Boundary memo skeleton for 1109 financial instruments with 1021 FX translation."""

from .schema import Transaction1109

SECTION_TITLES = [
    "왜 dual-track인가",
    "1109 입력",
    "1021 입력",
    "표시 질문",
    "결론 보류",
]


def generate_fx_dual_track_memo(txn: Transaction1109) -> str:
    md: list[str] = [f"# 1109+1021 외화 금융상품 boundary memo — {txn.label}", ""]

    md.append(f"## 1. {SECTION_TITLES[0]}")
    md.append("- 금융상품 분류·측정은 1109 판단이고, 외화환산은 1021 판단이다.")
    md.append("- 두 판단을 한 결론으로 합치지 않고 입력과 표시 질문을 분리한다.")
    md.append("")

    md.append(f"## 2. {SECTION_TITLES[1]}")
    md.extend(
        [
            "- 금융상품 종류와 계약상 현금흐름",
            "- SPPI 판단 입력",
            "- 사업모형 evidence",
            "- FVOCI/FVPL/AC 분류 후보",
            "- 공정가치 변동 자료",
        ]
    )
    md.append("")

    md.append(f"## 3. {SECTION_TITLES[2]}")
    md.extend(
        [
            "- 기능통화",
            "- 계약통화",
            "- 취득일 환율",
            "- 보고일 환율",
            "- 이자/원금 수취일 환율",
        ]
    )
    md.append("")

    md.append(f"## 4. {SECTION_TITLES[3]}")
    md.extend(
        [
            "- 환산차이와 공정가치 변동을 어느 손익/OCI 라인에 표시할지?",
            "- FVOCI 부채상품이면 상각후원가 환산차이와 공정가치 변동을 어떻게 분리할지?",
            "- FVPL이면 환산효과와 공정가치 변동을 함께 PL로 표시하는지?",
            "- 기능통화 판단이 회사 회계정책과 일치하는지?",
        ]
    )
    md.append("")

    md.append(f"## 5. {SECTION_TITLES[4]}")
    md.append("- 결론: 사람 검토 필요.")
    md.append("- 자동화 경계: FH4는 1109와 1021 판단을 분리하는 boundary memo를 제공한다.")

    return "\n".join(md)
