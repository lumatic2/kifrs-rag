# AP1 Analytical Procedure Scope and Fixture Inventory

> Date: 2026-07-05
> Horizon: `f-audit-analytical-procedures`
> Step: AP1 — analytical procedure scope and fixture inventory
> Inputs: `docs/practice-map/team-workflows.md`, `docs/reports/2026-07-05-fs5-statement-draft-report.md`

## 결론

첫 감사 분석적 절차 PoC는 **synthetic F/S fixture**로 시작한다. DART 공개 F/S는 좋은 후속 검증 source지만
API key, 공시 파싱, 회사별 계정명 정규화 문제가 동시에 열린다. AP2~AP4의 핵심은 외부 수집이 아니라
"기간별 F/S 숫자를 넣으면 계산표와 이상징후 메모가 deterministic하게 나온다"를 먼저 증명하는 것이다.

## 감사팀 workflow에서의 위치

`team-workflows.md` 기준 F-AUD의 분석적 절차는 다음 위치다.

- 자료수집: 전기 F/S, 당기 F/S, 산업정보, 원장 또는 trial balance를 받는다.
- 계산/대사: 전년 대비 증감률, 주요 비율, 추세, 비정상 변동을 계산한다.
- 판단: 변동 원인을 질문으로 만들고, 회계이슈 또는 감사절차 확장 필요성을 검토한다.
- 문서화: 분석조서, 이상징후 메모, reviewer question을 남긴다.

이번 horizon은 감사결론을 내리는 것이 아니라 계산/대사와 문서화 초안을 자동화한다.

## AP1 scope 결정

### 포함

- 2개 기간 이상의 재무제표 line item 입력.
- 금액, 전년 대비 증감액, 증감률 계산.
- 간단한 비율 계산:
  - 매출총이익률
  - 영업이익률
  - 유동비율
  - 부채비율
  - 매출채권 회전 관련 보조 지표는 후속 후보.
- threshold 기반 anomaly flag:
  - 절대금액 변동
  - 증감률 변동
  - 이익률 악화/개선
  - balance sheet line과 income statement line의 불일치 신호
- anomaly note:
  - 어떤 line이 얼마나 변했는지
  - 감사인이 확인할 질문
  - 연결 가능한 F-ACC output 후보

### 제외

- 감사 중요성 계산.
- 표본설계.
- KAM 또는 감사의견 문구.
- 내부통제 평가.
- 산업 평균 benchmark.
- DART API 직접 수집.
- 회사별 계정과목 mapping 자동화.

## Synthetic F/S fixture v0

AP2에서 만들 최소 schema 후보:

```python
FinancialStatementLine(
    period: str,
    statement: Literal["balance_sheet", "income_statement"],
    line_item: str,
    amount: float,
)

AnalyticalProcedureInput(
    entity: str,
    periods: list[str],
    lines: list[FinancialStatementLine],
)
```

첫 fixture는 다음 line item만 포함한다.

| Statement | Line item | 이유 |
|---|---|---|
| balance_sheet | 현금및현금성자산 | liquidity 변화 |
| balance_sheet | 매출채권 | revenue와 대사할 수 있는 working capital line |
| balance_sheet | 재고자산 | 매출원가와 연결되는 변동 후보 |
| balance_sheet | 유동자산 | 유동비율 |
| balance_sheet | 유동부채 | 유동비율 |
| balance_sheet | 총부채 | 부채비율 |
| balance_sheet | 자본총계 | 부채비율 |
| income_statement | 수익 | gross/operating margin denominator |
| income_statement | 매출원가 | gross margin |
| income_statement | 매출총이익 | gross margin |
| income_statement | 판매비와관리비 | operating margin bridge |
| income_statement | 영업이익 | operating margin |
| income_statement | 금융비용 | debt/financing anomaly link |

## 계산 output 후보

```python
AnalyticalMetric(
    metric_id: str,
    label: str,
    current_value: float,
    prior_value: float | None,
    change_amount: float | None,
    change_pct: float | None,
)

AnomalyFinding(
    finding_id: str,
    severity: Literal["info", "warning", "critical"],
    metric_id: str,
    message: str,
    review_questions: list[str],
    linked_statement_candidates: list[str],
)
```

## F-ACC output linkage

F/S draft에서 만든 `StatementLineCandidate`는 AP4의 연결 후보가 된다.

- 1115 수익/계약부채 후보가 있으면 수익 급증, 계약부채 급증 anomaly와 연결.
- 1109 FVPL/FVOCI 평가손익 후보가 있으면 금융수익/OCI 변동 anomaly와 연결.
- 1116 사용권자산/리스부채 후보가 있으면 부채비율 또는 금융비용 변동 anomaly와 연결.

AP1에서는 연결을 구현하지 않고, AP4의 입력 contract로만 남긴다.

## 다음 step

AP2는 `kifrs/workflows/audit_analytics/`를 추가하고, synthetic fixture에서 ratio/trend metric을
deterministic하게 계산하는 schema와 runner를 만든다.
