"""1109 회귀 fixture — `data/scenarios/1109_classification/scenario_*`(gitignored, local-only
K-IFRS 시나리오 문서)를 Step 1 스키마로 수동 전사(WA1 Step 2).

여기 담긴 숫자는 시나리오 작성 시 사용자가 창작한 연습용 거래(회사채 매입 등)이지 K-IFRS
기준서 원문이 아니다. `data/` 전체는 gitignore 대상(원문·파싱 DB·임베딩 보호)이라 회귀
테스트가 그 아래 두면 CI/새 clone에서 못 돈다 — 그래서 패키지 안(`kifrs/workflows/kifrs1109/`)에
둔다. 원본 시나리오 문서 자체(거래 배경 서술, 시험 문제 인용 등)는 여전히 `data/scenarios/`에만
있고 git에 올라가지 않는다 — 여기엔 분류·분개 결정에 필요한 사실만 옮긴다.

`special_case`가 있는 4개(05/06/08/10)는 WA1 core pipeline이 자동화하지 않는다
(docs/plans/2026-07-03-wa1-1109-pilot-engine.md 결정 로그 + 실행 중 발견). 나머지 6개
(01/02/03/04/07/09)는 SPPI+사업모형 조합만으로 결정론적으로 분류된다 — 07(보유자 전환사채)과
09(회계불일치 지정)는 계획 당시 "복잡 케이스"로 짐작했으나 구현 중 기존 SPPI-fail/지정 오버라이드
로직으로 그대로 커버됨이 확인되어 core 6개로 승격했다.
"""
from __future__ import annotations

from dataclasses import dataclass

from .schema import BusinessModelEvidence, PeriodObservation, Transaction1109


@dataclass
class ScenarioFixture:
    txn: Transaction1109
    expected_classification: str | None  # None if special_case (NeedsHumanReview expected)
    expected_initial_total: float | None = None


FIXTURES: list[ScenarioFixture] = [
    ScenarioFixture(
        txn=Transaction1109(
            label="scenario_01_corporate_bond_ac", instrument_type="debt",
            coupon_type="fixed", coupon_rate=0.06, maturity_years=5,
            acceleration_ordinary=True,
            business_model=BusinessModelEvidence(sale_frequency="rare", performance_basis="interest_ecl"),
            purchase_price=921_432, transaction_cost=9_000, assumed_eir=0.08,
            periods=[
                PeriodObservation(label="20x1.12.31", coupon_cash=60_000),
                PeriodObservation(label="20x2.12.31", coupon_cash=60_000),
                PeriodObservation(label="20x3.12.31", coupon_cash=60_000),
                PeriodObservation(label="20x4.12.31", coupon_cash=60_000),
                PeriodObservation(label="20x5.12.31", coupon_cash=60_000),
            ],
        ),
        expected_classification="AC", expected_initial_total=930_432,
    ),
    ScenarioFixture(
        txn=Transaction1109(
            label="scenario_02_corporate_bond_fvoci", instrument_type="debt",
            coupon_type="fixed", coupon_rate=0.07, maturity_years=6,
            business_model=BusinessModelEvidence(sale_frequency="moderate", performance_basis="fv_mixed"),
            purchase_price=1_895_000, transaction_cost=15_000, assumed_eir=0.08,
            periods=[
                PeriodObservation(label="20x1.12.31", coupon_cash=140_000, period_end_fair_value=1_950_000),
                PeriodObservation(label="20x2.12.31", coupon_cash=140_000, period_end_fair_value=1_945_000),
                PeriodObservation(label="20x3.12.31", coupon_cash=140_000, period_end_fair_value=1_960_000),
            ],
        ),
        expected_classification="FVOCI_DEBT", expected_initial_total=1_910_000,
    ),
    ScenarioFixture(
        txn=Transaction1109(
            label="scenario_03_credit_linked_note_fvpl", instrument_type="debt",
            coupon_type="floating", maturity_years=3, third_party_credit_linkage=True,
            purchase_price=500_000, transaction_cost=2_500,
            periods=[
                PeriodObservation(label="20x1.12.31", coupon_cash=45_000, period_end_fair_value=480_000),
                PeriodObservation(label="20x2.12.31", coupon_cash=40_000, period_end_fair_value=460_000),
            ],
        ),
        expected_classification="FVPL", expected_initial_total=502_500,
    ),
    ScenarioFixture(
        txn=Transaction1109(
            label="scenario_04_listed_equity_fvoci_irrevocable", instrument_type="equity",
            held_for_trading=False, fvoci_irrevocable_election=True,
            purchase_price=50_000_000, transaction_cost=125_000,
            periods=[
                PeriodObservation(label="20x1.12.31", period_end_fair_value=55_000_000),
                PeriodObservation(label="20x2.12.31", period_end_fair_value=48_000_000),
            ],
        ),
        expected_classification="FVOCI_EQUITY", expected_initial_total=50_125_000,
    ),
    ScenarioFixture(
        txn=Transaction1109(
            label="scenario_05_ifric19_debt_equity_swap", instrument_type="debt",
            special_case="ifric19_debt_equity_swap",
        ),
        expected_classification=None,
    ),
    ScenarioFixture(
        txn=Transaction1109(
            label="scenario_06_floating_rate_bond_sppi_nuance", instrument_type="debt",
            special_case="sppi_reset_mismatch",
        ),
        expected_classification=None,
    ),
    ScenarioFixture(
        txn=Transaction1109(
            label="scenario_07_convertible_bond_holder", instrument_type="debt",
            coupon_type="fixed", coupon_rate=0.05, maturity_years=5,
            embedded_conversion_option_holder_side=True,
            purchase_price=980_000, transaction_cost=5_000,
            periods=[
                PeriodObservation(label="20x1.12.31", coupon_cash=50_000, period_end_fair_value=970_000),
            ],
        ),
        expected_classification="FVPL", expected_initial_total=985_000,
    ),
    ScenarioFixture(
        txn=Transaction1109(
            label="scenario_08_business_model_change_reclassification", instrument_type="debt",
            special_case="reclassification",
        ),
        expected_classification=None,
    ),
    ScenarioFixture(
        txn=Transaction1109(
            label="scenario_09_fvpl_designation_accounting_mismatch", instrument_type="debt",
            coupon_type="fixed",
            business_model=BusinessModelEvidence(sale_frequency="rare", performance_basis="interest_ecl"),
            fvpl_designation_override=True,
            purchase_price=1_895_000, transaction_cost=15_000,
        ),
        expected_classification="FVPL", expected_initial_total=1_910_000,
    ),
    ScenarioFixture(
        txn=Transaction1109(
            label="scenario_10_foreign_currency_bond_1109_1021", instrument_type="debt",
            special_case="fx_dual_track",
        ),
        expected_classification=None,
    ),
]
