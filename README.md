# kifrs-rag

K-IFRS standards retrieval and MCP server prototype for evidence-grounded accounting analysis.

이 레포는 K-IFRS 기준서 원문을 직접 배포하는 레포가 아닙니다. 공개되는 범위는 RAG/MCP 서버 코드, 검색 파이프라인, 평가 하네스, 운영 문서입니다. 기준서 PDF, 파싱 텍스트, SQLite DB, 임베딩, 기출 dogfood 자료는 저작권과 사용 범위 때문에 git에서 제외됩니다.

## What It Shows

| Area | What is included |
|---|---|
| Standards retrieval | lexical, semantic, hybrid, reranked, and hierarchical retrieval experiments |
| MCP server | FastMCP tools for listing standards, searching paragraphs, and retrieving context |
| Evaluation harness | retrieval goldset runner and before/after metrics for search improvements |
| Operating notes | roadmap, backlog, and implementation notes for accounting RAG development |

## Public Boundary

Included:

- Python package code under `kifrs/`
- evaluation and validation scripts
- roadmap/backlog/docs that describe architecture and metrics
- `.gitignore` rules for protected data

Excluded:

- K-IFRS PDF files
- parsed standard text and paragraph DB dumps
- embedding indexes
- CPA exam/dogfood material
- local `.env` files and API keys

## Setup

```powershell
uv sync
```

To build a local database, place source materials in `data/` according to the project docs. `data/` is intentionally ignored and is not part of this public repository.

## Run

```powershell
uv run python -m kifrs.mcp_server
```

## Evaluation

```powershell
uv run python -m kifrs.eval.retrieval --k 20
```

Some evaluation paths require local data that is not included in the repository.

## License

Code in this repository is MIT licensed. The license does not cover third-party accounting standards, PDFs, parsed text, exam materials, or other excluded source data.

