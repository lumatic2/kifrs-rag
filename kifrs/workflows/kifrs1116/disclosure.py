"""1116 리스이용자 주석(공시) 초안 생성 (AE2).

[1116-53] 10개 요구항목 + [1116-58] 리스부채 만기분석을 구조화 체크리스트로 두고, AE1 리스
엔진의 이용자 시나리오 산출물(감가·이자·단기저가 비용·사용권자산·만기)을 각 항목에 매핑해
markdown 리스 주석 초안을 생성한다. 파일럿 엔티티 = AE1 이용자 시나리오를 한 회사의 리스
포트폴리오로 묶어 첫 보고기간(리스개시 후 1년) 기준으로 집계.

요구항목 중 포트폴리오에 해당 거래가 없는 항목(변동리스료·전대리스·판매후리스)은 "미해당"으로
정직하게 표시한다 — 커버리지 위장(optimistic-path) 금지. 각 요구항목의 근거 조항([1116-x])은
grounding으로 DB 존재 검증한다.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .amortization import amortize
from .classify import classify_path, exemption_expenses
from .grounding import ground_reasons
from .measurement import measure_lessee
from .money import won
from .schema import Lease1116

# 만기분석 버킷 (리스개시 후 1년 = 보고일 기준) — 다음 지급까지 남은 연수로 배치
MATURITY_BUCKETS = ["1년 이내", "1~2년", "2~3년", "3~4년", "4~5년", "5년 초과"]


@dataclass
class DisclosureRequirement:
    """[1116-53]/[58] 요구항목 1개."""

    item: str          # 예: "53(1)"
    label: str
    citation: str      # 예: "[1116-53]"
    fillable: bool     # AE1 엔진 산출물로 자동 채울 수 있는가(포트폴리오에 원천 거래 유무와 무관한 구조 판정)


LESSEE_DISCLOSURE_REQUIREMENTS: list[DisclosureRequirement] = [
    DisclosureRequirement("53(1)", "기초자산 유형별 사용권자산의 감가상각비", "[1116-53]", True),
    DisclosureRequirement("53(2)", "리스부채에 대한 이자비용", "[1116-53]", True),
    DisclosureRequirement("53(3)", "단기리스 관련 비용", "[1116-53]", True),
    DisclosureRequirement("53(4)", "소액자산 리스 관련 비용", "[1116-53]", True),
    DisclosureRequirement("53(5)", "리스부채에 포함되지 않은 변동리스료 비용", "[1116-53]", False),
    DisclosureRequirement("53(6)", "사용권자산의 전대리스에서 생기는 수익", "[1116-53]", False),
    DisclosureRequirement("53(7)", "리스의 총 현금유출", "[1116-53]", True),
    DisclosureRequirement("53(8)", "사용권자산의 추가", "[1116-53]", True),
    DisclosureRequirement("53(9)", "판매후리스 거래에서 생기는 차손익", "[1116-53]", False),
    DisclosureRequirement("53(10)", "기초자산 유형별 사용권자산의 기말 장부금액", "[1116-53]", True),
    DisclosureRequirement("58", "리스부채 만기분석", "[1116-58]", True),
]

# 요구항목 item → 집계 필드 (fillable=True 항목만)
_ITEM_TO_FIELD = {
    "53(1)": "depreciation",
    "53(2)": "interest",
    "53(3)": "short_term_expense",
    "53(4)": "low_value_expense",
    "53(7)": "cash_outflow",
    "53(8)": "rou_addition",
    "53(10)": "rou_year_end",
}


@dataclass
class LeaseDisclosureContribution:
    """리스 1건이 첫 보고기간 주석에 기여하는 금액."""

    label: str
    depreciation: int = 0
    interest: int = 0
    short_term_expense: int = 0
    low_value_expense: int = 0
    cash_outflow: int = 0
    rou_addition: int = 0
    rou_year_end: int = 0
    maturity: dict[str, int] = field(default_factory=dict)


def _maturity_bucket(years_from_report: int) -> str:
    idx = min(years_from_report, len(MATURITY_BUCKETS))
    return MATURITY_BUCKETS[idx - 1]


def lease_contribution(lease: Lease1116) -> LeaseDisclosureContribution:
    """이용자 리스 1건의 첫 보고기간(개시 후 1년) 주석 기여분 계산."""
    if lease.party != "lessee":
        raise ValueError(f"{lease.label}: 이용자 주석 파일럿은 리스이용자만")

    path = classify_path(lease)
    contrib = LeaseDisclosureContribution(label=lease.label)

    if path.path == "lessee_exemption":
        for exp in exemption_expenses(lease.exemption_cases):
            if exp.basis == "short_term":
                contrib.short_term_expense += won(exp.annual_expense)
            else:
                contrib.low_value_expense += won(exp.annual_expense)
            contrib.cash_outflow += won(exp.annual_expense)
        return contrib

    m = measure_lessee(lease)
    contrib.depreciation = m.annual_depreciation
    contrib.interest = amortize(m.lease_liability, lease.discount_rate, lease.annual_payment, 1)[0].interest
    contrib.cash_outflow = won(lease.annual_payment)
    contrib.rou_addition = m.rou_asset
    contrib.rou_year_end = m.rou_asset - m.annual_depreciation

    # 만기분석: 개시 후 1년 기준, 남은 리스료를 연도 버킷에 배치
    remaining = (lease.lease_term_years or 0) - 1
    for k in range(1, remaining + 1):
        bucket = _maturity_bucket(k)
        contrib.maturity[bucket] = contrib.maturity.get(bucket, 0) + won(lease.annual_payment)
    # 마지막 리스료 시점에 상당히 확실한 매수선택권 행사가 포함
    if lease.purchase_option_reasonably_certain and lease.purchase_option_price and remaining >= 1:
        bucket = _maturity_bucket(remaining)
        contrib.maturity[bucket] = contrib.maturity.get(bucket, 0) + won(lease.purchase_option_price)
    return contrib


@dataclass
class PortfolioDisclosure:
    depreciation: int = 0
    interest: int = 0
    short_term_expense: int = 0
    low_value_expense: int = 0
    cash_outflow: int = 0
    rou_addition: int = 0
    rou_year_end: int = 0
    maturity: dict[str, int] = field(default_factory=dict)
    contributions: list[LeaseDisclosureContribution] = field(default_factory=list)


def aggregate_portfolio(leases: list[Lease1116]) -> PortfolioDisclosure:
    """이용자 리스 포트폴리오의 첫 보고기간 주석 금액 집계."""
    port = PortfolioDisclosure()
    for lease in leases:
        c = lease_contribution(lease)
        port.contributions.append(c)
        port.depreciation += c.depreciation
        port.interest += c.interest
        port.short_term_expense += c.short_term_expense
        port.low_value_expense += c.low_value_expense
        port.cash_outflow += c.cash_outflow
        port.rou_addition += c.rou_addition
        port.rou_year_end += c.rou_year_end
        for bucket, amt in c.maturity.items():
            port.maturity[bucket] = port.maturity.get(bucket, 0) + amt
    return port


@dataclass
class CoverageResult:
    total: int
    auto_filled: list[str]      # 엔진이 정량 산출하는 요구항목 id
    needs_human: list[str]      # 별도 정보·모델 필요(변동리스료·전대·판매후리스)

    @property
    def coverage_pct(self) -> float:
        return round(100 * len(self.auto_filled) / self.total, 1)


def compute_coverage() -> CoverageResult:
    """[1116-53]+[58] 요구항목 중 AE1 엔진이 정량 산출하는 비율."""
    auto = [r.item for r in LESSEE_DISCLOSURE_REQUIREMENTS if r.fillable]
    human = [r.item for r in LESSEE_DISCLOSURE_REQUIREMENTS if not r.fillable]
    return CoverageResult(total=len(LESSEE_DISCLOSURE_REQUIREMENTS), auto_filled=auto, needs_human=human)


@dataclass
class CrossCheckResult:
    """엔진 자동 커버리지 vs DART 실제 공시 교차검증."""

    universal_items: list[str]        # DART 전사가 공시하는 항목
    conditional_items: list[str]      # 일부 회사만 공시(거래 유무 종속)
    engine_covers_universal: bool     # 엔진 자동 항목이 보편 항목을 모두 포함하는가


# item id → DART 요약 태그 키 (요약 JSON은 "53(1) 감가상각비" 형태 라벨을 씀)
def _summary_key_for(item: str, sample_keys: list[str]) -> str | None:
    for k in sample_keys:
        if k.startswith(item):
            return k
    return None


def cross_check_coverage(dart_summary: list[dict]) -> CrossCheckResult:
    """DART 요약(회사별 항목 존재)과 엔진 자동 커버리지를 대사한다.

    보편 항목 = 모든 회사가 공시 / 조건부 항목 = 일부만. 엔진 자동 항목(fillable=True)이 보편
    항목을 모두 포함하면 "엔진이 보편 공시를 커버"로 판정(조건부 항목만 사람 필요라는 설계 검증).
    """
    if not dart_summary:
        raise ValueError("dart_summary가 비어 있음 — Step 4 fetch 선행 필요")
    sample_keys = list(dart_summary[0]["items"].keys())
    engine_auto = {r.item for r in LESSEE_DISCLOSURE_REQUIREMENTS if r.fillable}

    universal, conditional = [], []
    for req in LESSEE_DISCLOSURE_REQUIREMENTS:
        key = _summary_key_for(req.item, sample_keys)
        if key is None:
            continue
        presence = [c["items"][key] for c in dart_summary]
        if all(presence):
            universal.append(req.item)
        elif any(presence):
            conditional.append(req.item)
    engine_covers_universal = set(universal).issubset(engine_auto)
    return CrossCheckResult(
        universal_items=universal, conditional_items=conditional,
        engine_covers_universal=engine_covers_universal,
    )


def ground_requirements() -> None:
    """모든 요구항목의 근거 조항이 DB에 존재하는지 검증(RGA1). 실패 시 GroundingFailure."""
    ground_reasons([f"{r.label} {r.citation}" for r in LESSEE_DISCLOSURE_REQUIREMENTS])


def generate_disclosure_note(port: PortfolioDisclosure) -> str:
    """포트폴리오 집계 → markdown 리스이용자 주석 초안([1116-54] 표 형식)."""
    md: list[str] = ["# 리스 주석 (리스이용자) — 초안", ""]
    md.append("> AE1 리스 엔진 자동 산출. 회사 특수 서술(리스 정책·판단·추정)은 사람이 보완.")
    md.append("")

    md.append("## 1. 당기손익 인식 금액 [1116-53]")
    md.append("| 요구항목 | 금액 | 근거 |")
    md.append("|---|---:|---|")
    rows = [
        ("(1) 사용권자산 감가상각비", port.depreciation, "[1116-53]"),
        ("(2) 리스부채 이자비용", port.interest, "[1116-53]"),
        ("(3) 단기리스 비용", port.short_term_expense, "[1116-53]"),
        ("(4) 소액자산 리스 비용", port.low_value_expense, "[1116-53]"),
        ("(5) 변동리스료 비용", None, "[1116-53]"),
        ("(6) 전대리스 수익", None, "[1116-53]"),
        ("(7) 리스 총 현금유출", port.cash_outflow, "[1116-53]"),
        ("(8) 사용권자산 추가", port.rou_addition, "[1116-53]"),
        ("(9) 판매후리스 차손익", None, "[1116-53]"),
        ("(10) 사용권자산 기말 장부금액", port.rou_year_end, "[1116-53]"),
    ]
    for label, amount, cite in rows:
        val = "미해당" if amount is None else f"{amount:,.0f}"
        md.append(f"| {label} | {val} | {cite} |")
    md.append("")
    md.append("> (5)·(6)·(9)는 포트폴리오에 해당 거래(변동리스료·전대·판매후리스)가 없어 미해당 — "
              "실제 회사에 해당 거래가 있으면 사람 보완 필요.")
    md.append("")

    md.append("## 2. 리스부채 만기분석 [1116-58]")
    md.append("| 구간 | 리스료(할인 전) |")
    md.append("|---|---:|")
    for bucket in MATURITY_BUCKETS:
        if bucket in port.maturity:
            md.append(f"| {bucket} | {port.maturity[bucket]:,.0f} |")
    total_maturity = sum(port.maturity.values())
    md.append(f"| **합계** | **{total_maturity:,.0f}** |")
    md.append("")

    md.append("## 3. 근거 조항")
    md.append("- [1116-53] 이용자 당기손익·현금흐름 공시 요구항목")
    md.append("- [1116-54] 표 형식 공시")
    md.append("- [1116-58] 리스부채 만기분석 ([1107-39·B11] 준용)")
    return "\n".join(md)
