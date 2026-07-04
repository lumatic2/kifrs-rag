# Step 3: needs-human-review-checklist

## 읽어야 할 파일

- `docs/PRD.md` — 왜: review pack이 회계자문팀 workpaper 초안이어야 한다는 제품 요구가 있다.
- `docs/ARCHITECTURE.md` — 왜: `review_pack.py`는 기존 1116 판단 로직을 감싸는 orchestration layer로 제한된다.
- `docs/horizons/f-acc-review-pack.md` — 왜: RP3의 위치와 close criteria를 확인한다.
- `docs/plans/2026-07-05-rp3-needs-human-review-checklist.md` — 왜: RP3 결정 로그와 acceptance criteria가 있다.
- `kifrs/workflows/kifrs1116/review_pack.py` — 왜: 사람 검토 항목 schema와 renderer를 수정할 대상이다.
- `tests/test_1116_review_pack.py` — 왜: structured action checklist와 markdown 노출을 고정할 테스트다.

## 작업

`NeedsHumanReview` pack이 단순 사유 문자열이 아니라 회계사가 처리할 action checklist를 제공하도록
`review_pack.py`를 강화한다. 새 1116 판단 로직은 만들지 않고, 기존 runner가 멈춘 경계를 설명 가능한
workpaper 입력으로 바꾼다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_workflow_1116_regression.py tests/test_1116_disclosure.py tests/test_1116_review_pack.py
git diff --check
```

## 검증 절차

1. AC 커맨드 실행
2. `scenario_09_lessee_modification_expand_shrink` markdown에 필요한 추가자료, 리뷰 질문, 기준서 처리 방향이 표시되는지 확인
3. `phases/1116-review-pack/index.json` step 상태 갱신

## 금지사항

- RP3에서 `scenario_09` 자동 판단을 새로 구현하지 않는다. 이유: 확장+축소 동시 변경은 회계사 수동 검토 경계로 남긴다.
- 기준서 원문 또는 비공개 DB 내용을 report에 포함하지 않는다.
