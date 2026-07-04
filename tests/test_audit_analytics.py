"""AP2 tests for synthetic audit analytical procedure metrics."""

import pytest

from kifrs.workflows.audit_analytics import SYNTHETIC_FS, calculate_metrics
from kifrs.workflows.audit_analytics.schema import AnalyticalProcedureInput


def _metric(metric_id: str):
    metrics = calculate_metrics(SYNTHETIC_FS)
    return next(metric for metric in metrics if metric.metric_id == metric_id)


def test_calculate_line_item_change_metrics():
    revenue = _metric("line:수익")

    assert revenue.current_value == 2_100_000
    assert revenue.prior_value == 1_500_000
    assert revenue.change_amount == 600_000
    assert revenue.change_pct == pytest.approx(0.4)


def test_calculate_core_profitability_and_liquidity_ratios():
    gross_margin = _metric("ratio:gross_margin")
    operating_margin = _metric("ratio:operating_margin")
    current_ratio = _metric("ratio:current_ratio")

    assert gross_margin.current_value == pytest.approx(580_000 / 2_100_000)
    assert gross_margin.prior_value == pytest.approx(520_000 / 1_500_000)
    assert operating_margin.current_value == pytest.approx(150_000 / 2_100_000)
    assert current_ratio.current_value == pytest.approx(810_000 / 450_000)


def test_calculate_debt_to_equity_ratio_change():
    debt_to_equity = _metric("ratio:debt_to_equity")

    assert debt_to_equity.current_value == pytest.approx(1_020_000 / 880_000)
    assert debt_to_equity.prior_value == pytest.approx(700_000 / 900_000)
    assert debt_to_equity.change_amount is not None
    assert debt_to_equity.change_amount > 0


def test_requires_at_least_two_periods():
    source = AnalyticalProcedureInput(entity="x", periods=["20x2"], lines=[])

    with pytest.raises(ValueError):
        calculate_metrics(source)
