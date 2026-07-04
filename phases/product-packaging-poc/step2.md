# Step 2: demo-command-surface

Status: completed

## 읽어야 할 파일

- `docs/reports/2026-07-05-pk1-demo-scenario-selection.md` — 왜: demo flow와 scenario가 선택되어 있다.
- `kifrs/workflows/kifrs1115/fixtures.py` — 왜: primary 1115 demo input.
- `kifrs/workflows/kifrs1115/review_pack.py` — 왜: review pack output.
- `kifrs/workflows/statement_draft/adapters.py` — 왜: F/S draft candidates output.
- `kifrs/workflows/audit_analytics/` — 왜: audit analytics linkage output.
- `kifrs/workflows/kifrs1116/fixtures.py` — 왜: secondary lease demo input.

## 작업

로컬 demo command surface를 만든다. 첫 형태는 `scripts/demo_poc.py`로 충분하다. command는 선택한 scenario를
실행하고 markdown output을 `demo_outputs/` 또는 `docs/reports/` 아래에 남긴다.

## Acceptance Criteria

```powershell
python scripts/demo_poc.py --scenario revenue-financing --out docs/reports/demo-poc
python -m pytest tests/test_demo_poc.py
git diff --check
```

## 금지사항

- 기준서 원문, DB, embedding, dogfood 자료를 output에 포함하지 않는다.
- 외부 API, DART, network를 호출하지 않는다.

## 완료 요약

`scripts/demo_poc.py`를 추가했다. `revenue-financing` scenario는 1115 significant financing, 1115 repurchase,
statement candidates, audit analytics note, audit-FACC links, 1116 lease review pack을 markdown으로 생성한다.
`tests/test_demo_poc.py`와 실제 `python scripts/demo_poc.py --scenario revenue-financing --out docs\reports\demo-poc`
실행이 통과했다.
