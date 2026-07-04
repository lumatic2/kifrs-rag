# RT3 — Statement Draft Fact Evidence Hook

## Objective

statement draft 후보가 runtime `fact_evidence`를 참조할 수 있게 한다. RT2처럼 판단 로직은 바꾸지 않고,
`StatementLineCandidate`가 synthetic structured fact evidence와 연결될 수 있는 reference field를 추가한다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-rt2-review-pack-evidence-panel.md` — 왜: review pack이 external evidence를 어떻게 표시하는지.
- `kifrs/runtime/evidence.py` — 왜: fact evidence query helper.
- `kifrs/workflows/statement_draft/schema.py` — 왜: `StatementLineCandidate` contract 수정 대상.
- `kifrs/workflows/statement_draft/adapters.py` — 왜: 1109/1115/1116 review pack을 statement candidate로 변환하는 곳.
- `tests/test_statement_draft.py` — 왜: 기존 statement draft regression과 새 evidence reference 테스트.

## 작업

1. `StatementLineCandidate`에 optional evidence reference field를 추가한다.
   - field 후보: `evidence_refs: list[dict[str, object]]`
   - default는 empty list로 기존 호출을 깨지 않는다.
2. statement draft adapter가 review pack의 `external_evidence` 중 `fact_evidence`를 line candidate에 연결한다.
   - 우선 synthetic fact evidence를 amount-bearing line candidate에만 붙인다.
   - note-only candidate에는 붙이지 않는다.
3. tests를 추가한다.
   - 기존 statement draft tests 유지.
   - fact evidence가 revenue/current assets 등 amount-bearing line candidate에 붙는지 확인.
   - source body/quote가 evidence refs에 들어가지 않는지 확인.

## Acceptance Criteria

```powershell
python -m pytest tests\test_statement_draft.py tests\test_runtime_evidence.py tests\test_1115_review_pack.py -q
python scripts\validate_ingestion_manifest.py docs\ingestion\source_manifest.example.json
python scripts\validate_ingestion_evidence.py docs\ingestion\evidence_manifest.example.json
python scripts\quality_preflight.py --format text
git diff --check
```

## Deliverable

- updated `StatementLineCandidate`
- updated statement draft adapters/tests
- `docs/reports/2026-07-05-rt3-statement-draft-fact-evidence.md`

## 금지사항

- synthetic fact evidence를 실제 회사 공시 검증 완료 수치처럼 표현하지 않는다.
- source body, quote, raw filing, API payload를 `evidence_refs`에 넣지 않는다.
- RT3에서 answer composer는 수정하지 않는다. 이유: RT4 범위다.

