"""평가 하네스 Reporter — Markdown + HTML.

stdlib `string.Template` 만 사용 (Jinja2 불필요).
"""
from __future__ import annotations

import html
import json
from pathlib import Path
from string import Template

from .models import ItemReport, RunReport


HTML_TEMPLATE = Template("""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>K-IFRS RAG 평가 리포트 — $timestamp</title>
<style>
  body { font-family: -apple-system, 'Pretendard', 'Segoe UI', sans-serif;
         max-width: 960px; margin: 2rem auto; padding: 0 1rem;
         color: #1a1a1a; line-height: 1.6; }
  h1 { border-bottom: 2px solid #2563eb; padding-bottom: .4rem; }
  h2 { margin-top: 2.5rem; color: #2563eb; }
  h3 { margin-top: 1.5rem; font-size: 1.1rem; }
  .summary { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;
             padding: 1rem 1.5rem; margin: 1rem 0; }
  .item { border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem 1.5rem;
          margin: 1rem 0; }
  .score-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: .5rem;
                margin: .5rem 0; }
  .score-card { background: #f8fafc; padding: .6rem .8rem; border-radius: 6px;
                border-left: 4px solid #2563eb; }
  .score-card .label { font-size: .8rem; color: #64748b; }
  .score-card .value { font-size: 1.3rem; font-weight: 600; }
  .good { border-left-color: #16a34a; }
  .warn { border-left-color: #ea580c; }
  .bad { border-left-color: #dc2626; }
  details { margin: .5rem 0; }
  summary { cursor: pointer; font-weight: 500; color: #2563eb; }
  pre { background: #f1f5f9; padding: .8rem; border-radius: 6px;
        overflow-x: auto; font-size: .85rem; }
  .answer { background: #fefce8; padding: .8rem 1rem; border-radius: 6px;
            white-space: pre-wrap; font-size: .95rem; border-left: 3px solid #eab308; }
  .cite { display: inline-block; background: #dbeafe; color: #1e40af;
          padding: 1px 6px; margin: 1px; border-radius: 4px; font-family: monospace;
          font-size: .85rem; }
  .cite.miss { background: #fee2e2; color: #991b1b; }
  .cite.may { background: #ecfccb; color: #3f6212; }
  .meta { color: #64748b; font-size: .85rem; }
  table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: .9rem; }
  th, td { border: 1px solid #e2e8f0; padding: .5rem .8rem; text-align: left; }
  th { background: #f8fafc; }
</style>
</head>
<body>
<h1>K-IFRS RAG 평가 리포트</h1>
<p class="meta">생성: $timestamp · Runner: <b>$runner</b> · 문항 수: <b>$n_items</b></p>

<div class="summary">
<h2 style="margin-top:0">요약</h2>
<div class="score-grid">
  <div class="score-card $composite_class"><div class="label">Composite 평균</div><div class="value">$composite</div></div>
  <div class="score-card"><div class="label">Cite F1 평균</div><div class="value">$cite_avg</div></div>
  <div class="score-card"><div class="label">Keyword 히트율</div><div class="value">$kw_avg</div></div>
  <div class="score-card"><div class="label">GlobalRules 통과</div><div class="value">$rules_avg</div></div>
</div>
<p><b>인용 정확도</b>: must_cite 적중 $must_hit_total / $must_total · forbidden 적발 $forbid_hit_total건 · DB 미존재 인용 $db_miss_total건</p>
</div>

<h2>문항별 상세</h2>
$items_html

<h2 class="meta">방법론</h2>
<p class="meta">
Scorer 3종: <b>Cite</b>(must/may precision·recall F1 + may 가점), <b>Keyword</b>(히트율 − forbidden 감점),
<b>GlobalRules</b>(인용된 기준서·문단이 DB에 존재하는지). 각 점수 단순 평균 = composite.<br>
Runner <b>$runner</b>: $runner_desc
</p>
</body>
</html>
""")

ITEM_TEMPLATE = Template("""
<div class="item">
<h3>[$item_id] $source · $source_ref</h3>
<p><b>질문:</b> $question</p>

<div class="score-grid">
  <div class="score-card $composite_class"><div class="label">Composite</div><div class="value">$composite</div></div>
  <div class="score-card"><div class="label">Cite F1</div><div class="value">$cite_score</div></div>
  <div class="score-card"><div class="label">Keyword</div><div class="value">$kw_score</div></div>
  <div class="score-card"><div class="label">GlobalRules</div><div class="value">$rules_score</div></div>
</div>

<p><b>must_cite:</b> $must_cites<br>
<b>인용 추출:</b> $cites_extracted<br>
<b>keywords hit/miss:</b> $kw_hits / <span style="color:#dc2626">$kw_miss</span><br>
<b>forbidden hit:</b> <span style="color:#dc2626">$forbid_hits</span></p>

<details><summary>답변 원문</summary>
<div class="answer">$answer</div>
</details>

<details><summary>검색 context ($n_ctx건)</summary>
<pre>$context_preview</pre>
</details>

<details><summary>scorer 상세 JSON</summary>
<pre>$scores_json</pre>
</details>
</div>
""")


def _cite_tag(std: str, no: str, kind: str = "") -> str:
    cls = {"miss": "miss", "may": "may"}.get(kind, "")
    return f'<span class="cite {cls}">[{html.escape(std)}-{html.escape(no)}]</span>'


def _score_class(score: float) -> str:
    return "good" if score >= 0.7 else ("warn" if score >= 0.4 else "bad")


def render_html(report: RunReport) -> str:
    # 요약 집계
    cite_scores = [s.score for r in report.items for s in r.scores if s.scorer == "cite"]
    kw_scores = [s.score for r in report.items for s in r.scores if s.scorer == "keyword"]
    rule_scores = [s.score for r in report.items for s in r.scores if s.scorer == "global_rules"]

    must_total = sum(len(i.item.must_cite) for i in report.items)
    must_hit_total = 0
    forbid_hit_total = 0
    db_miss_total = 0
    for r in report.items:
        for s in r.scores:
            if s.scorer == "cite":
                must_hit_total += len(s.details.get("must_hit", []))
            elif s.scorer == "keyword":
                forbid_hit_total += len(s.details.get("forbidden_hit", []))
            elif s.scorer == "global_rules":
                db_miss_total += len(s.details.get("invalid_paragraph_no", [])) + len(s.details.get("invalid_standard", []))

    composite_avg = report.mean_composite

    runner_descs = {
        "kifrs-mcp": "본인 시스템. 질문에서 한글 토큰·기준서 번호 추출 → SQLite FTS5 trigram 검색 (top_k=8 paragraph) → 검색 context 주입 후 Claude API.",
        "baseline-noretrieval": "대조군. Claude API 단독 (검색 없음). 모델의 사전학습 지식만 사용.",
        "notebooklm-manual": "NotebookLM 수동 입력 답변.",
    }

    items_html = []
    for r in report.items:
        cite_s = next((s for s in r.scores if s.scorer == "cite"), None)
        kw_s = next((s for s in r.scores if s.scorer == "keyword"), None)
        rule_s = next((s for s in r.scores if s.scorer == "global_rules"), None)

        must_cites_html = " ".join(_cite_tag(c.standard, c.no) for c in r.item.must_cite)
        if cite_s:
            hit = set(tuple(x) for x in cite_s.details.get("must_hit", []))
            miss = set(tuple(x) for x in cite_s.details.get("must_miss", []))
            may_hit = set(tuple(x) for x in cite_s.details.get("may_hit", []))
            extracted = cite_s.details.get("cites_extracted", [])
            cites_extracted_html = " ".join(
                _cite_tag(std, no, kind=("" if (std, no) in hit else ("may" if (std, no) in may_hit else "miss")))
                for std, no in extracted
            ) or "<i>(없음)</i>"
            must_cites_html = " ".join(
                _cite_tag(c.standard, c.no, kind=("" if (c.standard, c.no) in hit else "miss"))
                for c in r.item.must_cite
            )
        else:
            cites_extracted_html = "<i>(없음)</i>"

        kw_hits = ", ".join(html.escape(k) for k in (kw_s.details.get("keywords_hit", []) if kw_s else [])) or "—"
        kw_miss = ", ".join(html.escape(k) for k in (kw_s.details.get("keywords_miss", []) if kw_s else [])) or "—"
        forbid_hits = ", ".join(html.escape(k) for k in (kw_s.details.get("forbidden_hit", []) if kw_s else [])) or "—"

        ctx_lines = []
        for c in r.run.retrieved_context[:6]:
            sec = f" ({c.get('section')})" if c.get("section") else ""
            body = (c.get("body") or "")[:180].replace("\n", " ")
            ctx_lines.append(f"[{c['standard']}-{c['no']}]{sec}  {body}…")
        ctx_preview = html.escape("\n".join(ctx_lines)) if ctx_lines else "(검색 결과 없음)"

        scores_json = json.dumps(
            {s.scorer: {"score": round(s.score, 3), "details": s.details} for s in r.scores},
            ensure_ascii=False, indent=2,
        )

        items_html.append(ITEM_TEMPLATE.substitute(
            item_id=html.escape(r.item.id),
            source=html.escape(r.item.source),
            source_ref=html.escape(r.item.source_ref),
            question=html.escape(r.item.question),
            composite=f"{r.composite:.2f}",
            composite_class=_score_class(r.composite),
            cite_score=f"{cite_s.score:.2f}" if cite_s else "—",
            kw_score=f"{kw_s.score:.2f}" if kw_s else "—",
            rules_score=f"{rule_s.score:.2f}" if rule_s else "—",
            must_cites=must_cites_html,
            cites_extracted=cites_extracted_html,
            kw_hits=kw_hits,
            kw_miss=kw_miss,
            forbid_hits=forbid_hits,
            answer=html.escape(r.run.answer if r.run.answer else f"(ERROR) {r.run.error or ''}"),
            n_ctx=len(r.run.retrieved_context),
            context_preview=ctx_preview,
            scores_json=html.escape(scores_json),
        ))

    return HTML_TEMPLATE.substitute(
        timestamp=html.escape(report.timestamp),
        runner=html.escape(report.runner),
        runner_desc=html.escape(runner_descs.get(report.runner, "")),
        n_items=len(report.items),
        composite=f"{composite_avg:.2f}",
        composite_class=_score_class(composite_avg),
        cite_avg=f"{(sum(cite_scores)/len(cite_scores)):.2f}" if cite_scores else "—",
        kw_avg=f"{(sum(kw_scores)/len(kw_scores)):.2f}" if kw_scores else "—",
        rules_avg=f"{(sum(rule_scores)/len(rule_scores)):.2f}" if rule_scores else "—",
        must_total=must_total,
        must_hit_total=must_hit_total,
        forbid_hit_total=forbid_hit_total,
        db_miss_total=db_miss_total,
        items_html="\n".join(items_html),
    )


def render_markdown(report: RunReport) -> str:
    lines = [f"# K-IFRS RAG 평가 리포트\n",
             f"- 생성: {report.timestamp}",
             f"- Runner: `{report.runner}`",
             f"- 문항 수: {len(report.items)}",
             f"- Composite 평균: **{report.mean_composite:.3f}**\n"]
    for r in report.items:
        lines.append(f"\n## {r.item.id} — {r.item.source_ref}\n")
        lines.append(f"**질문:** {r.item.question}\n")
        lines.append(f"**Composite:** {r.composite:.3f}\n")
        for s in r.scores:
            lines.append(f"- {s.scorer}: {s.score:.3f}")
        if r.run.answer:
            lines.append(f"\n**답변:**\n\n{r.run.answer}\n")
        elif r.run.error:
            lines.append(f"\n**ERROR:** {r.run.error}\n")
    return "\n".join(lines)


def write_report(report: RunReport, out_dir: Path) -> tuple[Path, Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    ts_tag = report.timestamp.replace(":", "").replace(" ", "_")
    stem = f"{report.runner}_{ts_tag}"
    html_path = out_dir / f"{stem}.html"
    md_path = out_dir / f"{stem}.md"
    json_path = out_dir / f"{stem}.json"

    html_path.write_text(render_html(report), encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")

    raw = {
        "runner": report.runner,
        "timestamp": report.timestamp,
        "mean_composite": report.mean_composite,
        "items": [
            {
                "item_id": r.item.id,
                "composite": r.composite,
                "scores": {s.scorer: {"score": s.score, "details": s.details} for s in r.scores},
                "run": {
                    "answer": r.run.answer,
                    "latency_seconds": r.run.latency_seconds,
                    "model": r.run.model,
                    "error": r.run.error,
                    "retrieved_context": [
                        {"standard": c["standard"], "no": c["no"], "section": c.get("section")}
                        for c in r.run.retrieved_context
                    ],
                },
            }
            for r in report.items
        ],
    }
    json_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
    return html_path, md_path, json_path
