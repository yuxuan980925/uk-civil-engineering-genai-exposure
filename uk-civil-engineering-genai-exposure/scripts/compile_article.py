#!/usr/bin/env python3
"""Compile article Markdown to HTML and Word (.docx); fail if a figure link is missing."""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    markdown = None

CSS = """
body { font-family: Georgia, "Noto Serif CJK SC", serif; max-width: 52rem; margin: 2rem auto; padding: 0 1.2rem; line-height: 1.55; color: #111; }
img { max-width: 100%; height: auto; display: block; margin: 0.6rem 0 1.4rem; }
table { border-collapse: collapse; width: 100%; font-size: 0.88rem; margin: 1rem 0 1.6rem; }
th, td { border: 1px solid #ccc; padding: 0.35rem 0.5rem; text-align: left; }
th { background: #f4f4f4; }
code { font-size: 0.92em; }
h1, h2, h3 { line-height: 1.25; }
nav a { margin-right: 1rem; }
"""

NAV = """<nav>
<a href="index.html">Index</a>
<a href="Study4_Manuscript.html">English article</a>
<a href="CN_full_article.html">Chinese</a>
<a href="FIGURES.html">Supplementary figures</a>
<a href="tables_for_article.html">Tables</a>
</nav><hr>
"""

NAV_RE = re.compile(r"<nav>.*?</nav>\s*(<hr\s*/?>)?", re.S | re.I)

MD_FILES = [
    "Study4_Manuscript.md",
    "Study4_Concise_Manuscript.md",
    "CN_full_article.md",
    "CN_Concise_Manuscript.md",
    "FIGURES.md",
    "tables_for_article.md",
]


def img_srcs(text: str) -> list[str]:
    return re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)


def compile_one(md_path: Path, out_dir: Path) -> Path:
    text = md_path.read_text(encoding="utf-8")
    missing = []
    for src in img_srcs(text):
        p = (md_path.parent / src).resolve()
        if not p.is_file():
            missing.append(src)
    if missing:
        raise SystemExit(f"{md_path.name}: missing images: {missing}")
    if markdown is None:
        raise SystemExit("python-markdown is required: pip install markdown")
    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "nl2br"],
    )
    html = (
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
        f"<title>{md_path.stem}</title><style>{CSS}</style></head><body>"
        f"{NAV}{body}</body></html>"
    )
    dest = out_dir / (md_path.stem + ".html")
    dest.write_text(html, encoding="utf-8")
    return dest


def html_to_docx(html_path: Path, out_dir: Path) -> Path:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise SystemExit("pandoc is required to compile HTML to Word (.docx)")
    clean = NAV_RE.sub("", html_path.read_text(encoding="utf-8"))
    tmp = out_dir / f".{html_path.stem}.word.html"
    tmp.write_text(clean, encoding="utf-8")
    dest = out_dir / (html_path.stem + ".docx")
    try:
        subprocess.check_call(
            [
                pandoc,
                str(tmp),
                "-f",
                "html",
                "-t",
                "docx",
                "-o",
                str(dest),
                f"--resource-path={out_dir}",
            ],
            cwd=out_dir,
        )
    finally:
        tmp.unlink(missing_ok=True)
    if dest.stat().st_size < 10_000:
        raise SystemExit(f"{dest.name} is too small")
    return dest


def write_index(out_dir: Path) -> None:
    (out_dir / "index.html").write_text(
        f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Study 4 — compiled article</title><style>{CSS}</style></head><body>
<h1>How Does the Civil Engineering Industry Economy Change under an AI Shock? The United Kingdom’s Service Links with India and China</h1>
<p>Compiled HTML (figures load from <code>figures/</code>). In the editor, open the <strong>.md</strong> files — not the zip.</p>
<p>Word: <a href="Study4_Manuscript.docx">Study4_Manuscript.docx</a> ·
<a href="Study4_Concise_Manuscript.docx">Concise English</a> ·
<a href="CN_full_article.docx">CN_full_article.docx</a> ·
<a href="CN_Concise_Manuscript.docx">精简中文</a> ·
<a href="FIGURES.docx">FIGURES.docx</a> ·
<a href="tables_for_article.docx">tables_for_article.docx</a></p>
{NAV}
<ul>
<li><a href="Study4_Concise_Manuscript.html"><strong>Concise English manuscript</strong></a> — focused on UK, India and China</li>
<li><a href="CN_Concise_Manuscript.html"><strong>中文精简稿</strong></a> — 聚焦英国、印度和中国</li>
<li><a href="Study4_Manuscript.html">English full article</a> ← <code>Study4_Manuscript.md</code></li>
<li><a href="CN_full_article.html">Chinese article</a> ← <code>CN_full_article.md</code></li>
<li><a href="FIGURES.html">Supplementary figures</a> ← <code>FIGURES.md</code></li>
<li><a href="tables_for_article.html">All tables</a> ← <code>tables_for_article.md</code></li>
</ul>
<p>Data: <code>data/</code> · CSV tables: <code>tables/</code> · PNG: <code>figures/</code></p>
</body></html>
""",
        encoding="utf-8",
    )


def main() -> None:
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    compiled = []
    for name in MD_FILES:
        p = folder / name
        if not p.exists():
            raise SystemExit(f"missing {p}")
        compiled.append(compile_one(p, folder))
    write_index(folder)
    docx = [html_to_docx(html, folder) for html in compiled]
    n_fig = len(list((folder / "figures").glob("*.png")))
    n_tab = len(list((folder / "tables").glob("*.csv")))
    print("compiled", [p.name for p in compiled])
    print("docx", [p.name for p in docx])
    print("figures", n_fig, "tables", n_tab)
    if n_fig != 23:
        raise SystemExit(f"expected 23 PNG figures (5 in the main article), found {n_fig}")


if __name__ == "__main__":
    main()
