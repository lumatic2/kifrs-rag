# Field Feedback Package

> Date: 2026-07-05
> Purpose: 회계사 1명에게 최신 runtime evidence demo를 보여주고 실무 피드백을 받기 위한 자료 묶음.

## Demo Command

```powershell
python scripts\demo_poc.py --scenario revenue-financing --out docs\reports\demo-poc
```

## 읽는 순서

1. `docs/reports/field-feedback/2026-07-05-demo-brief.md`
   - 10분 demo flow와 설명 포인트.
2. `docs/reports/demo-poc/MANIFEST.md`
   - demo bundle 파일 목록.
3. `docs/reports/demo-poc/evidence-boundary.md`
   - primary K-IFRS evidence와 external evidence boundary.
4. `docs/reports/demo-poc/statement-candidates.md`
   - 재무제표 표시 후보와 synthetic fact evidence reference.
5. `docs/reports/field-feedback/2026-07-05-known-limitations.md`
   - 회계사 검토 필요성과 자동화 경계.
6. `docs/reports/field-feedback/2026-07-05-feedback-questionnaire.md`
   - 피드백 기록용 질문지.

## 피드백 목표

- 실제 검토 시간을 줄일 가능성이 있는 section을 찾는다.
- 위험하거나 오해될 수 있는 section을 찾는다.
- 다음 익명화 실제 거래 PoC 후보를 고른다.
- 법인 소개 전 보강해야 할 evidence boundary와 human-review gate를 확인한다.

## 피드백 후 결정 후보

1. `feedback-incorporation`
   - 받은 피드백을 바탕으로 demo, evidence boundary, review questions를 보강.
2. `real-anonymized-transaction-poc`
   - 익명화 실제 거래 1건으로 demo를 재구성.
3. `firm-introduction-material`
   - 법인 소개용 one-pager/deck/script 제작.

