"""IB2 파싱 수리 targeted tests — BC 세분화 + 섹션 제목 복구/오탐 차단.

합성 페이지 텍스트로 kifrs/parse.py의 parse_pages를 직접 검증한다 (PDF 원문 불필요).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kifrs.parse import parse_pages


def _by_no(paras):
    return {p["no"]: p for p in paras}


def test_bc_paragraphs_are_split():
    pages = [
        "1 이 기준서의 목적은 재무제표 표시이다.\n"
        "결론도출근거\n"
        "BC1 IASC는 1975년에 최초 기준서를 공표하였다.\n"
        "BC2 2001년 7월에 위원회는 개정을 논의하였다.\n"
        "BC48EA 두 글자 suffix 문단도 분리한다.\n"
        "한BC104.1 기업이 주가 변동에 따라 행사가격을 조정할 수 있는 조건을\n"
        "검토하였다.\n"
        "한BC104.2 처음에는 공시 대상으로 리픽싱 조건이 있는 상품을 다뤘다.\n"
    ]
    paras = _by_no(parse_pages(pages, "1001"))
    assert "BC1" in paras and "BC2" in paras
    assert "BC48EA" in paras
    assert "한BC104.1" in paras and paras["한BC104.1"]["ko_added"]
    assert paras["한BC104.1"]["appendix"] == "BC"
    assert "행사가격" in paras["한BC104.1"]["body"]
    # BC1 본문에 다른 BC 문단이 흡수되지 않음
    assert "2001년" not in paras["BC1"]["body"]


def test_bc_zone_blocks_plain_number_split():
    pages = [
        "1 본문 문단이다.\n"
        "BC1 결론도출근거 본문인데 다음 줄이\n"
        "1 숫자로 시작해도 새 문단으로 쪼개지 않는다.\n"
        "BC2 다음 문단.\n"
    ]
    paras = _by_no(parse_pages(pages, "1001"))
    assert "1 숫자로" not in "".join(p["no"] for p in parse_pages(pages, "1001"))
    assert "숫자로 시작해도" in paras["BC1"]["body"]


def test_bc_not_applied_to_gaap():
    pages = ["1. 본문이다.\nBC1 이 줄은 GAAP에서 문단이 아니다.\n"]
    paras = parse_pages(pages, "gaap_15")
    assert all(not p["no"].startswith("BC") for p in paras)


def test_wrapped_heading_is_joined():
    # "…지정할 수 있는 선" + "택권" → 한 소제목으로 복원 (1109 실측 패턴)
    pages = [
        "4.1.4 그 밖의 금융자산은 공정가치로 측정하며 선택을 취소할 수 없다(문단\n"
        "5.7.5~5.7.6).\n"
        "금융자산을 당기손익-공정가치 측정 항목으로 지정할 수 있는 선\n"
        "택권\n"
        "4.1.5 서로 다른 기준에 따라 자산이나 부채를 측정하는 경우가 있다.\n"
    ]
    paras = _by_no(parse_pages(pages, "1109"))
    assert (
        paras["4.1.5"]["section"]
        == "금융자산을 당기손익-공정가치 측정 항목으로 지정할 수 있는 선택권"
    )
    # 앞 문단 본문에서 소제목 앞줄이 제거됨
    assert "지정할 수 있는 선" not in paras["4.1.4"]["body"]


def test_body_wrap_fragment_not_heading():
    # 정의문 마지막 wrap 조각 "는 금융상품"이 소제목으로 오탐되지 않음 (1032 실측 패턴)
    pages = [
        "11 다음 용어의 정의는 이 기준서와 같다. 풋가능 금융상품은 보유자가 발행자에게 환매를 요구할 권리가 부여\n"
        "된 금융상품이나 불확실한 미래 사건이 일어나면 발행자에게 자동으로 환매되\n"
        "는 금융상품\n"
        "12 다음 용어는 부록에서 정의한 의미로 사용한다.\n"
    ]
    paras = _by_no(parse_pages(pages, "1032"))
    assert paras["12"]["section"] != "는 금융상품"
    assert "는 금융상품" in paras["11"]["body"]


def test_full_width_midsentence_fragment_not_heading():
    # 전폭 wrap + 문장 미종결 뒤의 조각 오탐 차단 (1001 "체 분류한 …" 실측 패턴)
    pages = [
        "한138.4 명칭을 사용하여 주석으로 공시할 수 있으며 이 경우 다음 내용을 포함한다.\n"
        "⑵ 이러한 조정영업이익 등은 해당 기업이 스스로 판단하여 자율적으로 자\n"
        "체 분류한 영업이익이라는 사실\n"
        "한138.5 발행자의 주가 변동에 따라 행사가격이 조정되는 조건이 있는 금융상품.\n"
    ]
    paras = _by_no(parse_pages(pages, "1001"))
    assert paras["한138.5"]["section"] != "체 분류한 영업이익이라는 사실"


def test_normal_single_line_heading_still_works():
    pages = [
        "15 발행자는 금융상품을 분류한다.\n"
        "풋가능 금융상품\n"
        "16 풋가능 금융상품은 지분상품으로 분류한다.\n"
    ]
    paras = _by_no(parse_pages(pages, "1032"))
    assert paras["16"]["section"] == "풋가능 금융상품"
