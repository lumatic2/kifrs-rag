# AP5 Analytical Procedure Report

> Date: 2026-07-05
> Horizon: `f-audit-analytical-procedures`
> Evidence: `kifrs/workflows/audit_analytics/`, `tests/test_audit_analytics.py`

## 한 줄 결론

감사팀용 분석적 절차 PoC가 생겼다. synthetic F/S fixture에서 주요 line item 증감과 비율을 계산하고,
threshold 기반 이상징후 메모를 만들며, 관련 F-ACC statement candidate와 연결한다. 감사의견, KAM,
중요성, 표본설계, 내부통제 결론은 자동화하지 않는다.

## 무엇이 됐나

### 1. Synthetic F/S fixture

AP1에서 DART/API 의존을 뒤로 미루고 synthetic F/S fixture부터 닫기로 했다. 이 fixture는 다음 line을
포함한다.

- 재무상태표: 현금및현금성자산, 매출채권, 재고자산, 유동자산, 유동부채, 총부채, 자본총계
- 손익계산서: 수익, 매출원가, 매출총이익, 판매비와관리비, 영업이익, 금융비용

목적은 외부 credential 없이 분석적 절차 계산과 memo generation을 회귀 테스트하는 것이다.

### 2. Ratio/trend 계산

`calculate_metrics()`는 다음을 deterministic하게 만든다.

- line item별 current/prior/change/change_pct
- 매출총이익률
- 영업이익률
- 유동비율
- 부채비율

현재 fixture에서는 수익 증가, 매출채권 증가, 영업이익률 하락, 부채비율 상승 같은 감사 질문 후보가
의도적으로 드러난다.

### 3. 이상징후 finding과 memo

`detect_anomalies()`는 metric을 threshold에 따라 `AnomalyFinding`으로 바꾼다.

- 큰 line item 변동: 예를 들어 매출채권 급증
- 영업이익률 하락: 수익 증가와 margin 악화가 동시에 나타나는 경우
- 부채비율 상승: 리스부채, 금융부채, 계약부채 검토 후보

`render_anomaly_note()`는 finding을 workpaper-style markdown으로 렌더링한다. 메모에는 항상
"감사결론, 중요성, 표본설계, KAM 판단은 포함하지 않음" 경계가 들어간다.

### 4. F-ACC output linkage

`link_statement_candidates()`는 audit finding과 F-ACC `StatementLineCandidate`를 line item 기준으로
연결한다.

예시:

- 부채비율 상승 finding → 1115 재매입약정 `금융부채` candidate
- 수익/계약부채 anomaly → 1115 수익인식 candidate
- 리스 관련 부채 anomaly → 1116 리스부채 candidate

이 연결은 "이 항목을 더 보라"는 검토 후보이지 감사 결론이 아니다.

## 자동화된 것과 남은 것

| 영역 | 지금 자동화 | 남은 사람 검토 |
|---|---|---|
| 입력 | synthetic F/S line fixture | 실제 고객 TB, DART 공시 파싱, 계정 mapping |
| 계산 | 증감액, 증감률, 주요 비율 | 산업 benchmark, 회사 특수 KPI |
| 이상징후 | threshold 기반 finding | 원인 판단, 감사절차 확장 여부 |
| 문서화 | markdown 분석적 절차 메모 | 조서 양식 반영, reviewer sign-off |
| F-ACC 연결 | statement candidate와 finding 연결 | 실제 회계이슈 결론, 중요성 판단 |

## 회계법인 설명 방식

> "재무제표 숫자를 넣으면 전년 대비와 주요 비율을 계산하고, 이상징후와 리뷰 질문을 메모로 뽑습니다.
> 이미 만든 수익/리스/금융상품 회계처리 후보와도 연결해 줍니다. 단, 감사결론과 중요성 판단은 사람이 합니다."

이 horizon의 의미는 F-ACC 산출물이 F-AUD 보조 업무로 확장됐다는 것이다. 회계자문팀의 검토메모/분개/
F/S 표시 후보가 감사팀의 분석적 절차 질문으로 이어진다.

## 검증

- `python -m pytest tests/test_audit_analytics.py`: 7 passed.
- `python -m pytest tests/test_audit_analytics.py tests/test_statement_draft.py`: 14 passed.
- `git diff --check`: passed.

## 다음 horizon

다음 sequence는 `product-packaging-poc`다. 여기서 처음으로 기술 표면을 회계법인 소개용 demo pack으로
묶는다. 포함 후보는 demo CLI, sample input/output bundle, README/setup guide, 10분 demo brief, 회계사
피드백 질문지다.
