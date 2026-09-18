#!/usr/bin/env python3
"""Create a standalone English-only folder: uk-civil-engineering-genai-exposure/"""
from __future__ import annotations

import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "Study4"
OUT = REPO / "uk-civil-engineering-genai-exposure"

SKIP_NAME_PARTS = (
    "CN_full_article",
    "CN_Concise",
    "CN_novelty",
    "02_Chinese_Manuscript",
)
SKIP_SUFFIXES = {".zip"}


def is_chinese(rel: str) -> bool:
    name = Path(rel).name
    stem = Path(rel).stem
    if name.startswith("CN_") or stem.startswith("CN_"):
        return True
    return any(part in rel or part in name for part in SKIP_NAME_PARTS)


def copy_tree(src: Path, dst: Path) -> int:
    n = 0
    for path in src.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        rel = path.relative_to(src).as_posix()
        if is_chinese(rel):
            continue
        dest = dst / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        n += 1
    return n


README = """# Open these files in the editor

Cursor cannot preview Word, zip or Excel (`binary file is not supported`). Open **Markdown / HTML / CSV** only.

**How Does the Civil Engineering Industry Economy Change under an AI Shock? The United Kingdom’s Service Links with India and China**

English-only folder. There is no Chinese manuscript here.

Corresponding author: Yuxuan Chai (`yuxuanchai98@outlook.com`), University of Strathclyde.

## Open in the editor

1. [Study4_Manuscript.md](Study4_Manuscript.md) — English article (figures load from `figures/`)
2. [Study4_Manuscript.html](Study4_Manuscript.html) — same article as HTML
3. [FIGURES.md](FIGURES.md) — all 23 figures
4. [tables_for_article.md](tables_for_article.md) — tables
5. [IJCM_Submission/02_Blinded_Manuscript_for_Review.md](IJCM_Submission/02_Blinded_Manuscript_for_Review.md) — blinded manuscript
6. [EXPERIMENTS_RUN.md](EXPERIMENTS_RUN.md) — experiment log
7. [results/results_nlg.json](results/results_nlg.json) — NLG estimates

## Data (CSV / JSON — editor can open these)

| Path | Contents |
|---|---|
| `data/` | Retrieved Eurostat / BaTIS / SBS series |
| `tables/` | Complete CSV tables |
| `figures/` | PNG figures (also preview in FIGURES.md) |
| `results/` | `results.json`, `results_nlg.json`, `results_industry.json` |
| `Data_Study4_IJCM/` | Numbered Study 4 replication data |
| `Data_IJCM/` | Study 1 occupation-exposure data |

Word `.docx` files in `Word/` are for Microsoft Word on your computer, not for Cursor.
"""

INDEX = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>uk-civil-engineering-genai-exposure — English package</title><style>
body { font-family: Georgia, serif; max-width: 52rem; margin: 2rem auto; padding: 0 1.2rem; line-height: 1.55; color: #111; }
img { max-width: 100%; height: auto; display: block; margin: 0.6rem 0 1.4rem; }
table { border-collapse: collapse; width: 100%; font-size: 0.88rem; margin: 1rem 0 1.6rem; }
th, td { border: 1px solid #ccc; padding: 0.35rem 0.5rem; text-align: left; }
th { background: #f4f4f4; }
h1, h2, h3 { line-height: 1.25; }
nav a { margin-right: 1rem; }
</style></head><body>
<h1>How Does the Civil Engineering Industry Economy Change under an AI Shock? The United Kingdom’s Service Links with India and China</h1>
<p>English-only folder. In the editor, open <strong>.md / .html / .csv</strong>. Do not open <code>.docx</code> or <code>.zip</code> (Cursor shows <em>binary file is not supported</em>).</p>
<nav>
<a href="Study4_Manuscript.md">English Markdown</a>
<a href="Study4_Manuscript.html">English HTML</a>
<a href="FIGURES.md">Figures</a>
<a href="tables_for_article.md">Tables</a>
<a href="IJCM_Submission/02_Blinded_Manuscript_for_Review.md">IJCM blinded</a>
</nav><hr>
<ul>
<li><a href="Study4_Manuscript.md"><strong>English manuscript (Markdown)</strong></a></li>
<li><a href="Study4_Manuscript.html">English compiled HTML</a></li>
<li><a href="FIGURES.md">All 23 figures</a></li>
<li><a href="tables_for_article.md">Tables</a></li>
<li><a href="EXPERIMENTS_RUN.md">Experimental results log</a></li>
<li><a href="IJCM_Submission/02_Blinded_Manuscript_for_Review.md">Blinded manuscript (Markdown)</a></li>
<li><a href="IJCM_Submission/02_Blinded_Manuscript_for_Review.html">Blinded manuscript (HTML)</a></li>
</ul>
<p>Data: <code>data/</code> · <code>Data_Study4_IJCM/</code> · <code>Data_IJCM/</code> · PNG: <code>figures/</code> · results: <code>results/</code></p>
</body></html>
"""

WORD_MAP = {
    "01_Manuscript.docx": "Word/01_English_Manuscript.docx",
    "02_All_Figures.docx": "Word/03_All_Figures.docx",
    "03_All_Tables.docx": "Word/04_All_Tables.docx",
    "04_Experimental_Results.docx": "Word/05_Experimental_Results.docx",
    "05_IJCM_Title_Page.docx": "Word/06_IJCM_Title_Page.docx",
    "06_IJCM_Blinded_Manuscript.docx": "Word/07_IJCM_Blinded_Manuscript.docx",
    "07_IJCM_Cover_Letter.docx": "Word/08_IJCM_Cover_Letter.docx",
    "08_IJCM_Tables.docx": "Word/09_IJCM_Tables.docx",
    "09_IJCM_Figure_Captions.docx": "Word/10_IJCM_Figure_Captions.docx",
    "10_IJCM_Identified_Manuscript.docx": "Word/11_IJCM_Identified_Manuscript.docx",
    "11_Supplementary_Tables.docx": "Word/12_Supplementary_Tables.docx",
}


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    n = copy_tree(SRC, OUT)
    # Study 1 English replication data
    if (REPO / "Data_IJCM").exists():
        n += copy_tree(REPO / "Data_IJCM", OUT / "Data_IJCM")
    for name in ("LICENSE", "CITATION.cff"):
        src = REPO / name
        if src.exists():
            shutil.copy2(src, OUT / name)

    # Rebuild Word/ with English filenames only (no Chinese manuscript).
    word = OUT / "Word"
    shutil.rmtree(word, ignore_errors=True)
    word.mkdir(parents=True)
    for dest_name, src_rel in WORD_MAP.items():
        src = SRC / src_rel
        if not src.exists():
            raise SystemExit(f"missing {src_rel}")
        shutil.copy2(src, word / dest_name)

    for html in OUT.rglob("*.html"):
        text = html.read_text(encoding="utf-8", errors="replace")
        text = text.replace('<li>Chinese: <code>CN_full_article.md</code></li>', "")
        text = text.replace('<a href="CN_full_article.html">Chinese</a>', "")
        text = text.replace('<a href="CN_full_article.md">中文 .md</a>', "")
        text = text.replace('<a href="CN_full_article.html">中文 HTML</a>', "")
        text = text.replace('<li><a href="CN_full_article.md"><strong>中文全文（Markdown）</strong></a></li>', "")
        text = text.replace('<li><a href="CN_full_article.html">Chinese compiled HTML</a></li>', "")
        text = text.replace(' · <a href="CN_full_article.docx">中文 Word</a>', "")
        text = text.replace('<a href="CN_Concise_Manuscript.html"><strong>中文精简稿</strong></a> — 聚焦英国、印度和中国', "")
        html.write_text(text, encoding="utf-8")

    concise = OUT / "Study4_Concise_Manuscript.md"
    if concise.exists():
        text = concise.read_text(encoding="utf-8")
        text = text.replace("- Chinese: `CN_full_article.md`\n", "")
        concise.write_text(text, encoding="utf-8")
    ms_concise = OUT / "manuscript" / "Study4_Concise_Manuscript.md"
    if ms_concise.exists():
        text = ms_concise.read_text(encoding="utf-8")
        text = text.replace("- Chinese: `CN_full_article.md`\n", "")
        ms_concise.write_text(text, encoding="utf-8")
    for name in ("PACKAGE_INVENTORY.md", "SHA256SUMS.txt", "MANIFEST.csv"):
        path = OUT / name
        if path.exists():
            lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if "CN_" not in ln]
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    res_manifest = OUT / "results" / "MANIFEST.csv"
    if res_manifest.exists():
        lines = [ln for ln in res_manifest.read_text(encoding="utf-8").splitlines() if "CN_" not in ln]
        res_manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text(README, encoding="utf-8")
    (OUT / "OPEN_IN_EDITOR.md").write_text(README, encoding="utf-8")
    (word / "README.md").write_text(README, encoding="utf-8")
    (OUT / "index.html").write_text(INDEX, encoding="utf-8")
    (OUT / "ZIP_PATH.md").write_text(
        "Do not open zip or Word files in Cursor (binary file is not supported).\n\n"
        "Open Study4_Manuscript.md, FIGURES.md and tables_for_article.md.\n",
        encoding="utf-8",
    )
    open_me = """# Open me (not Word, not zip)

Cursor cannot preview `.docx` / `.zip` / `.xlsx`.

1. [Study4_Manuscript.md](Study4_Manuscript.md)
2. [FIGURES.md](FIGURES.md)
3. [tables_for_article.md](tables_for_article.md)
4. [EXPERIMENTS_RUN.md](EXPERIMENTS_RUN.md)
5. [IJCM_Submission/02_Blinded_Manuscript_for_Review.md](IJCM_Submission/02_Blinded_Manuscript_for_Review.md)
"""
    (OUT / "00_OPEN_ME.md").write_text(open_me, encoding="utf-8")

    chinese = [p.as_posix() for p in OUT.rglob("*") if p.is_file() and is_chinese(p.relative_to(OUT).as_posix())]
    if chinese:
        raise SystemExit("Chinese files remain:\n" + "\n".join(chinese))
    required = [
        "Word/01_Manuscript.docx",
        "Word/02_All_Figures.docx",
        "Study4_Manuscript.md",
        "Study4_Manuscript.docx",
        "data/batis_uk_india_china.csv",
        "results/results_nlg.json",
        "Data_Study4_IJCM/README.txt",
        "IJCM_Submission/02_Blinded_Manuscript_for_Review.docx",
        "figures/figure22_uk_india_china_sj3.png",
    ]
    missing = [r for r in required if not (OUT / r).exists()]
    if missing:
        raise SystemExit("missing:\n" + "\n".join(missing))
    files = [p for p in OUT.rglob("*") if p.is_file()]
    pngs = list((OUT / "figures").glob("*.png"))
    print("folder", OUT)
    print("copied", n)
    print("files", len(files))
    print("figures", len(pngs))
    print("word", sorted(p.name for p in word.glob("*.docx")))


if __name__ == "__main__":
    main()
