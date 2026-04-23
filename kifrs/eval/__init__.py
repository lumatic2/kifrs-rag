"""K-IFRS RAG 평가 하네스.

서브모듈:
- `models`: Goldset item / RunResult / ScoreResult / Report 데이터클래스
- `runners`: Runner 인터페이스 + kifrs-mcp(Claude API + store 직접) + notebooklm-manual
- `scorers`: CiteScorer, KeywordScorer, GlobalRulesScorer
- `reporter`: Markdown + HTML 리포트 생성 (stdlib string.Template)
- `harness`: 오케스트레이션 — goldset 로드 → runner 실행 → scorers → reporter
"""
