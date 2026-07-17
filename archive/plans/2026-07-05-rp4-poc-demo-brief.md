# RP4 — PoC demo brief

> Date: 2026-07-05
> Horizon: `f-acc-review-pack`
> ROADMAP milestone: RP4
> Phase step: `phases/1116-review-pack/step4.md`

## 산문 요약

RP4는 RP1~RP3로 만든 1116 F-ACC review pack을 회계법인 Accounting Advisory 팀에 설명할 수 있는
PoC 브리프로 묶는다. 목적은 "AI가 기준서 리서치를 한다"가 아니라 "리스 계약 검토 workpaper 초안을
줄인다"는 제품 표면을 보여주는 것이다.

## Step tree

- [x] Step 4 — PoC demo brief
  - AC: `docs/reports/2026-07-05-rp4-poc-demo-brief.md`가 문제, 사용자, demo flow, 현재 capability,
    사람 검토 경계, PoC 질문을 포함한다.
  - AC: `python -m pytest tests/test_1116_review_pack.py`
  - AC: `git diff --check`

## 결정 로그

- 결정: RP4는 영업자료가 아니라 PoC 대화용 technical brief로 작성한다.
- 결정: 공개 repo 제약 때문에 기준서 원문, DB, dogfood 자료, 고객자료 예시는 포함하지 않는다.
- 결정: 다음 구현을 약속하지 않고, 현 PoC 질문을 통해 패키징/인터뷰/다음 도메인 중 무엇을 할지 판단한다.

## 산출물

- `docs/reports/2026-07-05-rp4-poc-demo-brief.md`
- `phases/1116-review-pack/step4.md`
- `ROADMAP.md`
- `phases/1116-review-pack/index.json`
