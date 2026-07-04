# Step PB1: Horizon and Phase Setup

## 읽어야 할 파일

- `docs/OBJECTIVE.md` - 왜: 법인 소개/PoC를 성공 모습으로 둔 현재 objective를 확인한다.
- `ROADMAP.md` - 왜: `toolkit-packaging-readiness` 완료 뒤 다음 active horizon을 연다.
- `docs/horizons/toolkit-packaging-readiness.md` - 왜: readiness package가 무엇을 증명했는지 이어받는다.
- `docs/practice-map/company-map.md` - 왜: 회계법인 service-line과 1순위 대상 팀을 확인한다.
- `docs/practice-map/team-workflows.md` - 왜: F-ACC/F-AUD 업무 흐름과 AI insertion point를 확인한다.

## 작업

`firm-facing-poc-brief` horizon을 열고 PB1~PB4 phase를 정의한다.

## Acceptance Criteria

```powershell
Test-Path docs\horizons\firm-facing-poc-brief.md
Test-Path phases\firm-facing-poc-brief\index.json
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. ROADMAP/OBJECTIVE가 active horizon을 가리키는지 확인한다.
3. PB1을 completed로 업데이트한다.

## 금지사항

- 기준서 원문, DB, 임베딩, dogfood 자료를 PoC 브리프에 포함하지 않는다.
