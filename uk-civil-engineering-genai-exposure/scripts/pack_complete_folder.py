#!/usr/bin/env python3
"""Assemble a complete, openable Study 4 folder (no zip required)."""
from __future__ import annotations

import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = Path(__file__).resolve().parents[1]
OUT = REPO / "Study4"
DATA = REPO / "Data_Study4_IJCM"
SKIP_NAMES = {".DS_Store", "Thumbs.db"}
SKIP_SUFFIXES = {".zip"}


def copy_tree(src: Path, dst: Path) -> int:
    n = 0
    if not src.exists():
        return 0
    dst.mkdir(parents=True, exist_ok=True)
    for p in src.rglob("*"):
        if not p.is_file():
            continue
        if p.name in SKIP_NAMES or p.suffix.lower() in SKIP_SUFFIXES:
            continue
        rel = p.relative_to(src)
        q = dst / rel
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, q)
        n += 1
    return n


README = """# Study 4 — complete folder

**How Does the Civil Engineering Industry Economy Change under an AI Shock? The United Kingdom’s Service Links with India and China**

This folder is the **complete Study 4 package**. Open the files here. Do not open a zip in the editor.

## Open these

1. [Study4_Manuscript.md](Study4_Manuscript.md) — English article
2. [Study4_Manuscript.html](Study4_Manuscript.html) — English HTML (figures from `figures/`)
3. [CN_full_article.md](CN_full_article.md) — 中文全文
4. [CN_full_article.html](CN_full_article.html) — 中文 HTML
5. [index.html](index.html) — folder index
6. [FIGURES.md](FIGURES.md) — supplementary figures 1–23
7. [tables_for_article.md](tables_for_article.md) — supplementary tables

## Word / IJCM upload

- [IJCM_Submission/01_Title_Page_Not_for_Review.docx](IJCM_Submission/01_Title_Page_Not_for_Review.docx)
- [IJCM_Submission/02_Blinded_Manuscript_for_Review.docx](IJCM_Submission/02_Blinded_Manuscript_for_Review.docx)
- [IJCM_Submission/03_Cover_Letter.docx](IJCM_Submission/03_Cover_Letter.docx)
- [IJCM_Submission/04_Tables.docx](IJCM_Submission/04_Tables.docx)
- [IJCM_Submission/05_Figure_Captions.docx](IJCM_Submission/05_Figure_Captions.docx)
- [Study4_Manuscript.docx](Study4_Manuscript.docx)
- [CN_full_article.docx](CN_full_article.docx)

## Folders

| Path | Contents |
|---|---|
| `figures/` | PNG figures used by the articles |
| `tables/` | CSV tables |
| `data/` | Retrieved Eurostat / BaTIS / SBS series |
| `Data_Study4_IJCM/` | Numbered replication data (01–08), Study 1 layout |
| `IJCM_Submission/` | Title page, blinded manuscript, cover letter, 300 dpi Figure1–5 |
| `scripts/` | Replication scripts |

Corresponding author: Yuxuan Chai (`yuxuanchai98@outlook.com`), University of Strathclyde.
"""


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    n_src = copy_tree(SRC, OUT)
    n_data = copy_tree(DATA, OUT / "Data_Study4_IJCM")
    n_ijcm_data = copy_tree(DATA, OUT / "IJCM_Submission" / "Data_Study4_IJCM")

    (OUT / "README.md").write_text(README, encoding="utf-8")
    (OUT / "OPEN_IN_EDITOR.md").write_text(README, encoding="utf-8")

    required = [
        "Study4_Manuscript.md",
        "CN_full_article.md",
        "index.html",
        "figures/figure22_uk_india_china_sj3.png",
        "IJCM_Submission/02_Blinded_Manuscript_for_Review.docx",
        "IJCM_Submission/Figures/Figure1.png",
        "Data_Study4_IJCM/README.txt",
        "IJCM_Submission/Data_Study4_IJCM/README.txt",
    ]
    missing = [r for r in required if not (OUT / r).exists()]
    if missing:
        raise SystemExit("missing:\n" + "\n".join(missing))

    files = [p for p in OUT.rglob("*") if p.is_file()]
    pngs = list((OUT / "figures").glob("*.png"))
    print("folder", OUT)
    print("copied_from_article", n_src)
    print("copied_data", n_data, n_ijcm_data)
    print("files", len(files))
    print("figures", len(pngs))
    if len(pngs) < 23:
        raise SystemExit(f"expected 23 figures, found {len(pngs)}")


if __name__ == "__main__":
    main()
