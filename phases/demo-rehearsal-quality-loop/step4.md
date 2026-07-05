# Step 4: Demo Improvement Backlog

## 읽어야 할 파일

- `docs/reports/2026-07-05-drq3-demo-rehearsal-evidence.md` - 왜: improvement backlog의 finding source다.

## 작업

rehearsal findings를 product impact와 implementation cost 기준으로 backlog items로 변환한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_demo_improvement_backlog.py -q
python scripts\demo_improvement_backlog.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. backlog가 외부 의존 없이 내부 개선으로 닫히는지 확인
3. phase index 업데이트

## 금지사항

- outreach 또는 packaging을 backlog item으로 넣지 마라.
