# RT5 Runtime Close Demo

> Horizon: `multi-authority-runtime-integration`
> Step: RT5 — Runtime Close Demo
> Date: 2026-07-05

## 한 줄 결론

`multi-authority-runtime-integration` horizon은 닫을 수 있다. ingestion/evidence manifest가 runtime loader,
review pack, statement draft, answer boundary, demo bundle까지 연결됐다.

## 무엇이 가능해졌나

### 1. Review pack에서 외부 근거 표시

1115/1116 demo review pack markdown에 `## 외부 근거` section이 추가됐다.

표시되는 role:

- 해석 보조 근거
- 법적 경계 근거
- 수치 사실 근거

### 2. Statement draft candidate에서 fact evidence reference 표시

`statement-candidates.md`에 `Evidence` column이 추가됐다. 금액 후보에는 synthetic DART fact id가 붙고,
note-only candidate에는 fact evidence가 붙지 않는다.

### 3. Answer boundary demo

새 demo output:

- `docs/reports/demo-poc/evidence-boundary.md`

이 파일은 primary K-IFRS evidence와 external evidence를 분리한다.

Sections:

- Primary K-IFRS evidence
- Supporting interpretation
- Legal boundary
- Fact evidence

## 구현 산출물

Runtime:

- `kifrs/runtime/evidence.py`
- `kifrs/runtime/evidence_panel.py`
- `kifrs/runtime/answer_boundary.py`

Workflow integration:

- `kifrs/workflows/kifrs1116/review_pack.py`
- `kifrs/workflows/kifrs1109/review_pack.py`
- `kifrs/workflows/kifrs1115/review_pack.py`
- `kifrs/workflows/statement_draft/schema.py`
- `kifrs/workflows/statement_draft/adapters.py`

Demo:

- `scripts/demo_poc.py`
- `docs/reports/demo-poc/evidence-boundary.md`
- `docs/reports/demo-poc/statement-candidates.md`
- `docs/reports/demo-poc/MANIFEST.md`

Tests:

- `tests/test_runtime_evidence.py`
- `tests/test_answer_boundary.py`
- `tests/test_demo_poc.py`
- `tests/test_statement_draft.py`

## Close Gate

```powershell
python scripts\demo_poc.py --scenario revenue-financing --out docs\reports\demo-poc
# wrote index/review packs/statement candidates/evidence boundary/audit outputs

python -m pytest tests\test_demo_poc.py tests\test_answer_boundary.py tests\test_statement_draft.py -q
# 13 passed

python scripts\validate_ingestion_manifest.py docs\ingestion\source_manifest.example.json
# ok: true, total: 5

python scripts\validate_ingestion_evidence.py docs\ingestion\evidence_manifest.example.json
# ok: true, total: 3

python scripts\quality_preflight.py --format text
# ok: True, public_safe: True

git diff --check
# no whitespace errors
```

Pytest cache warning은 `.pytest_cache` 쓰기 권한 문제이고 테스트 실패는 아니다.

## Deliberately Out of Scope

- no external API call
- no raw DART filing
- no KASB/FSS body fetch
- no law article body copy
- no MCP answer runtime rewrite
- no final accounting judgment automation from external evidence alone

## Next Horizon Recommendation

Recommended next horizon:

- `field-feedback-ready-demo`

Why:

이제 demo bundle은 기준서 근거, 외부 해석/법적 경계 metadata, synthetic fact evidence를 함께 보여준다.
다음은 회계사 1명이 읽고 피드백할 수 있도록 demo brief, feedback questionnaire, known limitations를 최신
runtime output 기준으로 갱신하는 것이다.

Candidate milestones:

1. Demo brief refresh
   - runtime evidence boundary가 무엇을 보여주는지 설명한다.
2. Feedback questionnaire refresh
   - 회계사가 볼 질문을 “정확성/유용성/검토 부담/위험”으로 나눈다.
3. Known limitation and human-review boundary
   - external evidence가 결론을 대체하지 않는다는 경계를 명확히 한다.
4. Feedback package smoke
   - demo command와 산출물 경로를 한 번에 검증한다.

