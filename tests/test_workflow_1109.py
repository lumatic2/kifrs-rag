"""WA1 unit tests — kifrs/workflows/kifrs1109/* (docs/plans/2026-07-03-wa1-1109-pilot-engine.md)."""
from __future__ import annotations

import pytest

from kifrs.workflows.kifrs1109.schema import (
    BusinessModelEvidence,
    PeriodObservation,
    Transaction1109,
)
from kifrs.workflows.kifrs1109.amortization import (
    amortize_ac_or_fvoci_debt,
    revalue_fvpl_or_fvoci_equity,
)
from kifrs.workflows.kifrs1109.business_model import classify_business_model
from kifrs.workflows.kifrs1109.classify import NeedsHumanReview, classify
from kifrs.workflows.kifrs1109.initial_entry import initial_recognition_entry
from kifrs.workflows.kifrs1109.review_memo import SECTION_TITLES, generate_review_memo
from kifrs.workflows.kifrs1109.sppi import classify_sppi
from kifrs.workflows.kifrs1109.subsequent_entry import (
    subsequent_entries_ac_or_fvoci_debt,
    subsequent_entries_fvpl_or_fvoci_equity,
)


def test_transaction_schema_constructs_minimal_debt_instrument():
    txn = Transaction1109(
        label="scenario_01",
        instrument_type="debt",
        principal=1_000_000,
        coupon_type="fixed",
        coupon_rate=0.06,
        maturity_years=5,
        acceleration_ordinary=True,
        business_model=BusinessModelEvidence(
            sale_frequency="rare",
            performance_basis="interest_ecl",
        ),
        purchase_price=921_432,
        transaction_cost=9_000,
        assumed_eir=0.08,
        periods=[PeriodObservation(label="20x1.12.31", coupon_cash=60_000)],
    )
    assert txn.instrument_type == "debt"
    assert txn.business_model.sale_frequency == "rare"
    assert txn.periods[0].coupon_cash == 60_000


def test_transaction_schema_equity_defaults():
    txn = Transaction1109(
        label="scenario_04",
        instrument_type="equity",
        held_for_trading=False,
        fvoci_irrevocable_election=True,
        purchase_price=50_000_000,
        transaction_cost=125_000,
    )
    assert txn.principal is None
    assert txn.fvoci_irrevocable_election is True


def test_sppi_pass_plain_fixed_bond():
    txn = Transaction1109(label="scenario_01", instrument_type="debt", coupon_type="fixed")
    result = classify_sppi(txn)
    assert result.passed is True


def test_sppi_fail_third_party_credit_linkage():
    txn = Transaction1109(
        label="scenario_03", instrument_type="debt", third_party_credit_linkage=True,
    )
    result = classify_sppi(txn)
    assert result.passed is False


def test_sppi_fail_holder_side_conversion_option():
    txn = Transaction1109(
        label="scenario_07", instrument_type="debt",
        embedded_conversion_option_holder_side=True,
    )
    result = classify_sppi(txn)
    assert result.passed is False


def test_sppi_rejects_equity_instrument():
    txn = Transaction1109(label="scenario_04", instrument_type="equity")
    with pytest.raises(ValueError):
        classify_sppi(txn)


def test_business_model_1_hold_to_collect():
    ev = BusinessModelEvidence(sale_frequency="rare", performance_basis="interest_ecl")
    assert classify_business_model(ev).model == 1


def test_business_model_2_collect_and_sell():
    ev = BusinessModelEvidence(sale_frequency="moderate", performance_basis="fv_mixed")
    assert classify_business_model(ev).model == 2


def test_business_model_3_trading():
    ev = BusinessModelEvidence(sale_frequency="frequent", performance_basis="fv_trading",
                                compensation_trading_linked=True)
    assert classify_business_model(ev).model == 3


def test_scenario_01_ac_classification_and_initial_entry():
    txn = Transaction1109(
        label="scenario_01", instrument_type="debt", coupon_type="fixed", coupon_rate=0.06,
        acceleration_ordinary=True,
        business_model=BusinessModelEvidence(sale_frequency="rare", performance_basis="interest_ecl"),
        purchase_price=921_432, transaction_cost=9_000,
    )
    result = classify(txn)
    assert result.classification == "AC"
    entry = initial_recognition_entry(txn, result.classification)
    assert entry.total_debit == entry.total_credit == 930_432
    assert entry.lines[0].account == "AC금융자산"


def test_scenario_02_fvoci_debt_classification_and_initial_entry():
    txn = Transaction1109(
        label="scenario_02", instrument_type="debt", coupon_type="fixed", coupon_rate=0.07,
        business_model=BusinessModelEvidence(sale_frequency="moderate", performance_basis="fv_mixed"),
        purchase_price=1_895_000, transaction_cost=15_000,
    )
    result = classify(txn)
    assert result.classification == "FVOCI_DEBT"
    entry = initial_recognition_entry(txn, result.classification)
    assert entry.total_debit == entry.total_credit == 1_910_000


def test_scenario_03_fvpl_via_sppi_fail_credit_linked_note():
    txn = Transaction1109(
        label="scenario_03", instrument_type="debt", third_party_credit_linkage=True,
        purchase_price=500_000, transaction_cost=2_500,
    )
    result = classify(txn)
    assert result.classification == "FVPL"
    entry = initial_recognition_entry(txn, result.classification)
    assert entry.total_debit == entry.total_credit == 502_500
    # FVPL expenses transaction cost immediately -- must appear as its own line, not capitalized
    assert any(line.account == "수수료비용" and line.debit == 2_500 for line in entry.lines)
    assert any(line.account == "FVPL금융자산" and line.debit == 500_000 for line in entry.lines)


def test_scenario_04_fvoci_equity_classification_and_initial_entry():
    txn = Transaction1109(
        label="scenario_04", instrument_type="equity", held_for_trading=False,
        fvoci_irrevocable_election=True, purchase_price=50_000_000, transaction_cost=125_000,
    )
    result = classify(txn)
    assert result.classification == "FVOCI_EQUITY"
    entry = initial_recognition_entry(txn, result.classification)
    assert entry.total_debit == entry.total_credit == 50_125_000


def test_scenario_09_fvpl_via_designation_override():
    txn = Transaction1109(
        label="scenario_09", instrument_type="debt", coupon_type="fixed",
        business_model=BusinessModelEvidence(sale_frequency="rare", performance_basis="interest_ecl"),
        fvpl_designation_override=True,
        purchase_price=1_895_000, transaction_cost=15_000,
    )
    result = classify(txn)
    assert result.classification == "FVPL"
    entry = initial_recognition_entry(txn, result.classification)
    assert entry.total_debit == entry.total_credit == 1_910_000
    assert any(line.account == "수수료비용" and line.debit == 15_000 for line in entry.lines)


def test_classify_raises_needs_human_review_for_special_case():
    txn = Transaction1109(
        label="scenario_05", instrument_type="debt", special_case="ifric19_debt_equity_swap",
    )
    with pytest.raises(NeedsHumanReview):
        classify(txn)


def test_scenario_01_amortization_table_matches_source():
    txn = Transaction1109(
        label="scenario_01", instrument_type="debt",
        purchase_price=921_432, transaction_cost=9_000, assumed_eir=0.08,
        periods=[PeriodObservation(label=f"y{i}", coupon_cash=60_000) for i in range(1, 6)],
    )
    rows = amortize_ac_or_fvoci_debt(txn, "AC")
    expected_closing = [944_867, 960_456, 977_292, 995_475, 1_015_113]
    expected_amort = [14_435, 15_589, 16_836, 18_183, 19_638]
    assert [r.closing_ac_bv for r in rows] == expected_closing
    assert [r.amortization for r in rows] == expected_amort
    assert rows[0].opening_bv == 930_432


def test_scenario_02_fvoci_amortization_and_oci_matches_source():
    txn = Transaction1109(
        label="scenario_02", instrument_type="debt",
        purchase_price=1_895_000, transaction_cost=15_000, assumed_eir=0.08,
        periods=[
            PeriodObservation(label="y1", coupon_cash=140_000, period_end_fair_value=1_950_000),
            PeriodObservation(label="y2", coupon_cash=140_000, period_end_fair_value=1_945_000),
            PeriodObservation(label="y3", coupon_cash=140_000, period_end_fair_value=1_960_000),
        ],
    )
    rows = amortize_ac_or_fvoci_debt(txn, "FVOCI_DEBT")
    assert [r.closing_ac_bv for r in rows] == [1_922_800, 1_936_624, 1_951_554]
    assert [r.oci_cumulative for r in rows] == [27_200, 8_376, 8_446]
    assert rows[0].oci_delta == 27_200
    assert rows[1].oci_delta == -18_824


def test_scenario_03_fvpl_revaluation_matches_source():
    txn = Transaction1109(
        label="scenario_03", instrument_type="debt", third_party_credit_linkage=True,
        purchase_price=500_000, transaction_cost=2_500,
        periods=[
            PeriodObservation(label="y1", coupon_cash=45_000, period_end_fair_value=480_000),
            PeriodObservation(label="y2", coupon_cash=40_000, period_end_fair_value=460_000),
        ],
    )
    rows = revalue_fvpl_or_fvoci_equity(txn, "FVPL")
    assert [r.fv_delta for r in rows] == [-20_000, -20_000]


def test_scenario_01_subsequent_entries_balance_and_match_interest():
    txn = Transaction1109(
        label="scenario_01", instrument_type="debt",
        purchase_price=921_432, transaction_cost=9_000, assumed_eir=0.08,
        periods=[PeriodObservation(label="y1", coupon_cash=60_000)],
    )
    rows = amortize_ac_or_fvoci_debt(txn, "AC")
    entries = subsequent_entries_ac_or_fvoci_debt(txn.label, "AC", rows)
    assert len(entries) == 1  # AC has no OCI entry
    entry = entries[0]
    assert entry.total_debit == entry.total_credit
    assert any(line.account == "이자수익" and line.credit == 74_435 for line in entry.lines)
    assert any(line.account == "AC금융자산" and line.debit == 14_435 for line in entry.lines)


def test_scenario_02_subsequent_entries_include_oci_adjustment():
    txn = Transaction1109(
        label="scenario_02", instrument_type="debt",
        purchase_price=1_895_000, transaction_cost=15_000, assumed_eir=0.08,
        periods=[
            PeriodObservation(label="y1", coupon_cash=140_000, period_end_fair_value=1_950_000),
            PeriodObservation(label="y2", coupon_cash=140_000, period_end_fair_value=1_945_000),
        ],
    )
    rows = amortize_ac_or_fvoci_debt(txn, "FVOCI_DEBT")
    entries = subsequent_entries_ac_or_fvoci_debt(txn.label, "FVOCI_DEBT", rows)
    assert len(entries) == 4  # 2 periods x (interest + OCI)
    y1_oci, y2_oci = entries[1], entries[3]
    assert all(e.total_debit == e.total_credit for e in entries)
    assert any(line.account == "평가이익(OCI)" and line.credit == 27_200 for line in y1_oci.lines)
    assert any(line.account == "평가손실(OCI)" and line.debit == 18_824 for line in y2_oci.lines)


def test_scenario_03_fvpl_subsequent_entries_match_source_loss():
    txn = Transaction1109(
        label="scenario_03", instrument_type="debt", third_party_credit_linkage=True,
        purchase_price=500_000, transaction_cost=2_500,
        periods=[PeriodObservation(label="y1", coupon_cash=45_000, period_end_fair_value=480_000)],
    )
    rows = revalue_fvpl_or_fvoci_equity(txn, "FVPL")
    entries = subsequent_entries_fvpl_or_fvoci_equity(txn.label, "FVPL", rows)
    assert len(entries) == 2  # interest + revaluation
    interest_entry, revaluation_entry = entries
    assert any(line.account == "이자수익" and line.credit == 45_000 for line in interest_entry.lines)
    assert any(line.account == "평가손실(PL)" and line.debit == 20_000 for line in revaluation_entry.lines)
    assert all(e.total_debit == e.total_credit for e in entries)


def test_review_memo_contains_all_7_sections_and_classification():
    txn = Transaction1109(
        label="scenario_01", instrument_type="debt",
        business_model=BusinessModelEvidence(sale_frequency="rare", performance_basis="interest_ecl"),
        purchase_price=921_432, transaction_cost=9_000, assumed_eir=0.08,
        periods=[PeriodObservation(label="y1", coupon_cash=60_000)],
    )
    result = classify(txn)
    entry = initial_recognition_entry(txn, result.classification)
    rows = amortize_ac_or_fvoci_debt(txn, result.classification)
    memo = generate_review_memo(txn, result, entry, rows)
    assert len(SECTION_TITLES) == 7
    for i, title in enumerate(SECTION_TITLES, start=1):
        assert f"## {i}. {title}" in memo
    assert "AC" in memo
    assert "930,432" in memo
