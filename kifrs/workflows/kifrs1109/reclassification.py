"""Review-memo skeleton for 1109 business-model reclassification cases."""

from .schema import Transaction1109

SECTION_TITLES = [
    "재분류 트리거",
    "필요 입력",
    "판단 질문",
    "처리 방향 초안",
    "결론 보류",
]


def generate_reclassification_memo(txn: Transaction1109) -> str:
    md: list[str] = [f"# 1109 재분류 검토메모 skeleton — {txn.label}", ""]

    md.append(f"## 1. {SECTION_TITLES[0]}")
    md.append("- 금융자산 재분류는 사업모형 변경의 사실과 적용일 판단이 필요하다.")
    md.append("- 자동 분류 결론을 내지 않고, 아래 입력을 확보한 뒤 수동 workpaper로 완성한다.")
    md.append("")

    md.append(f"## 2. {SECTION_TITLES[1]}")
    md.extend(
        [
            "- 사업모형 변경 승인 자료",
            "- 변경일 및 재분류일",
            "- 변경 전후 보유 목적",
            "- 재분류일 공정가치",
            "- 기존 장부금액과 유효이자율",
            "- 변경 전후 분류 후보(AC/FVOCI/FVPL)",
        ]
    )
    md.append("")

    md.append(f"## 3. {SECTION_TITLES[2]}")
    md.extend(
        [
            "- 사업모형 변경이 외부적으로 관찰 가능한가?",
            "- 변경이 경영진 의도 변경만이 아니라 실제 사업 활동 변경인가?",
            "- 재분류일 이후 전진 적용이 맞는가?",
            "- 재분류일 공정가치를 신뢰성 있게 측정할 수 있는가?",
        ]
    )
    md.append("")

    md.append(f"## 4. {SECTION_TITLES[3]}")
    md.append("- 기준서 방향: 사업모형 변경이 확인되면 재분류일 이후 전진 적용을 검토한다.")
    md.append("- 분개 초안: 재분류 전후 분류와 재분류일 공정가치 확정 후 작성한다.")
    md.append("")

    md.append(f"## 5. {SECTION_TITLES[4]}")
    md.append("- 결론: 사람 검토 필요.")
    md.append("- 자동화 경계: FH3는 결론 산출이 아니라 누락 입력과 판단 질문을 구조화한다.")

    return "\n".join(md)
