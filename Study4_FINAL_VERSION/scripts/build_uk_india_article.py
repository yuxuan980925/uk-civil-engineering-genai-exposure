#!/usr/bin/env python3
"""Assemble the UK-India generative-AI article as a Word (.docx) package.

Runs the estimation script (to refresh figures and tables), converts the
English journal-format manuscript to `.docx` via pandoc, and bundles the Word
document with its figures, result tables and Markdown source into a single
self-contained folder plus a downloadable `.zip`.

Requires the ``pandoc`` CLI on PATH.

Usage:
    python3 scripts/build_uk_india_article.py
"""
from __future__ import annotations

import runpy
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # Study4_FINAL_VERSION
REPO = ROOT.parent                                  # repository root
SCRIPTS = ROOT / "scripts"
MAN = ROOT / "manuscript"
FIGS = ROOT / "figures"
TABLES = ROOT / "tables"

MD = MAN / "UK_India_GenAI_CivilEngineering.md"
DOCX_NAME = "UK_India_GenAI_CivilEngineering_EN.docx"
FIG_NAMES = ["fig_ukin_1_trade.png", "fig_ukin_2_employment.png", "fig_ukin_3_exposure.png"]
TBL_NAMES = ["tbl_ukin_model.csv", "tbl_ukin_trade_series.csv", "tbl_ukin_exposure.csv"]

STAMP = date.today().isoformat()
PKG = REPO / "UK_India_GenAI_Article"


def require_pandoc() -> None:
    if shutil.which("pandoc") is None:
        sys.exit("ERROR: pandoc not found. Install with `apt-get install -y pandoc` or `brew install pandoc`.")


def build() -> None:
    require_pandoc()

    # 1) Refresh model outputs (figures + tables).
    runpy.run_path(str(SCRIPTS / "uk_india_genai_model.py"), run_name="__main__")

    if PKG.exists():
        shutil.rmtree(PKG)
    (PKG / "figures").mkdir(parents=True)
    (PKG / "tables").mkdir(parents=True)

    # 2) Convert the English manuscript to .docx (journal format, TOC, native math).
    dst = PKG / DOCX_NAME
    subprocess.run(
        ["pandoc", str(MD), "-o", str(dst),
         "--resource-path", str(ROOT), "--standalone", "--toc", "--toc-depth=2"],
        check=True,
    )
    print(f"wrote {dst}  ({dst.stat().st_size} bytes)")

    # 3) Bundle supporting content and the Markdown source.
    for f in FIG_NAMES:
        shutil.copy2(FIGS / f, PKG / "figures" / f)
    for t in TBL_NAMES:
        shutil.copy2(TABLES / t, PKG / "tables" / t)
    shutil.copy2(MD, PKG / MD.name)

    (PKG / "README.md").write_text(
        f"""# UK–India generative-AI civil-engineering article ({STAMP})

Journal-format working paper (English) with a two-country task model and
UK–India empirical estimates.

| File | Contents |
|---|---|
| `{DOCX_NAME}` | Journal-format Word manuscript (theory model + 3 empirical models, 3 figures, 2 tables) |
| `figures/` | Model figures (trade ITS, employment DiD, exposure scatter) |
| `tables/` | Estimation output tables (CSV) |
| `{MD.name}` | Markdown source |

Rebuild: `python3 Study4_FINAL_VERSION/scripts/build_uk_india_article.py`
(estimation only: `python3 Study4_FINAL_VERSION/scripts/uk_india_genai_model.py`).
""",
        encoding="utf-8",
    )

    # 4) Zip for download.
    zip_path = shutil.make_archive(str(REPO / f"UK_India_GenAI_Article_{STAMP}"), "zip",
                                   root_dir=REPO, base_dir=PKG.name)
    print(f"zip {zip_path}  ({Path(zip_path).stat().st_size} bytes)")
    print("done")


if __name__ == "__main__":
    build()
