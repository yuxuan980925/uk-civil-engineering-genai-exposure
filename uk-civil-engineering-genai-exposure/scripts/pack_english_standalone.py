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


README = """# uk-civil-engineering-genai-exposure

Standalone **English-only** folder. There is no Chinese manuscript in this directory.

**How Does the Civil Engineering Industry Economy Change under an AI Shock? The United Kingdom’s Service Links with India and China**

Corresponding author: Yuxuan Chai (`yuxuanchai98@outlook.com`), University of Strathclyde.

## Word (open these)

| File | Contents |
|---|---|
| [Word/01_Manuscript.docx](Word/01_Manuscript.docx) | English article with five in-text figures |
| [Word/02_All_Figures.docx](Word/02_All_Figures.docx) | All 23 figures |
| [Word/03_All_Tables.docx](Word/03_All_Tables.docx) | All experiment tables |
| [Word/04_Experimental_Results.docx](Word/04_Experimental_Results.docx) | TANY / TNLG / SBS estimates |
| [Word/06_IJCM_Blinded_Manuscript.docx](Word/06_IJCM_Blinded_Manuscript.docx) | Blinded IJCM manuscript |
| [Word/08_IJCM_Tables.docx](Word/08_IJCM_Tables.docx) | Article Tables 1–6 |

Also: [Study4_Manuscript.docx](Study4_Manuscript.docx) · [Study4_Manuscript.md](Study4_Manuscript.md) · [index.html](index.html)

## Data and results (same folder)

| Path | Contents |
|---|---|
| `data/` | Retrieved Eurostat / BaTIS / SBS series |
| `Data_Study4_IJCM/` | Numbered Study 4 replication data (01–08) |
| `Data_IJCM/` | Study 1 occupation-exposure replication data (01–08) |
| `tables/` | Complete CSV tables |
| `figures/` | PNG originals |
| `results/` | `results.json`, `results_nlg.json`, `results_industry.json` |
| `IJCM_Submission/` | Title page, blinded manuscript, cover letter, Figure1–5 |

Do not open zip files in the editor.
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
<p>English-only folder. Open the <strong>Word</strong> files. There is no Chinese article here.</p>
<nav>
<a href="Word/01_Manuscript.docx">English Word</a>
<a href="Study4_Manuscript.md">English Markdown</a>
<a href="Study4_Manuscript.html">English HTML</a>
<a href="FIGURES.md">Figures</a>
<a href="tables_for_article.md">Tables</a>
<a href="Word/06_IJCM_Blinded_Manuscript.docx">IJCM blinded</a>
</nav><hr>
<ul>
<li><a href="Word/01_Manuscript.docx"><strong>English manuscript (Word)</strong></a></li>
<li><a href="Word/02_All_Figures.docx">All 23 figures (Word)</a></li>
<li><a href="Word/03_All_Tables.docx">All tables (Word)</a></li>
<li><a href="Word/04_Experimental_Results.docx">Experimental results (Word)</a></li>
<li><a href="Study4_Manuscript.md">English Markdown</a></li>
<li><a href="IJCM_Submission/01_Title_Page_Not_for_Review.docx">Title page</a></li>
<li><a href="IJCM_Submission/02_Blinded_Manuscript_for_Review.docx">Blinded manuscript</a></li>
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
        "This folder is the complete English package. Open Word/01_Manuscript.docx.\n"
        "There is no Chinese manuscript in this directory.\n",
        encoding="utf-8",
    )

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
