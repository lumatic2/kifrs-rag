# RP3 — NeedsHumanReview Checklist Hardening

> Date: 2026-07-05
> Horizon: `f-acc-review-pack`

## 무엇을 바꿨나

RP3는 review pack의 `needs_human_review`를 단순 문자열 목록에서 구조화된 회계사 action checklist로
바꿨다. 이제 pack은 다음 정보를 낸다.

- 이슈: 무엇 때문에 자동화가 멈췄는지
- 왜 멈췄나: 자동 판단 경계
- 필요한 추가자료: 회계사가 받아야 할 입력
- 리뷰 질문: workpaper에 결론을 적기 전에 답해야 할 질문
- 기준서 처리 방향: 검토할 K-IFRS 1116 문단 방향

## scenario_09 결과

`scenario_09_lessee_modification_expand_shrink`는 계속 `needs_human_review`다. 다만 이제 실패 문구가
아니라 다음 checklist로 보인다.

- 이슈: 리스범위 확장+축소 동시 변경
- 필요한 추가자료: 변경 전 리스부채/사용권자산 장부금액, 축소 범위와 비율, 확장 범위/기간/대가,
  변경일 수정 할인율, 변경 전후 지급 스케줄
- 리뷰 질문: 축소분이 부분 종료인지, 확장분이 별도 리스인지, 제거 비율과 손익 계산 근거가 무엇인지,
  잔여/확장분 재측정 할인율이 무엇인지
- 기준서 방향: `[1116-45]`, `[1116-46(a)]`, `[1116-46(b)]`

## 자동화 pack 결과

자동화된 리스이용자 pack도 사람 검토 항목을 더 구체화했다. 회사 회계정책 문구, 단기·소액 면제,
변동리스료, 전대리스, 판매후리스, 만기분석 자료를 별도 확인해야 한다는 점을 checklist로 노출한다.

## 검증

```text
python -m pytest tests/test_workflow_1116_regression.py tests/test_1116_disclosure.py tests/test_1116_review_pack.py
git diff --check
```

결과: 통과.

## 의미

RP3 이후 review pack은 "자동화됨/멈춤" 상태만 보여주는 산출물이 아니라, 회계사가 이어서 검토할
workpaper queue까지 제공한다. 이것이 F-ACC PoC에서 설명할 제품성의 핵심이다.
