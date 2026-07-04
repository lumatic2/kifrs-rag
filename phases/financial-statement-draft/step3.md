# Step 3: 1109-statement-draft-pilot

Status: completed

## 읽어야 할 파일

- `phases/financial-statement-draft/step2.md` — 왜: 공통 statement draft schema와 adapter가 만들어진 상태를 이어받는다.
- `kifrs/workflows/statement_draft/adapters.py` — 왜: 1109 adapter를 pilot 수준으로 확장할 위치다.
- `kifrs/workflows/kifrs1109/subsequent_entry.py` — 왜: FVOCI/FVPL/AC 후속측정 분개가 PL/OCI 표시 후보의 source다.
- `kifrs/workflows/kifrs1109/runner.py` — 왜: 1109 scenario outcome에서 후속분개 접근 가능 여부를 확인한다.
- `tests/test_statement_draft.py` — 왜: FS2 adapter test에 FS3 1109 pilot 기대값을 추가한다.

## 작업

1109 statement draft adapter를 pilot 수준으로 확장한다. 최초인식 분개뿐 아니라 1109 분류별 표시 방향을
더 명확히 하고, 가능한 경우 후속측정 PL/OCI line 후보를 포함한다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_statement_draft.py tests/test_workflow_1109.py tests/test_workflow_1109_regression.py
git diff --check
```

## 금지사항

- 1109 분류 로직 자체를 바꾸지 않는다. 이유: FS3는 표시 pilot이지 classification hardening이 아니다.
- IFRIC19, 재분류, FX dual-track 결론을 자동 확정하지 않는다. 이유: FH horizon에서 사람 검토 경계로 확정했다.

## 완료 요약

1109 runner/review pack에 이미 계산되던 후속측정 분개를 보존하고, statement draft adapter가
`subsequent_entries`를 재무제표 후보로 변환하게 했다. 이제 AC/FVOCI/FVPL의 이자수익, FVPL 평가손익,
FVOCI OCI 평가손익이 `StatementLineCandidate`로 나온다. `tests/test_statement_draft.py`,
`tests/test_workflow_1109.py`, `tests/test_workflow_1109_regression.py`가 통과했다.
