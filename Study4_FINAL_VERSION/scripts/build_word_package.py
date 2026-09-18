#!/usr/bin/env python3
"""Build Word (.docx) manuscripts and a complete self-contained content package.

Converts the English and Chinese Study 4 manuscripts (Markdown, with the 21
figures and all inline tables) into `.docx` files using pandoc, then assembles a
single folder that bundles the Word documents together with the figures, tables,
data and Markdown sources. The folder is also written as a `.zip` for download.

Requires the `pandoc` CLI on PATH (e.g. `apt-get install pandoc` or
`brew install pandoc`).

Usage:
    python3 scripts/build_word_package.py
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # Study4_FINAL_VERSION
REPO = ROOT.parent                                  # repository root
MAN = ROOT / "manuscript"
FIGS = MAN / "figures"
TABLES = ROOT / "tables"
DATA = ROOT / "data"

STAMP = date.today().isoformat()
PKG = REPO / "Study4_Word_Package"

DOCS = [
    # (markdown source, output .docx, human label)
    ("Study4_Manuscript.md", "Study4_Manuscript_EN.docx", "English manuscript"),
    ("CN_full_article.md", "Study4_Article_CN.docx", "Chinese full article"),
]


def require_pandoc() -> None:
    if shutil.which("pandoc") is None:
        sys.exit(
            "ERROR: pandoc not found on PATH.\n"
            "Install it with `apt-get install -y pandoc` (Linux) or "
            "`brew install pandoc` (macOS), then re-run."
        )


def build_docx(md_name: str, docx_name: str) -> Path:
    src = MAN / md_name
    if not src.exists():
        sys.exit(f"ERROR: manuscript source not found: {src}")
    dst = PKG / docx_name
    cmd = [
        "pandoc",
        str(src),
        "-o",
        str(dst),
        # Resolve `figures/...` image links relative to the manuscript folder.
        "--resource-path",
        str(MAN),
        "--standalone",
        "--toc",
        "--toc-depth=2",
    ]
    subprocess.run(cmd, check=True)
    print(f"wrote {dst}  ({dst.stat().st_size} bytes)")
    return dst


def copytree(src: Path, dst: Path, pattern: str = "*") -> int:
    dst.mkdir(parents=True, exist_ok=True)
    n = 0
    for p in sorted(src.glob(pattern)):
        if p.is_file():
            shutil.copy2(p, dst / p.name)
            n += 1
    return n


def write_readme() -> None:
    figs = len(list(FIGS.glob("*.png")))
    tables = len(list(TABLES.glob("*.csv")))
    data = len(list(DATA.glob("*.csv"))) + len(list(DATA.glob("*.json")))
    (PKG / "README.md").write_text(
        f"""# Study 4 — Word manuscript package ({STAMP})

Self-contained bundle for *How Does the Civil Engineering Industry Economy
Change under an AI Shock?* (Yuxuan Chai, University of Strathclyde).

## Word documents (open in Microsoft Word / Pages)

| File | Contents |
|---|---|
| `Study4_Manuscript_EN.docx` | Full English manuscript — all sections, {figs} figures embedded, all tables |
| `Study4_Article_CN.docx` | Chinese full article — all sections, {figs} figures embedded |

## Supporting content

| Folder | Contents |
|---|---|
| `figures/` | {figs} figures (PNG) |
| `tables/` | {tables} result tables (CSV) |
| `data/` | {data} source/derived datasets (CSV / JSON) |
| `source_markdown/` | Original Markdown manuscripts and table sheet |

Regenerate with `python3 Study4_FINAL_VERSION/scripts/build_word_package.py`.
""",
        encoding="utf-8",
    )
    print(f"wrote {PKG / 'README.md'}")


def main() -> None:
    require_pandoc()
    if PKG.exists():
        shutil.rmtree(PKG)
    PKG.mkdir(parents=True)

    for md_name, docx_name, _label in DOCS:
        build_docx(md_name, docx_name)

    n_fig = copytree(FIGS, PKG / "figures", "*.png")
    n_tab = copytree(TABLES, PKG / "tables", "*.csv")
    n_data = copytree(DATA, PKG / "data", "*.csv")
    n_data += copytree(DATA, PKG / "data", "*.json")

    src_md = PKG / "source_markdown"
    src_md.mkdir(parents=True, exist_ok=True)
    for name in ("Study4_Manuscript.md", "CN_full_article.md", "tables_for_article.md"):
        p = MAN / name
        if p.exists():
            shutil.copy2(p, src_md / name)

    print(f"copied {n_fig} figures, {n_tab} tables, {n_data} data files")
    write_readme()

    archive = REPO / f"Study4_Word_Package_{STAMP}"
    zip_path = shutil.make_archive(str(archive), "zip", root_dir=REPO, base_dir=PKG.name)
    print(f"zip {zip_path}  ({Path(zip_path).stat().st_size} bytes)")
    print("done")


if __name__ == "__main__":
    main()
