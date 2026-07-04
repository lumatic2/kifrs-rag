# Firm-Facing PoC Package

> Date: 2026-07-05
> Purpose: 회계법인 소개/PoC를 위한 public-safe narrative package.

## 읽는 순서

1. `docs/reports/firm-facing-poc/2026-07-05-one-page-brief.md`
   - 미팅 전송용 1페이지 요약.
2. `docs/reports/firm-facing-poc/2026-07-05-poc-brief.md`
   - 회계법인 service-line, demo path, risk boundary, PoC ask를 담은 본문 브리프.
3. `docs/reports/field-feedback/INDEX.md`
   - 회계사 1명에게 실제 demo를 보여주고 피드백을 받는 자료 묶음.
4. `docs/reports/demo-poc/MANIFEST.md`
   - public-safe demo bundle 파일 목록과 재생성 명령.
5. `docs/toolkit/README.md`
   - 로컬 도구킷 readiness와 protected-data boundary.

## 핵심 메시지

- 첫 PoC 대상은 F-ACC(Accounting Advisory / F-S support)다.
- 감사팀은 회계이슈 검토와 주석 요구사항 대사 보조 적용처다.
- 이 도구는 최종 판단이 아니라 결정준비 초안을 만든다.
- public repo는 기준서 원문, 파싱 DB, 임베딩, dogfood 자료, 고객자료를 포함하지 않는다.

## Meeting Use

### 10분 소개

1. F-ACC review pack이 왜 첫 표면인지 설명한다.
2. demo PoC bundle의 review pack과 evidence boundary를 보여준다.
3. limitations와 human-review boundary를 먼저 말한다.

### 30분 데모

```powershell
python scripts\demo_poc.py --scenario revenue-financing --out docs\reports\demo-poc
```

이후 `docs/reports/demo-poc/1115-significant-financing-review-pack.md`,
`docs/reports/demo-poc/evidence-boundary.md`,
`docs/reports/demo-poc/statement-candidates.md` 순서로 본다.

## PoC 요청사항

1. 익명화된 복잡 거래 1건
2. 회계사 reviewer 1명
3. 평가 기준 3개: 시간 절감, 근거 추적성, human-review boundary
