# Step RC3: Case-to-Review-Pack Routing Stub

## 읽어야 할 파일

- `kifrs/workflows/source_aware_rebuild.py` - 왜: 현재 지원 가능한 1109/1115/1116 domain을 확인한다.
- `kifrs/workflows/kifrs1109/fixtures.py`, `kifrs/workflows/kifrs1115/fixtures.py`, `kifrs/workflows/kifrs1116/fixtures.py` - 왜: routing 후보가 어떤 구조화 사실을 요구하는지 확인한다.

## 작업

`CaseIntake`의 domain hint와 fact keys를 보고 review pack routing 후보를 반환한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_real_case_feedback.py -q
```

## 검증 절차

1. 1109/1115/1116 후보 routing test를 통과시킨다.
2. 세무/unsupported domain은 out-of-scope reason을 반환한다.
3. RC3을 completed로 업데이트한다.

## 금지사항

- routing stub에서 실제 판단 엔진을 실행하지 않는다.
- 불충분한 입력을 자동화 가능하다고 표시하지 않는다.
