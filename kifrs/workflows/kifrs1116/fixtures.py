"""1116 회귀 fixture — `data/scenarios/1116_lease/scenario_*`(gitignored, local-only 시나리오
문서)를 Step 1 스키마로 수동 전사(AE1 Step 2).

여기 담긴 숫자는 시나리오 작성 시 사용자가 만든 연습용 거래(사무실 임차·리스제공자 계약 등)이지
K-IFRS 기준서 원문이나 학원 문제 원문이 아니다. `data/` 전체는 gitignore 대상이라 회귀 테스트를
그 아래 두면 CI/새 clone에서 못 돈다 — 그래서 패키지 안에 둔다. 원본 시나리오 문서(거래 배경
서술, textbook 문제 인용 등)는 여전히 `data/scenarios/`에만 있고 git에 올라가지 않는다 —
여기엔 측정·분개 결정에 필요한 수치·판정만 옮긴다.

할인율 현가계수(annuity_factor·single_factor)는 시나리오가 제시한 값 그대로다(엔진은 수치해석을
하지 않는다 — schema.py 참조). `special_case`가 있는 1개(scenario_09)는 동시 확장+축소 변경으로
[1116-46(a)]/[1116-46(b)] 2차원 분해가 필요해 AE1 core pipeline 밖 — NeedsHumanReview 기대.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .schema import ExemptionCase, Lease1116, LeaseEvent

# 현가계수 (시나리오 제시값)
ANNUITY_5_4 = 3.54595
SINGLE_5_4 = 0.82270
ANNUITY_5_3 = 2.72325
ANNUITY_6_4 = 3.46511


@dataclass
class ScenarioFixture:
    txn: Lease1116
    # 기대 headline (None이면 NeedsHumanReview 기대)
    expected: dict[str, Any] | None


FIXTURES: list[ScenarioFixture] = [
    # 1 — 단순 사무실 임차 (이용자, 4년·후급·5%)
    ScenarioFixture(
        txn=Lease1116(
            label="scenario_01_simple_office_lease", party="lessee",
            annual_payment=1_000_000, lease_term_years=4, discount_rate=0.05,
            annuity_factor=ANNUITY_5_4,
        ),
        expected={"lease_liability": 3_545_950, "rou_asset": 3_545_950, "annual_depreciation": 886_488},
    ),
    # 2 — 복구의무 + 선급 + 인센티브 + 개설직접원가 (사용권자산 4구성요소, 1116+1037)
    ScenarioFixture(
        txn=Lease1116(
            label="scenario_02_restoration_prepaid", party="lessee",
            annual_payment=1_000_000, lease_term_years=4, discount_rate=0.05,
            annuity_factor=ANNUITY_5_4,
            prepaid_lease_payment=200_000, lease_incentive_received=100_000,
            initial_direct_costs=50_000,
            restoration_future_estimate=500_000, restoration_factor=SINGLE_5_4,
        ),
        expected={
            "lease_liability": 3_545_950, "rou_asset": 4_107_300,
            "restoration_provision": 411_350, "annual_depreciation": 1_026_825,
        },
    ),
    # 3 — 단기·소액 면제 (이용자, 두 케이스)
    ScenarioFixture(
        txn=Lease1116(
            label="scenario_03_short_low_value_exemption", party="lessee",
            exemption_cases=[
                ExemptionCase(label="case_a", monthly_payment=300_000, months=12, basis="short_term"),
                ExemptionCase(label="case_b", monthly_payment=40_000, months=24, basis="low_value"),
            ],
        ),
        expected={
            "case_a_annual_expense": 3_600_000, "case_b_annual_expense": 480_000,
            "case_b_total_expense": 960_000,
        },
    ),
    # 4 — 제공자 금융→운용 변경 (10%, 잔존 100,000)
    ScenarioFixture(
        txn=Lease1116(
            label="scenario_04_lessor_finance_to_operating", party="lessor",
            lessor_classification="finance",
            annual_payment=1_000_000, lease_term_years=4, discount_rate=0.10,
            annuity_factor=3.16987,
            lessor_residual_value=100_000, lessor_residual_factor=0.68301,
            events=[LeaseEvent(kind="lessor_finance_to_operating", effective="20x2.1.1", periods_elapsed=1)],
        ),
        expected={
            "net_investment": 3_238_171, "year1_interest_income": 323_817,
            "operating_lease_asset": 2_561_988, "modification_gain_loss": 0,
        },
    ),
    # 5 — 제공자 운용→금융 변경 (textbook ch15 물음1, 모범답안 6/6 검증 재료)
    ScenarioFixture(
        txn=Lease1116(
            label="scenario_05_lessor_op_to_finance", party="lessor",
            lessor_classification="operating",
            annual_payment=1_000_000, lease_term_years=3, discount_rate=0.10,
            asset_cost=3_163_171, asset_useful_life_years=5, lessor_initial_direct_costs=75_000,
            events=[LeaseEvent(
                kind="lessor_operating_to_finance", effective="20x2.1.1", periods_elapsed=1,
                new_rate=0.12, new_remaining_term=3, new_annuity_factor=2.40183,
                new_annual_payment=1_000_000, new_residual=100_000, new_residual_factor=0.71178,
            )],
        ),
        expected={
            "operating_asset_initial": 3_238_171, "year1_depreciation": 657_634,
            "year1_pl_effect": 342_366, "operating_asset_carrying_at_change": 2_580_537,
            "lease_receivable": 2_473_008, "modification_loss": -107_529,
        },
    ),
    # 6 — 제공자 금융→금융 변경 (정기리스료 감소, textbook ch15 물음3)
    ScenarioFixture(
        txn=Lease1116(
            label="scenario_06_lessor_finance_to_finance_payment_change", party="lessor",
            lessor_classification="finance",
            annual_payment=1_000_000, lease_term_years=4, discount_rate=0.10,
            annuity_factor=3.16987,
            lessor_residual_value=100_000, lessor_residual_factor=0.68301,
            events=[LeaseEvent(
                kind="lessor_finance_to_finance", effective="20x2.1.1", periods_elapsed=1,
                new_rate=0.12, new_remaining_term=3, new_annuity_factor=2.40183,
                new_annual_payment=950_000, new_residual=100_000, new_residual_factor=0.71178,
            )],
        ),
        expected={
            "receivable_before_change": 2_561_988, "net_investment_after_change": 2_352_917,
            "modification_loss": -209_071, "year2_interest_income": 282_350,
        },
    ),
    # 7 — 이용자 리스기간 재평가 (갱신 상당히 확실해짐, 5%→6%)
    ScenarioFixture(
        txn=Lease1116(
            label="scenario_07_lessee_term_reassessment", party="lessee",
            annual_payment=1_000_000, lease_term_years=3, discount_rate=0.05,
            annuity_factor=ANNUITY_5_3,
            events=[LeaseEvent(
                kind="term_reassessment", effective="20x2.1.1", periods_elapsed=1,
                new_rate=0.06, new_remaining_term=4, new_annuity_factor=ANNUITY_6_4,
                new_annual_payment=1_000_000,
            )],
        ),
        expected={
            "initial_liability": 2_723_250, "liability_after_elapsed": 1_859_413,
            "rou_after_elapsed": 1_815_500, "remeasured_liability": 3_465_110,
            "remeasurement_increase": 1_605_697, "remeasured_rou": 3_421_197,
        },
    ),
    # 8 — 이용자 매수선택권 행사 거의 확실 (감가 = 내용연수 6년)
    ScenarioFixture(
        txn=Lease1116(
            label="scenario_08_lessee_purchase_option_reasonably_certain", party="lessee",
            annual_payment=1_000_000, lease_term_years=4, discount_rate=0.05,
            annuity_factor=ANNUITY_5_4,
            purchase_option_price=200_000, purchase_option_reasonably_certain=True,
            purchase_option_factor=SINGLE_5_4, asset_useful_life_years=6,
        ),
        expected={"lease_liability": 3_710_490, "rou_asset": 3_710_490, "annual_depreciation": 618_415},
    ),
    # 9 — 이용자 변경: 확장+축소 동시 → AE1 범위 밖 (2차원 분해, NeedsHumanReview)
    ScenarioFixture(
        txn=Lease1116(
            label="scenario_09_lessee_modification_expand_shrink", party="lessee",
            annual_payment=1_000_000, lease_term_years=6, discount_rate=0.07,
            special_case="modification_expand_shrink_two_dimensional",
        ),
        expected=None,
    ),
    # 10 — 이용자 변경: 기간 1년 연장 단독 (7%→8%, 잔여 5년)
    ScenarioFixture(
        txn=Lease1116(
            label="scenario_10_lessee_modification_extend", party="lessee",
            annual_payment=1_000_000, lease_term_years=6, discount_rate=0.07,
            annuity_factor=4.7665,
            events=[LeaseEvent(
                kind="modification_extend", effective="20x3.1.1", periods_elapsed=2,
                new_rate=0.08, new_remaining_term=5, new_annuity_factor=3.9927,
                new_annual_payment=1_000_000,
            )],
        ),
        expected={
            "liability_before_change": 3_387_166, "remeasured_liability": 3_992_700,
            "remeasurement_adjustment": 605_534, "y_end_liability": 3_312_116,
            "y_end_rou": 3_026_561,
        },
    ),
]
