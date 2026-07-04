"""Ratio and trend metric calculation for audit analytical procedures."""

from .schema import AnalyticalMetric, AnalyticalProcedureInput, AnomalyFinding


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


def detect_anomalies(metrics: list[AnalyticalMetric]) -> list[AnomalyFinding]:
    """Create review-question findings from deterministic metric thresholds."""
    findings: list[AnomalyFinding] = []
    by_id = {metric.metric_id: metric for metric in metrics}

    for metric in metrics:
        if metric.metric_id.startswith("line:") and metric.change_pct is not None:
            if abs(metric.change_pct) >= 0.5:
                line_item = metric.metric_id.removeprefix("line:")
                findings.append(
                    AnomalyFinding(
                        finding_id=f"line-change:{line_item}",
                        severity="warning",
                        metric_id=metric.metric_id,
                        message=(
                            f"{line_item} 변동률 {metric.change_pct:.1%}: "
                            f"{metric.prior_value:,.0f} -> {metric.current_value:,.0f}"
                        ),
                        review_questions=[
                            f"{line_item} 변동의 주요 원인이 신규 거래, 회계정책 변경, 일회성 항목 중 무엇인지?",
                            f"{line_item} 변동이 관련 주석 또는 회계이슈 memo에 반영되어 있는지?",
                        ],
                        linked_statement_candidates=[line_item],
                    )
                )

    operating_margin = by_id.get("ratio:operating_margin")
    if operating_margin and operating_margin.change_amount is not None and operating_margin.change_amount <= -0.05:
        findings.append(
            AnomalyFinding(
                finding_id="ratio:operating_margin_drop",
                severity="critical",
                metric_id="ratio:operating_margin",
                message=(
                    f"영업이익률 하락 {operating_margin.change_amount:.1%}p: "
                    f"{operating_margin.prior_value:.1%} -> {operating_margin.current_value:.1%}"
                ),
                review_questions=[
                    "수익 증가와 영업이익률 하락이 동시에 발생한 원인은 무엇인지?",
                    "매출원가 또는 판매비와관리비 증가가 계약 조건, 리스, 금융상품 이슈와 연결되는지?",
                ],
                linked_statement_candidates=["수익", "매출원가", "판매비와관리비", "영업이익"],
            )
        )

    debt_to_equity = by_id.get("ratio:debt_to_equity")
    if debt_to_equity and debt_to_equity.change_amount is not None and debt_to_equity.change_amount >= 0.25:
        findings.append(
            AnomalyFinding(
                finding_id="ratio:debt_to_equity_rise",
                severity="warning",
                metric_id="ratio:debt_to_equity",
                message=(
                    f"부채비율 상승 {debt_to_equity.change_amount:.2f}: "
                    f"{debt_to_equity.prior_value:.2f} -> {debt_to_equity.current_value:.2f}"
                ),
                review_questions=[
                    "부채 증가가 리스부채, 금융부채, 계약부채 중 어느 항목과 관련되는지?",
                    "신규 차입 또는 재매입약정 같은 금융요소가 있는지?",
                ],
                linked_statement_candidates=["총부채", "자본총계", "리스부채", "금융부채", "계약부채"],
            )
        )

    return findings


def render_anomaly_note(entity: str, findings: list[AnomalyFinding]) -> str:
    """Render findings into a workpaper-style analytical procedure note."""
    lines = [
        f"# 분석적 절차 이상징후 메모 — {entity}",
        "",
        f"- finding 수: {len(findings)}",
        "- 범위: synthetic F/S fixture 기반 계산 초안",
        "- 경계: 감사결론, 중요성, 표본설계, KAM 판단은 포함하지 않음",
        "",
        "## Findings",
    ]
    if not findings:
        lines.append("- threshold를 초과한 이상징후 없음")
        return "\n".join(lines)

    for finding in findings:
        lines.append(f"### {finding.finding_id} [{finding.severity}]")
        lines.append(f"- metric: {finding.metric_id}")
        lines.append(f"- 요약: {finding.message}")
        if finding.linked_statement_candidates:
            lines.append("- 연결 후보:")
            lines.extend(f"  - {item}" for item in finding.linked_statement_candidates)
        if finding.review_questions:
            lines.append("- 리뷰 질문:")
            lines.extend(f"  - {question}" for question in finding.review_questions)
    return "\n".join(lines)


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
