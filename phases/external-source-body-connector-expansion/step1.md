# Step 1: Source-Body Connector Selection And Policy Gate

## 읽어야 할 파일

- `docs/horizons/external-source-body-connector-expansion.md` - 왜: ESB1 acceptance와 horizon boundary를 확인한다.
- `docs/plans/2026-07-05-external-source-body-connector-expansion.md` - 왜: ESB milestone tree와 decision log를 따른다.
- `docs/reports/2026-07-05-private-parser-realism-hardening-close-report.md` - 왜: 직전 horizon handoff evidence다.
- `docs/reports/2026-07-05-esbd1-external-source-body-ingestion-decision-gate.md` - 왜: 기존 source-body decision evidence다.
- `docs/reports/2026-07-05-esag1-external-source-body-authorization-gate.md` - 왜: authorization gate evidence다.

## 작업

`scripts/external_source_connector_body_selection.py`를 만들어 첫 source-body connector class, authorization boundary, allowed fields, public-safe report rules를 고정한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_external_source_connector_body_selection.py -q
python scripts\external_source_connector_body_selection.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. protected source body ingestion을 실제 수행했다고 주장하지 않는지 확인
3. phase index 업데이트

## 금지사항

- protected third-party body text를 public report에 넣지 마라.
- live scraping이나 배포를 완료했다고 주장하지 마라.
