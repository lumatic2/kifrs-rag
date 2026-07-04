"""Ratio and trend metric calculation for audit analytical procedures."""

from .schema import AnalyticalMetric, AnalyticalProcedureInput


def calculate_metrics(source: AnalyticalProcedureInput) -> list[AnalyticalMetric]:
    """Calculate deterministic line-item changes and core ratios for the last two periods."""
    if len(source.periods) < 2:
        raise ValueError("analytical procedures require at least two periods")

    prior_period, current_period = source.periods[-2], source.periods[-1]
    metrics: list[AnalyticalMetric] = []

    line_items = sorted({line.line_item for line in source.lines})
    for line_item in line_items:
        prior = _amount(source, prior_period, line_item)
        current = _amount(source, current_period, line_item)
        if prior is None or current is None:
            continue
        metrics.append(
            _metric(
                metric_id=f"line:{line_item}",
                label=f"{line_item} 증감",
                current=current,
                prior=prior,
            )
        )

    ratio_specs = [
        ("ratio:gross_margin", "매출총이익률", "매출총이익", "수익"),
        ("ratio:operating_margin", "영업이익률", "영업이익", "수익"),
        ("ratio:current_ratio", "유동비율", "유동자산", "유동부채"),
        ("ratio:debt_to_equity", "부채비율", "총부채", "자본총계"),
    ]
    for metric_id, label, numerator, denominator in ratio_specs:
        prior = _ratio(source, prior_period, numerator, denominator)
        current = _ratio(source, current_period, numerator, denominator)
        if prior is None or current is None:
            continue
        metrics.append(_metric(metric_id=metric_id, label=label, current=current, prior=prior))

    return metrics


def _amount(source: AnalyticalProcedureInput, period: str, line_item: str) -> float | None:
    for line in source.lines:
        if line.period == period and line.line_item == line_item:
            return line.amount
    return None


def _ratio(
    source: AnalyticalProcedureInput, period: str, numerator: str, denominator: str
) -> float | None:
    num = _amount(source, period, numerator)
    den = _amount(source, period, denominator)
    if num is None or den in (None, 0):
        return None
    return num / den


def _metric(metric_id: str, label: str, current: float, prior: float) -> AnalyticalMetric:
    change = current - prior
    change_pct = None if prior == 0 else change / prior
    return AnalyticalMetric(
        metric_id=metric_id,
        label=label,
        current_value=current,
        prior_value=prior,
        change_amount=change,
        change_pct=change_pct,
    )
