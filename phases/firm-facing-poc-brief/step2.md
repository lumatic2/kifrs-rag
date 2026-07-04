# Step PB2: PoC Brief

## 읽어야 할 파일

- `docs/practice-map/company-map.md` - 왜: 회계법인 서비스라인 구조를 브리프의 첫 문단으로 압축한다.
- `docs/practice-map/team-workflows.md` - 왜: F-ACC와 F-AUD의 workflow별 적용 지점을 설명한다.
- `docs/practice-map/service-line-candidates.md` - 왜: F-ACC review pack을 1순위 PoC 표면으로 둔 근거를 확인한다.
- `docs/reports/field-feedback/INDEX.md` - 왜: 현업 피드백 흐름과 질문지를 연결한다.
- `docs/reports/demo-poc/MANIFEST.md` - 왜: 실제 데모 흐름을 브리프에 연결한다.
- `docs/toolkit/README.md` - 왜: 로컬 도구킷 실행 경계를 설명한다.

## 작업

회계법인 담당자에게 보낼 수 있는 본문 브리프를 작성한다.

## Acceptance Criteria

```powershell
Test-Path docs\reports\firm-facing-poc\2026-07-05-poc-brief.md
rg -n "F-ACC|F-AUD|PoC ask|Risk boundary" docs\reports\firm-facing-poc\2026-07-05-poc-brief.md
```

## 검증 절차

1. 브리프가 target team, problem, proof, demo path, risk boundary, ask를 포함하는지 확인한다.
2. PB2를 completed로 업데이트한다.

## 금지사항

- 최종 회계판단, 감사의견, 세무판단을 AI가 대체한다고 표현하지 않는다.
