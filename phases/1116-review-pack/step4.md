# Step 4: poc-demo-brief

## 읽어야 할 파일

- `docs/PRD.md` — 왜: F-ACC review pack의 사용자, 산출물, non-goal이 정의되어 있다.
- `docs/horizons/f-acc-review-pack.md` — 왜: RP4의 위치와 close criteria를 확인한다.
- `docs/practice-map/company-map.md` — 왜: 회계법인 service-line 맥락과 F-ACC 적용처를 설명한다.
- `docs/practice-map/team-workflows.md` — 왜: F-ACC workflow 안에서 review pack이 줄이는 단계를 설명한다.
- `docs/reports/2026-07-04-rp2-1116-review-pack-fixture-summary.md` — 왜: 1116 fixture 전체 상태 증거다.
- `docs/reports/2026-07-05-rp3-needs-human-review-checklist.md` — 왜: 사람 검토 경계와 checklist 증거다.

## 작업

회계법인 Accounting Advisory 팀에 보여줄 1~2페이지 PoC demo brief를 작성한다. 브리프는 제품이 줄이는
workpaper 산출물, 현재 되는 것, 사람이 남는 판단, PoC에서 확인할 질문을 명확히 적는다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_1116_review_pack.py
git diff --check
```

## 검증 절차

1. AC 커맨드 실행
2. 브리프가 RP1~RP3 evidence에 근거하는지 확인
3. `phases/1116-review-pack/index.json` step 상태 갱신

## 금지사항

- 기준서 원문, DB 덤프, 비공개 dogfood 자료를 브리프에 넣지 않는다.
- 최종 회계 판단, 감사의견, 서명 책임을 AI가 대체한다고 쓰지 않는다.
