# Step 2: statement-line-schema

Status: completed

## 읽어야 할 파일

- `docs/reports/2026-07-05-fs1-statement-draft-surface-inventory.md` — 왜: FS2 schema와 adapter 범위가 여기 정리되어 있다.
- `kifrs/workflows/disclosure/schema.py` — 왜: 공통 surface schema의 기존 스타일이다.
- `kifrs/workflows/disclosure/adapters.py` — 왜: 기준서별 review pack adapter 패턴을 재사용한다.
- `kifrs/workflows/kifrs1109/review_pack.py` — 왜: 1109 ReviewPack 필드와 journal_entry source.
- `kifrs/workflows/kifrs1115/review_pack.py` — 왜: 1115 ReviewPack 필드와 journal_entries/measurement source.
- `kifrs/workflows/kifrs1116/review_pack.py` — 왜: 1116 ReviewPack 필드와 disclosure_draft source.

## 작업

`kifrs/workflows/statement_draft/`에 `StatementLineCandidate` schema와 1109/1115/1116 adapter를 추가한다.
adapter는 review pack의 분개 line을 재무상태표/손익/OCI/note 후보로 변환하고, 사람 검토 질문을 함께
붙인다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_statement_draft.py
git diff --check
```

## 금지사항

- 회사별 TB, 계정과목 mapping table, DART 양식 rendering은 만들지 않는다. 이유: FS2는 공통 후보 schema까지만 닫는다.
- 기존 review pack dataclass 계약을 깨지 않는다.

## 완료 요약

`kifrs/workflows/statement_draft/`에 `StatementLineCandidate` schema와 1109/1115/1116 review-pack adapter를
추가했다. 새 adapter는 분개 line을 재무상태표/손익/note 후보로 바꾸고, review question과 citation을
후보에 붙인다. `tests/test_statement_draft.py` 4개와 관련 review-pack/disclosure 회귀 17개가 통과했다.
