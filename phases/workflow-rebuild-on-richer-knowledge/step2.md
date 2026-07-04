# Step WR2: Source-Aware Review Pack Analyzer

## 읽어야 할 파일

- `kifrs/workflows/kifrs1109/review_pack.py` - 왜: 1109 pack 필드와 external evidence 연결 방식을 분석한다.
- `kifrs/workflows/kifrs1115/review_pack.py` - 왜: 1115 pack 필드와 citation 수집 방식을 분석한다.
- `kifrs/workflows/kifrs1116/review_pack.py` - 왜: 1116 pack 필드와 disclosure/citation 연결 방식을 분석한다.
- `kifrs/runtime/evidence.py` - 왜: runtime evidence bundle과 public-safe reference dict 계약을 재사용한다.
- `tests/test_1109_review_pack.py`, `tests/test_1115_review_pack.py`, `tests/test_1116_review_pack.py` - 왜: 기존 review pack contract를 깨지 않는다.

## 작업

공통 analyzer `kifrs/workflows/source_aware_rebuild.py`를 추가한다. 이 모듈은 review pack 객체를
`SourceAwarePackSummary`로 변환하고, 1109/1115/1116 기본 fixture 전체에 대해
`SourceAwareRebuildReport`를 생성한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_source_aware_rebuild.py -q
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. analyzer output에 `body`, `text`, `content`, `source_body`, `full_text` 키가 없는지 테스트한다.
3. `phases/workflow-rebuild-on-richer-knowledge/index.json`의 WR2를 completed로 업데이트한다.

## 금지사항

- external evidence를 primary K-IFRS evidence로 승격하지 않는다.
- raw source body를 summary/report에 포함하지 않는다.
- 기존 1109/1115/1116 판단 로직을 수정하지 않는다.
