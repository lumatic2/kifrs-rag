"""KASB 회계기준서 PDF 다운로더.

목록(List) → 상세(View) → 파일(commonFile/fileDownload) 3단계.
각 기준서의 "현행"(최신) PDF 한 개만 다운로드한다. 과거 개정본 수집이 필요하면
`keep_all=True` 로 호출.

실행:
  uv run python -m kifrs.download                       # K-IFRS 전체
  uv run python -m kifrs.download --category kifrs      # 동일
  uv run python -m kifrs.download --category gaap       # 일반기업회계기준
  uv run python -m kifrs.download --only 1115           # 특정 기준서
  uv run python -m kifrs.download --list-only           # 목록만 출력
"""
from __future__ import annotations
import argparse
import io
import re
import sys
import time

# Windows 콘솔(cp949)에서 유니코드 출력 허용
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

import requests

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "standards"

BASE = "https://www.kasb.or.kr"
SITE_CD = "002000000000000"

# 카테고리 → (목록 URL, gubun 코드, View URL)
CATEGORIES: dict[str, dict[str, str]] = {
    "kifrs":   {"list": "/front/board/ingAccountingList.do",  "gubun": "3001", "view": "/front/board/View3001.do"},
    "gaap":    {"list": "/front/board/List3003.do",           "gubun": "3003", "view": "/front/board/View3003.do"},
    "special": {"list": "/front/board/List3004.do",           "gubun": "3004", "view": "/front/board/View3004.do"},
    "smb":     {"list": "/front/board/List3005.do",           "gubun": "3005", "view": "/front/board/View3005.do"},
    "nonprofit": {"list": "/front/board/List3006.do",         "gubun": "3006", "view": "/front/board/View3006.do"},
    "preface": {"list": "/front/board/List3007.do",           "gubun": "3007", "view": "/front/board/View3007.do"},
    "ifrs":    {"list": "/front/board/List3013.do",           "gubun": "3013", "view": "/front/board/View3013.do"},
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8",
}


@dataclass
class Standard:
    gubun: str
    seq: str
    number: str   # 예: "1101"
    title: str    # 예: "제1101호 한국채택국제회계기준의 최초채택"


@dataclass
class FileRef:
    file_no: str
    file_seq: str
    filename: str   # 상세 페이지 title 속성에서 추출 (디코딩됨)
    ext: str        # "pdf" | "hwp"


def _slug(s: str) -> str:
    return re.sub(r"[^\w가-힣]+", "_", s).strip("_")[:40]


# ── 세션 빌더 ──────────────────────────────────────────────────────────────
def build_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(HEADERS)
    return s


# ── 1단계: 목록 파싱 ────────────────────────────────────────────────────────
_ROW_RE = re.compile(
    # <a onclick="javascript:fn_Detail('3001','59');">(<span>)?텍스트(</span>)?</a>
    r"fn_Detail\([\'\"](\d+)[\'\"]\s*,\s*[\'\"](\d+)[\'\"]\)\s*;?\s*\"[^>]*>(?:\s*<span[^>]*>)?\s*([^<]+?)\s*(?:</span>)?\s*</a>",
    re.S,
)


def fetch_list(session: requests.Session, category: str) -> list[Standard]:
    cat = CATEGORIES[category]
    r = session.get(BASE + cat["list"], timeout=30)
    r.raise_for_status()
    # 응답은 EUC-KR/CP949일 수 있음 — requests가 추정하지 못하면 명시
    if r.encoding is None or r.encoding.lower() == "iso-8859-1":
        r.encoding = "utf-8"
    html = r.text
    standards: list[Standard] = []
    seen: set[str] = set()
    for m in _ROW_RE.finditer(html):
        gubun, seq, title = m.group(1), m.group(2), m.group(3).strip()
        if seq in seen:
            continue
        seen.add(seq)
        num_m = re.search(r"제(\d{4}(?:-\d+)?)호", title)
        number = num_m.group(1) if num_m else _slug(title)
        standards.append(Standard(gubun=gubun, seq=seq, number=number, title=title))
    return standards


# ── 2단계: 상세에서 파일 참조 추출 ──────────────────────────────────────────
_FILE_DOWNLOAD_RE = re.compile(
    r'<a\s+[^>]*title="([^"]+)"[^>]*class="ico_(pdf|hwp)[^"]*"[^>]*onclick="[^"]*fileDownload\(\'(-?\d+)\',\'(\d+)\'\)',
    re.S,
)


def fetch_detail_files(session: requests.Session, std: Standard, category: str) -> list[FileRef]:
    cat = CATEGORIES[category]
    r = session.post(
        BASE + cat["view"],
        data={"siteCd": SITE_CD, "gubun": std.gubun, "accstdSeq": std.seq},
        headers={"Referer": BASE + cat["list"]},
        timeout=30,
    )
    r.raise_for_status()
    if r.encoding is None or r.encoding.lower() == "iso-8859-1":
        r.encoding = "utf-8"
    html = r.text
    refs: list[FileRef] = []
    for m in _FILE_DOWNLOAD_RE.finditer(html):
        title_attr, ext, file_no, file_seq = m.groups()
        # title 속성은 "다운로드 하려면 클릭하세요 <파일명>.pdf" 형식.
        # 파일명만 추출: 마지막 공백 이후 혹은 전체에서 확장자로 끝나는 부분
        fn_m = re.search(rf"([^\s]+\.{ext})\s*$", title_attr)
        filename = fn_m.group(1) if fn_m else title_attr.strip()
        refs.append(FileRef(file_no=file_no, file_seq=file_seq, filename=filename, ext=ext))
    return refs


# ── 3단계: PDF 다운로드 ─────────────────────────────────────────────────────
_CD_FILENAME_STAR = re.compile(r"filename\*=UTF-8''([^;]+)", re.I)
_CD_FILENAME = re.compile(r'filename="([^"]+)"', re.I)


def _filename_from_response(r: requests.Response, fallback: str) -> str:
    cd = r.headers.get("Content-Disposition", "")
    m = _CD_FILENAME_STAR.search(cd)
    if m:
        return unquote(m.group(1)).strip()
    m = _CD_FILENAME.search(cd)
    if m:
        raw = m.group(1)
        # 일부 서버는 단순 latin1 인코딩 → UTF-8 바이트를 넣기도 함
        try:
            return unquote(raw)
        except Exception:
            return raw
    return fallback


def download_file(session: requests.Session, ref: FileRef, out_dir: Path, *, referer: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    r = session.post(
        BASE + "/commonFile/fileDownload.do",
        data={"fileNo": ref.file_no, "fileSeq": ref.file_seq},
        headers={"Referer": BASE + referer},
        timeout=120,
        stream=True,
    )
    r.raise_for_status()
    filename = _filename_from_response(r, ref.filename)
    # Windows 파일명 금지 문자 정리
    safe = re.sub(r'[<>:"/\\|?*]', "_", filename).strip()
    out = out_dir / safe
    if out.exists() and out.stat().st_size > 0:
        return out  # 재실행 시 스킵
    with open(out, "wb") as f:
        for chunk in r.iter_content(chunk_size=65536):
            if chunk:
                f.write(chunk)
    return out


# ── 파이프라인 ──────────────────────────────────────────────────────────────
def run(category: str, *, only: str | None = None, keep_all: bool = False, delay: float = 1.0, list_only: bool = False) -> None:
    if category not in CATEGORIES:
        raise SystemExit(f"unknown category: {category} (choose from {list(CATEGORIES)})")

    session = build_session()
    print(f"[list] {category} …", flush=True)
    standards = fetch_list(session, category)
    print(f"[list] {len(standards)}개 기준서")

    if only:
        standards = [s for s in standards if s.number.startswith(only)]
        print(f"[filter] --only {only} → {len(standards)}개")

    if list_only:
        for s in standards:
            print(f"  {s.number:>8s}  seq={s.seq:>4s}  {s.title}")
        return

    out_base = DATA / category
    for i, std in enumerate(standards, 1):
        print(f"[{i}/{len(standards)}] {std.number} seq={std.seq} — {std.title}")
        try:
            refs = fetch_detail_files(session, std, category)
        except Exception as e:
            print(f"  ! 상세 조회 실패: {e}")
            continue
        pdfs = [r for r in refs if r.ext == "pdf"]
        if not pdfs:
            print("  (PDF 없음, 건너뜀)")
            continue
        targets = pdfs if keep_all else pdfs[:1]  # 첫 PDF = 현행
        std_dir = out_base / std.number
        for ref in targets:
            try:
                path = download_file(session, ref, std_dir, referer=CATEGORIES[category]["view"])
                size_kb = path.stat().st_size // 1024
                print(f"  ✓ {path.name} ({size_kb} KB)")
            except Exception as e:
                print(f"  ! 다운로드 실패 ({ref.file_no}/{ref.file_seq}): {e}")
        if delay:
            time.sleep(delay)


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description="KASB 회계기준서 PDF 일괄 다운로드")
    p.add_argument("--category", default="kifrs", choices=list(CATEGORIES.keys()))
    p.add_argument("--only", help="기준서번호 prefix 필터 (예: 1115)")
    p.add_argument("--keep-all", action="store_true", help="개정본 전체 다운로드 (기본: 현행만)")
    p.add_argument("--delay", type=float, default=1.0, help="요청 간 sleep(초)")
    p.add_argument("--list-only", action="store_true", help="다운로드 없이 목록만 출력")
    args = p.parse_args(argv)
    run(args.category, only=args.only, keep_all=args.keep_all, delay=args.delay, list_only=args.list_only)


if __name__ == "__main__":
    main()
