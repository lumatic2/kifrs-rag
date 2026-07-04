# RT4 — Answer Boundary Composer

## Objective

primary K-IFRS evidence와 external supporting/fact evidence를 답변에서 섞지 않도록 boundary composer
helper를 만든다. 이 step은 기존 MCP/RAG answer runtime을 크게 바꾸지 않고, evidence bundle을 사람이 읽는
boundary section으로 렌더링하는 공통 helper를 만든다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-rt3-statement-draft-fact-evidence.md` — 왜: review pack/statement draft까지 evidence가 들어온 현재 상태.
- `kifrs/runtime/evidence.py` — 왜: role별 evidence bundle query helper.
- `kifrs/runtime/evidence_panel.py` — 왜: review pack panel 렌더링 경계.
- `docs/ingestion/evidence_manifest.example.json` — 왜: composer가 다룰 evidence role.
- `tests/test_runtime_evidence.py` — 왜: runtime evidence baseline tests.

## 작업

1. `kifrs/runtime/answer_boundary.py`를 추가한다.
   - `compose_evidence_boundary(bundle)` helper
   - primary evidence placeholder와 external evidence role sections를 분리한다.
2. output section을 네 그룹으로 나눈다.
   - `primary_kifrs_evidence`
   - `supporting_interpretation`
   - `legal_boundary`
   - `fact_evidence`
3. tests를 추가한다.
   - role별 section이 분리되는지
   - primary evidence가 없을 때도 external evidence가 primary로 승격되지 않는지
   - source body/quote/record payload가 출력되지 않는지

## Acceptance Criteria

```powershell
python -m pytest tests\test_answer_boundary.py tests\test_runtime_evidence.py -q
python scripts\validate_ingestion_manifest.py docs\ingestion\source_manifest.example.json
python scripts\validate_ingestion_evidence.py docs\ingestion\evidence_manifest.example.json
python scripts\quality_preflight.py --format text
git diff --check
```

## Deliverable

- `kifrs/runtime/answer_boundary.py`
- `tests/test_answer_boundary.py`
- `docs/reports/2026-07-05-rt4-answer-boundary-composer.md`

## 금지사항

- external evidence를 primary K-IFRS evidence로 승격하지 않는다.
- source body, quote, 법령 조문, 질의회신 본문을 출력하지 않는다.
- RT4에서 MCP server나 retrieval policy는 수정하지 않는다. 이유: runtime helper 먼저 안정화.

