# Step 3: anomaly-note-renderer

Status: pending

## 읽어야 할 파일

- `phases/audit-analytical-procedures/step2.md` — 왜: AP2 metric schema와 runner 결과를 이어받는다.
- `kifrs/workflows/audit_analytics/schema.py` — 왜: finding schema를 추가할 위치다.
- `kifrs/workflows/audit_analytics/metrics.py` — 왜: metric output을 anomaly input으로 사용한다.
- `tests/test_audit_analytics.py` — 왜: AP3 renderer test를 추가한다.

## 작업

threshold 기반 anomaly finding과 markdown note renderer를 추가한다. 큰 증감률, 영업이익률 악화,
부채비율 상승 같은 finding에 review question을 붙인다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_audit_analytics.py
git diff --check
```

## 금지사항

- finding을 감사결론으로 표현하지 않는다. 이유: AP3는 이상징후 메모 초안이다.
- 산업 benchmark나 외부 데이터를 사용하지 않는다.
