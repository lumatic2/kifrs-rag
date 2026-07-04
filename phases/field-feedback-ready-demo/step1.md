# FF1 — Demo Brief Refresh

## Objective

기존 PK5 demo brief를 최신 runtime evidence demo 기준으로 갱신한다. 회계사에게 10분 안에 무엇을 보여줄지,
어떤 순서로 볼지, 무엇을 결정하지 말아야 하는지 명확히 한다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-pk5-demo-brief-feedback.md` — 왜: 기존 demo brief와 질문지의 출발점.
- `docs/reports/2026-07-05-rt5-runtime-close-demo.md` — 왜: 최신 runtime evidence demo의 변경점.
- `docs/reports/demo-poc/MANIFEST.md` — 왜: 실제 demo bundle 파일 목록.
- `docs/reports/demo-poc/evidence-boundary.md` — 왜: 새 evidence boundary 설명 대상.
- `docs/reports/demo-poc/statement-candidates.md` — 왜: fact evidence reference가 표시되는 화면.

## 작업

1. 새 brief 파일을 작성한다.
   - 후보 path: `docs/reports/field-feedback/2026-07-05-demo-brief.md`
2. 10분 demo flow를 최신 파일 기준으로 갱신한다.
   - review pack external evidence section
   - statement candidate evidence column
   - evidence boundary file
3. 회계사에게 요청할 피드백 범위를 명확히 한다.
   - 정확성 최종 판단이 아니라 workflow usefulness와 위험 평가
4. source body, raw filing, protected DB가 demo에 없다는 경계를 포함한다.

## Acceptance Criteria

```powershell
python scripts\demo_poc.py --scenario revenue-financing --out docs\reports\demo-poc
Test-Path docs\reports\field-feedback\2026-07-05-demo-brief.md
Select-String -Path docs\reports\field-feedback\2026-07-05-demo-brief.md -Pattern "evidence-boundary.md"
Select-String -Path docs\reports\field-feedback\2026-07-05-demo-brief.md -Pattern "회계사 검토를 대체하지 않는다"
git diff --check
```

## Deliverable

- `docs/reports/field-feedback/2026-07-05-demo-brief.md`

## 금지사항

- 제품을 이미 도입 가능한 완제품처럼 표현하지 않는다.
- 외부 evidence가 회계 결론을 자동 확정한다고 말하지 않는다.
- 기준서 원문, 질의회신 본문, 법령 조문, raw filing을 인용하지 않는다.

