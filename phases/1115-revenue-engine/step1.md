# Step 1: schema-fixture-inventory

Status: completed (2026-07-05)

## 읽어야 할 파일

- `docs/horizons/f-acc-1115-revenue-engine.md` — 왜: 1115 horizon 목표와 milestone sequence가 있다.
- `docs/plans/2026-07-05-r15-1115-revenue-engine.md` — 왜: R15 전체 step tree와 결정 로그가 있다.
- `data/scenarios/1115_revenue/WORKFLOW.md` — 왜: 비공개 seed. 공개 fixture로 옮길 판단유형과 인용 후보를 확인한다.
- `kifrs/workflows/kifrs1109/schema.py` — 왜: 구조화 입력 schema 스타일과 special_case 경계를 참고한다.
- `kifrs/workflows/kifrs1116/fixtures.py` — 왜: 비공개 scenario를 공개 가능한 fixture로 수동 전사한 전례다.

## 작업

1115 revenue workflow seed의 4개 판단유형을 공개 가능한 schema와 fixture로 옮긴다. 첫 결정 함수는
판단 경로, 수행의무, 주요 근거 인용을 반환한다. 기준서 원문, 시험 문제 원문, 모범답안 텍스트는
커밋하지 않는다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_workflow_1115.py
git diff --check
```

## 검증 절차

1. AC 커맨드 실행
2. 4개 fixture가 모두 구조화 입력으로 생성되는지 확인
3. 결정 함수가 각 fixture의 expected_path와 citations를 반환하는지 확인
4. `phases/1115-revenue-engine/index.json` step 상태 갱신

## 결과

- `kifrs/workflows/kifrs1115/schema.py`: 수익 계약 구조화 입력 `Revenue1115` 추가.
- `kifrs/workflows/kifrs1115/fixtures.py`: 고객 선택권, 할인권, 유의적 금융요소, 재매입 콜옵션 4개 seed fixture 추가.
- `kifrs/workflows/kifrs1115/classify.py`: 첫 결정 함수 `evaluate_revenue()` 추가.
- `tests/test_workflow_1115.py`: 4개 fixture path/citation regression 추가.

## 금지사항

- `data/` 아래 파일을 git add하지 않는다.
- 기준서 원문, 시험 문제 원문, 모범답안 텍스트를 fixture에 넣지 않는다.
