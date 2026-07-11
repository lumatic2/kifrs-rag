"""K-IFRS 기준서 PDF 파서.

PDF → {standard, paragraphs: [{no, body, appendix, ko_added, page}]} JSON.

tax-agent parse_exam_papers.py 의 extract → split → dump 구조를 포팅.
정규식은 기준서 문단 번호 체계(ROADMAP "PDF 구조 샘플링")에 맞춰 재작성.

실행:
  uv run python -m kifrs.parse --standard 1115
  uv run python -m kifrs.parse --pdf path/to/file.pdf --standard 1115
  uv run python -m kifrs.parse --all
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import pdfplumber
except ImportError:
    print("pdfplumber 없음: uv add pdfplumber", file=sys.stderr)
    sys.exit(1)

try:
    import fitz as pymupdf
    _HAS_PYMUPDF = True
except ImportError:
    _HAS_PYMUPDF = False


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "standards"
PARSED_DIR = DATA / "parsed"
TODAY = date.today().isoformat()


# ── 정규식 (ROADMAP PDF 구조 샘플링 기반) ─────────────────────────────────────
# 실측: PDF에서 "1 이 기준서의 목적은..." 처럼 번호+공백+본문이 같은 줄에 붙는다.
# 드물게 번호만 단독으로 오는 경우도 허용.
# 일반 문단: '5 본문' 또는 다계층 '5.5.15 본문' (1109호 등)
# Suffix [A-Z]? : 1109.4.1.2A, 5.7.1A 같이 개정 추가 문단 허용
RE_PARA_INLINE = re.compile(r"^(\d+(?:\.\d+)*[A-Z]?)\s+(\S.*)$")
RE_PARA_ONLY = re.compile(r"^(\d+(?:\.\d+)*[A-Z]?)$")
RE_KO_PARA = re.compile(r"^한(\d+(?:\.\d+)*[A-Z]?)(?:\s+(.*))?$")
# GAAP 부록 실무지침: "실9.1 본문", "실9.23 본문"
RE_PRAC_PARA = re.compile(r"^실(\d+(?:\.\d+)*[A-Z]?)(?:\s+(.*))?$")
# 결론도출근거(Basis for Conclusions): "BC1 본문", "BC48EA 본문", "한BC104.1 본문",
# "BCE.15 본문"(효과분석). suffix 2글자 허용(BC48EA). TOC 줄("도입 BC1~BC10")은
# 줄 시작이 아니라 매치 안 됨.
RE_BC_PARA = re.compile(r"^(한)?(BC[A-Z]?\.?\d+(?:\.\d+)*[A-Z]{0,2})(?:\s+(\S.*))?$")
# 반대의견(DO)·도입(IN) 문단 — BC 구간 안에서만 인식 (본문 오매치 방지)
RE_DOIN_PARA = re.compile(r"^((?:DO|IN)\d+[A-Z]{0,2})(?:\s+(\S.*))?$")
# 일반기업회계기준(GAAP) 스타일: "1. 본문", "14. 부채의 계정과목" (번호 뒤에 점)
RE_GAAP_PARA_INLINE = re.compile(r"^(\d{1,3})\.\s+(\S.*)$")
# GAAP 세부 문단: "(2-1) 본문", "(13-2) 본문"
RE_GAAP_SUB_INLINE = re.compile(r"^\((\d+-\d+)\)\s+(\S.*)$")
# 부록 내 문단: A1 / B5 / C12 / B5.6.2 (다계층 허용, 트레일링 점 옵션)
RE_APP_PARA_INLINE = re.compile(r"^([A-Z])(\d+(?:\.\d+)*)\.?\s+(\S.*)$")
RE_APP_PARA_ONLY = re.compile(r"^([A-Z])(\d+(?:\.\d+)*)\.?$")
RE_APPENDIX = re.compile(r"^부록\s*([A-Z]|\d+)(?:[\.\s]|$)")
RE_PAGE_FOOTER = re.compile(r"^-\s*\d+\s*-$")
# 섹션 소제목 후보: 한글(+간단 기호)만으로 구성, 구두점·종결어미 없음
RE_HEADING_CHARS = re.compile(r"^[가-힣A-Za-z0-9\s·ㆍ\(\)（）\-]+$")

# IFRS Foundation 판권/연락처 보일러플레이트
RE_BOILERPLATE = re.compile(
    r"(Westferry Circus|Canary Wharf|London E14|ifrs\.org|IFRS Foundation"
    r"|Tel:\s*\+|Fax:\s*\+|Copyright\s*©|All rights reserved|United Kingdom"
    r"|^\s*ISBN\b)",
    re.IGNORECASE,
)

# 줄 시작이 하위 호 원문자인 경우 (줄바꿈 유지해야 함)
RE_SUBCLAUSE_START = re.compile(
    r"^\s*[⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚㈎㈏㈐㈑㈒㈓㈔㈕㈖㈗㈘㈙㈚㈛]"
)


@dataclass
class Paragraph:
    no: str
    body: str = ""
    appendix: str | None = None  # "A", "B", "C" or None for 본문
    ko_added: bool = False
    page: int = 0
    section: str | None = None  # 섹션 소제목 (예: "적용범위", "수행의무의 식별")
    _buf: list[str] = field(default_factory=list, repr=False)

    def finalize(self) -> dict:
        # 스마트 조인: 연속 본문 줄은 공백 없이 이어붙이고(한글 줄바꿈),
        # ⑴⑵… 하위 호 시작 줄과 빈 줄은 줄바꿈 유지.
        out: list[str] = []
        for seg in self._buf:
            if not seg or not seg.strip():
                # K-IFRS 문단 내부는 연속 텍스트로 취급한다. 페이지 경계/공백줄은 무시.
                # 하위 호(⑴⑵…)는 자체 감지로 처리되므로 여기서 단락을 나눌 필요 없음.
                continue
            if RE_SUBCLAUSE_START.match(seg):
                if out and not out[-1].endswith("\n"):
                    out.append("\n")
                out.append(seg)
            else:
                # 하이픈 줄바꿈 복구(라틴 텍스트 대비)
                if out and out[-1].endswith("-"):
                    out[-1] = out[-1][:-1]
                    out.append(seg)
                else:
                    out.append(seg)
        body = "".join(out).strip()
        body = re.sub(r"[ \t]+\n", "\n", body)
        body = re.sub(r"\n{3,}", "\n\n", body)
        return {
            "no": self.no,
            "body": body,
            "appendix": self.appendix,
            "ko_added": self.ko_added,
            "page": self.page,
            "section": getattr(self, "section", None),
        }


# ── PDF 텍스트 추출 (페이지별) ──────────────────────────────────────────────
def extract_pages(pdf_path: Path, prefer_pymupdf: bool = False) -> list[str]:
    """페이지별 텍스트 리스트 반환. 빈 페이지는 빈 문자열.

    PDF 텍스트 추출이 비어있으면(스캔본) 같은 폴더의 `_ocr.txt` 를 단일 페이지로 사용한다.
    """
    ocr_path = pdf_path.parent / "_ocr.txt"

    def _maybe_ocr_fallback(pages: list[str]) -> list[str]:
        # 페이지 푸터(`- 2 -`)만 있고 한글 본문이 없으면 스캔본으로 간주
        joined = "\n".join(pages or [])
        hangul_count = len(re.findall(r"[가-힣]", joined))
        if hangul_count >= 50:
            return pages
        if ocr_path.exists():
            text = ocr_path.read_text(encoding="utf-8")
            print(f"  [OCR] PDF 텍스트 비어있음(한글 {hangul_count}자) → {ocr_path.name} 사용")
            return [text]
        return pages

    if prefer_pymupdf and _HAS_PYMUPDF:
        try:
            doc = pymupdf.open(str(pdf_path))
            return [page.get_text() or "" for page in doc]
        except Exception as e:
            print(f"  [WARN] PyMuPDF 실패: {e}", file=sys.stderr)

    try:
        with pdfplumber.open(pdf_path) as pdf:
            return _maybe_ocr_fallback([(p.extract_text() or "") for p in pdf.pages])
    except Exception as e:
        print(f"  [WARN] pdfplumber 실패: {e}", file=sys.stderr)
        if _HAS_PYMUPDF:
            doc = pymupdf.open(str(pdf_path))
            return _maybe_ocr_fallback([page.get_text() or "" for page in doc])
        return _maybe_ocr_fallback([])


# ── 라인 정리 ────────────────────────────────────────────────────────────
def clean_line(line: str) -> str:
    line = line.rstrip()
    stripped = line.strip()
    if not stripped:
        return ""
    if RE_PAGE_FOOTER.match(stripped):
        return ""
    if RE_BOILERPLATE.search(stripped):
        return ""
    return line


# ── 섹션 소제목 판별 ──────────────────────────────────────────────────────
_HEADING_END_BAD = ("다.", "다", ".", "?", "!", ",", "음", "임", "것")

# 조사로 시작하는 줄 = 본문 wrap 조각 ("는 금융상품", "에게 부과하는 …")
RE_JOSA_START = re.compile(r"^(?:는|은|이|가|을|를|의|와|과|로|에|에게|도|만)\s")

# 문장 종결(구두점) — 직전 본문 줄이 이걸로 끝나야 다음 줄을 소제목 후보로 인정
RE_SENTENCE_END = re.compile(r"[.)）:：;；?!」』’”]$")


def looks_like_heading(s: str) -> bool:
    """섹션 소제목 후보 판별. 매우 보수적."""
    if not s or len(s) > 30:
        return False
    if s[0].isdigit() or s.startswith("한") and len(s) < 4:
        return False
    if s.endswith(_HEADING_END_BAD):
        return False
    if not RE_HEADING_CHARS.match(s):
        return False
    if not re.search(r"[가-힣]", s):
        return False
    # 괄호 균형 — 본문 연속 줄이 소제목으로 오탐되는 경우 차단
    if s.count("(") != s.count(")") or s.count("（") != s.count("）"):
        return False
    # 너무 많은 공백(본문 조각일 가능성)
    if s.count(" ") > 4:
        return False
    return True


# ── 파라그래프 스캐너 ─────────────────────────────────────────────────────
_RE_TOC_LINE = re.compile(r"\.{3,}|\s\d+\s*$")  # "... 15" 형식


def _find_body_start(flat: list[tuple[str, int]]) -> int:
    """첫 실제 문단(한글 본문 포함) 인덱스. TOC(점선·꼬리 페이지번호) 제외."""
    for i, (line, _p) in enumerate(flat):
        s = line.strip()
        if not s or _RE_TOC_LINE.search(s):
            continue
        m = RE_PARA_INLINE.match(s) or RE_GAAP_PARA_INLINE.match(s)
        if m and re.search(r"[가-힣]{3,}", m.group(2)):
            # 다음 비어있지 않은 몇 줄도 한글 본문(TOC 꼬리 아님) 인지 확인
            ok = 0
            for j in range(i + 1, min(i + 6, len(flat))):
                ns = flat[j][0].strip()
                if not ns:
                    continue
                if _RE_TOC_LINE.search(ns):
                    ok = 0
                    break
                if re.search(r"[가-힣]", ns):
                    ok += 1
                if ok >= 2:
                    return i
    return 0


def parse_pages(pages: list[str], standard: str) -> list[dict]:
    """페이지 텍스트 → Paragraph 리스트. 플랫 라인 리스트로 변환 후 lookahead 사용."""
    # GAAP/special 기준서에만 "N. 본문", "(N-M) 본문" 패턴 활성화.
    # K-IFRS 본문에서 "(1-1)" 같은 리스트 하위항목이 오매치되는 것을 방지.
    gaap_mode = standard.startswith("gaap_") or standard.startswith("special_")

    # 1) 플랫 라인 리스트 구축 (page 번호 보존)
    flat: list[tuple[str, int]] = []
    for page_idx, page_text in enumerate(pages, start=1):
        if not page_text:
            continue
        for raw in page_text.splitlines():
            cleaned = clean_line(raw)
            flat.append((cleaned, page_idx))

    # 2) TOC 스킵: 첫 진짜 문단(1번)까지 건너뜀
    start = _find_body_start(flat)
    flat = flat[start:]

    paragraphs: list[Paragraph] = []
    current: Paragraph | None = None
    current_appendix: str | None = None
    current_section: str | None = None
    pending_section: str | None = None  # 다음 paragraph 에 붙일 섹션 소제목

    def flush():
        nonlocal current
        if current is not None:
            paragraphs.append(current)
            current = None

    def next_nonempty(i: int) -> str | None:
        for j in range(i + 1, min(i + 5, len(flat))):
            s = flat[j][0].strip()
            if s:
                return s
        return None

    for i, (line, page_idx) in enumerate(flat):
        if not line.strip():
            continue
        stripped = line.strip()

        # 부록 경계
        m_app = RE_APPENDIX.match(stripped)
        if m_app:
            flush()
            current_appendix = m_app.group(1)
            current_section = None
            pending_section = None
            header = Paragraph(
                no=f"부록{current_appendix}",
                appendix=current_appendix,
                page=page_idx,
            )
            header._buf.append(stripped)
            paragraphs.append(header)
            continue

        # 결론도출근거 문단: "BC1 본문", "한BC104.1 본문", "BCE.15 본문" (K-IFRS 계열만)
        m_bc = RE_BC_PARA.match(stripped) if not gaap_mode else None
        if m_bc:
            flush()
            # BC 구간 진입 — 이후 일반 번호("1 ...")가 BC 본문을 쪼개지 않도록 차단
            current_appendix = "BC"
            ko = bool(m_bc.group(1))
            current = Paragraph(
                no=f"{'한' if ko else ''}{m_bc.group(2)}",
                appendix="BC",
                ko_added=ko,
                page=page_idx,
                section=pending_section or current_section,
            )
            pending_section = None
            if m_bc.group(3):
                current._buf.append(m_bc.group(3))
            continue

        # 반대의견(DO)·도입(IN) 문단 — BC 구간 뒤에 이어지는 부속 문단
        m_doin = RE_DOIN_PARA.match(stripped) if current_appendix == "BC" else None
        if m_doin:
            flush()
            current = Paragraph(
                no=m_doin.group(1),
                appendix="BC",
                page=page_idx,
                section=pending_section or current_section,
            )
            pending_section = None
            if m_doin.group(2):
                current._buf.append(m_doin.group(2))
            continue

        # K-IFRS 한N.M 문단
        m_ko = RE_KO_PARA.match(stripped)
        if m_ko:
            flush()
            current = Paragraph(
                no=f"한{m_ko.group(1)}",
                appendix=current_appendix,
                ko_added=True,
                page=page_idx,
                section=pending_section or current_section,
            )
            pending_section = None
            rest = m_ko.group(2)
            if rest:
                current._buf.append(rest)
            continue

        # GAAP 실무지침 "실N.M 본문"
        m_prac = RE_PRAC_PARA.match(stripped) if gaap_mode else None
        if m_prac:
            flush()
            current = Paragraph(
                no=f"실{m_prac.group(1)}",
                appendix=current_appendix or "실무지침",
                page=page_idx,
                section=pending_section or current_section,
            )
            pending_section = None
            rest = m_prac.group(2)
            if rest:
                current._buf.append(rest)
            continue

        # 일반 문단 번호: "N 본문..." 또는 단독 "N" — 본문 영역에서만
        m_inline = RE_PARA_INLINE.match(stripped) if not current_appendix else None
        m_only = RE_PARA_ONLY.match(stripped) if (not m_inline and not current_appendix) else None
        if m_inline or m_only:
            flush()
            no = (m_inline or m_only).group(1)
            current = Paragraph(
                no=no,
                appendix=current_appendix,
                page=page_idx,
                section=pending_section or current_section,
            )
            pending_section = None
            if m_inline:
                current._buf.append(m_inline.group(2))
            continue

        # GAAP 스타일 "N. 본문" — GAAP/special 기준서 본문 영역에서만
        m_gaap = RE_GAAP_PARA_INLINE.match(stripped) if (gaap_mode and not current_appendix) else None
        if m_gaap:
            flush()
            current = Paragraph(
                no=m_gaap.group(1),
                appendix=current_appendix,
                page=page_idx,
                section=pending_section or current_section,
            )
            pending_section = None
            current._buf.append(m_gaap.group(2))
            continue

        # GAAP 세부 문단 "(N-M) 본문" — GAAP/special 기준서만
        m_gsub = RE_GAAP_SUB_INLINE.match(stripped) if (gaap_mode and not current_appendix) else None
        if m_gsub:
            flush()
            current = Paragraph(
                no=m_gsub.group(1),
                appendix=current_appendix,
                page=page_idx,
                section=pending_section or current_section,
            )
            pending_section = None
            current._buf.append(m_gsub.group(2))
            continue

        # 부록 내 A1/B5/C12 문단 (부록 컨텍스트 안에서만)
        if current_appendix:
            m_aline = RE_APP_PARA_INLINE.match(stripped)
            m_aonly = RE_APP_PARA_ONLY.match(stripped) if not m_aline else None
            if (m_aline or m_aonly) and (m_aline or m_aonly).group(1) == current_appendix:
                flush()
                letter, num = (m_aline or m_aonly).group(1), (m_aline or m_aonly).group(2)
                current = Paragraph(
                    no=f"{letter}{num}",
                    appendix=current_appendix,
                    page=page_idx,
                    section=pending_section or current_section,
                )
                pending_section = None
                if m_aline:
                    current._buf.append(m_aline.group(3))
                continue

        # 섹션 소제목 후보: lookahead 로 다음 비어있지 않은 줄이 문단 번호이면 heading 확정
        if looks_like_heading(stripped):

            def _next_is_para(nxt: str | None) -> bool:
                return bool(
                    nxt
                    and (
                        RE_PARA_INLINE.match(nxt)
                        or RE_PARA_ONLY.match(nxt)
                        or RE_KO_PARA.match(nxt)
                        or (not gaap_mode and RE_BC_PARA.match(nxt))
                        or RE_GAAP_PARA_INLINE.match(nxt)
                        or RE_GAAP_SUB_INLINE.match(nxt)
                        or (current_appendix and RE_APP_PARA_INLINE.match(nxt))
                    )
                )

            # 마지막 본문 줄 (열린 문단의 wrap 판정·후방 join 재료)
            last_buf = current._buf[-1].strip() if (current and current._buf) else ""
            before_last = (
                current._buf[-2].strip() if (current and len(current._buf) >= 2) else ""
            )

            # (1) 두 줄로 감긴 소제목 복구: 앞줄이 30자 제한에 걸려 본문에 붙은 경우
            #     — 앞줄이 heading 문자셋 + 문장 미종결 + 그 앞줄은 문장 종결이면 join
            #     (예: "…지정할 수 있는 선" + "택권" → "…선택권")
            if (
                last_buf
                and 25 <= len(last_buf) <= 40  # 전폭(wrap) 줄만 — 짧은 상위 소제목과 join 금지
                and len(last_buf + stripped) <= 60
                and RE_HEADING_CHARS.match(last_buf)
                and not last_buf.endswith(_HEADING_END_BAD)
                and not RE_SENTENCE_END.search(last_buf)
                and re.search(r"[가-힣]", last_buf)
                and (not before_last or RE_SENTENCE_END.search(before_last))
                and _next_is_para(next_nonempty(i))
            ):
                joined = last_buf + stripped
                current._buf.pop()
                flush()
                current_section = joined
                pending_section = joined
                continue

            # (2) 본문 wrap 조각 오탐 차단: 열린 문단의 마지막 줄이 전폭(wrap)인데
            #     문장 미종결이면 이 줄은 소제목이 아니라 그 문장의 연속
            #     (예: "…자동으로 환매되" + "는 금융상품" ← 정의문 조각)
            mid_sentence = (
                last_buf and len(last_buf) >= 30 and not RE_SENTENCE_END.search(last_buf)
            )
            if (
                not mid_sentence
                and not RE_JOSA_START.match(stripped)
                and _next_is_para(next_nonempty(i))
            ):
                flush()
                current_section = stripped
                pending_section = stripped
                continue

        # 본문
        if current is not None:
            current._buf.append(line)

    flush()
    return [p.finalize() for p in paragraphs]


# ── 파일 파싱 ─────────────────────────────────────────────────────────────
def parse_pdf(pdf_path: Path, standard: str) -> dict:
    print(f"  파싱: {pdf_path.name}")
    pages = extract_pages(pdf_path)
    if not any(pages):
        print("  [WARN] 텍스트 추출 실패 (스캔 이미지?)", file=sys.stderr)
        return {"standard": standard, "paragraphs": [], "source": pdf_path.name, "parsed_at": TODAY}

    paragraphs = parse_pages(pages, standard)
    return {
        "standard": standard,
        "source": pdf_path.name,
        "parsed_at": TODAY,
        "total_paragraphs": len(paragraphs),
        "paragraphs": paragraphs,
    }


def resolve_pdf(standard: str) -> Path | None:
    folder = DATA / "kifrs" / standard
    if not folder.exists():
        return None
    pdfs = sorted(folder.glob("*.pdf"))
    return pdfs[0] if pdfs else None


def main():
    ap = argparse.ArgumentParser(description="K-IFRS 기준서 PDF 파서")
    ap.add_argument("--standard", help="기준서 번호 (예: 1115)")
    ap.add_argument("--pdf", help="단일 PDF 경로 직접 지정")
    ap.add_argument("--all", action="store_true", help="data/standards/kifrs/ 전체 파싱")
    ap.add_argument("--out", help="출력 JSON 경로 (기본: data/standards/parsed/<standard>.json)")
    args = ap.parse_args()

    PARSED_DIR.mkdir(parents=True, exist_ok=True)

    targets: list[tuple[str, Path]] = []
    if args.all:
        # kifrs/: 폴더명 = standard id (예: 1115, 재무보고를_위한_개념체계)
        for d in sorted((DATA / "kifrs").glob("*")):
            if d.is_dir():
                pdfs = sorted(d.glob("*.pdf"))
                if pdfs:
                    targets.append((d.name, pdfs[0]))
        # gaap/: 폴더명 정규화 (제07장_재고자산 → gaap_07, 제01장_목적... → gaap_01)
        for d in sorted((DATA / "gaap").glob("*")):
            if not d.is_dir():
                continue
            pdfs = sorted(d.glob("*.pdf"))
            if not pdfs:
                continue
            m_ch = re.match(r"제(\d+)장", d.name)
            if m_ch:
                std_id = f"gaap_{int(m_ch.group(1)):02d}"
            else:
                # 장 번호 없는 것 (재무회계개념체계, 보험업회계처리준칙 등)
                std_id = f"gaap_{d.name}"
            targets.append((std_id, pdfs[0]))
        # special/: 기준서 번호 그대로
        for d in sorted((DATA / "special").glob("*")):
            if d.is_dir():
                pdfs = sorted(d.glob("*.pdf"))
                if pdfs:
                    targets.append((f"special_{d.name}", pdfs[0]))
    elif args.pdf:
        if not args.standard:
            print("--pdf 사용 시 --standard 필수", file=sys.stderr)
            sys.exit(2)
        targets.append((args.standard, Path(args.pdf)))
    elif args.standard:
        pdf = resolve_pdf(args.standard)
        if not pdf:
            print(f"  [ERR] {args.standard} PDF 없음", file=sys.stderr)
            sys.exit(1)
        targets.append((args.standard, pdf))
    else:
        ap.print_help()
        sys.exit(0)

    for std, pdf in targets:
        result = parse_pdf(pdf, std)
        out = Path(args.out) if args.out else (PARSED_DIR / f"{std}.json")
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  → {out.relative_to(ROOT)} ({result.get('total_paragraphs', 0)} paragraphs)")


if __name__ == "__main__":
    main()
