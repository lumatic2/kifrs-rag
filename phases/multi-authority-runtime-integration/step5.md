# RT5 — Runtime Close Demo

## Objective

`multi-authority-runtime-integration` horizon을 닫는다. 기존 PoC demo에 runtime evidence loader, review pack
external evidence panel, statement draft fact evidence refs, answer boundary section을 연결해 하나의 demo
bundle에서 확인할 수 있게 한다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-rt4-answer-boundary-composer.md` — 왜: RT5가 demo에 포함해야 하는 boundary output.
- `scripts/demo_poc.py` — 왜: 기존 public synthetic demo entrypoint.
- `kifrs/runtime/evidence.py` — 왜: demo에서 evidence bundle을 로드.
- `kifrs/runtime/answer_boundary.py` — 왜: demo boundary section 렌더링.
- `kifrs/workflows/statement_draft/adapters.py` — 왜: statement candidate evidence refs 확인.
- `tests/test_demo_poc.py` — 왜: 기존 demo regression.

## 작업

1. `scripts/demo_poc.py`에 runtime evidence bundle을 주입한다.
   - review pack 생성 시 `load_runtime_evidence()` bundle을 넘긴다.
   - statement candidates에는 fact evidence refs가 포함되게 한다.
2. demo output에 evidence boundary markdown을 추가한다.
   - 후보 파일: `evidence-boundary.md`
3. statement candidates markdown에 evidence refs 요약 column을 추가한다.
4. tests를 보강한다.
   - demo output에 external evidence section이 있는지
   - evidence boundary file이 생성되는지
   - source body/quote가 demo output에 없는지
5. horizon close report를 작성하고 ROADMAP을 갱신한다.

## Acceptance Criteria

```powershell
python scripts\demo_poc.py --scenario revenue-financing --out docs\reports\demo-poc
python -m pytest tests\test_demo_poc.py tests\test_answer_boundary.py tests\test_statement_draft.py -q
python scripts\validate_ingestion_manifest.py docs\ingestion\source_manifest.example.json
python scripts\validate_ingestion_evidence.py docs\ingestion\evidence_manifest.example.json
python scripts\quality_preflight.py --format text
git diff --check
```

## Deliverable

- updated `scripts/demo_poc.py`
- updated `tests/test_demo_poc.py`
- updated `docs/reports/demo-poc/`
- `docs/reports/2026-07-05-rt5-runtime-close-demo.md`
- ROADMAP close update

## 금지사항

- demo output에 source body, copied quote, law article text, raw filing payload를 넣지 않는다.
- K-IFRS primary evidence와 external evidence를 같은 section으로 합치지 않는다.
- 외부 API 호출을 추가하지 않는다.

