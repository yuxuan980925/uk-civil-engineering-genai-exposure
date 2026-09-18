#!/usr/bin/env python3
"""One folder with the full article: manuscript, all figures, all tables, data, unzippable zip."""
from __future__ import annotations

import shutil
import subprocess
import sys
import hashlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = Path(__file__).resolve().parents[1]
OUT = REPO / "Study4_Article_Complete"
ZIP_NAME = "Study4.zip"

CAPTIONS = [
    (1, "figure1_eurostat_M_vs_F.png", "Eurostat enterprise AI use, EU-27, NACE M vs F."),
    (2, "figure2_uk_aps_bundle.png", "UK APS employment change, civil-adjacent SOC 2020."),
    (3, "figure3_uk_trade.png", "UK BaTIS: India SJ3, China SE, India SI."),
    (4, "figure4_event_study.png", "Event study, year × ΔM TANY."),
    (5, "figure5_ilo_M_vs_F.png", "ILO ISIC M vs F employment growth."),
    (6, "figure6_eu_mode1_vs_china.png", "EU SJ3 imports vs Chinese construction services."),
    (7, "figure7_cross_section.png", "ΔM TANY vs Δ log India SJ3."),
    (8, "figure8_loo.png", "Leave-one-importer-out, TANY."),
    (9, "figure9_m71_vs_F_gva.png", "NACE M71 vs F GVA."),
    (10, "figure10_instruments_vs_aps.png", "APS vs Eloundou and Felten AIOE."),
    (11, "figure11_aiie_construction.png", "Felten AIIE, US construction."),
    (12, "figure12_tnlg_vs_tml.png", "EU-27 NLG vs ML vs construction NLG."),
    (13, "figure13_tnlg_2024_MF.png", "2024 NLG, NACE M vs F."),
    (14, "figure14_event_study_tnlg.png", "Event study, year × ΔM TNLG."),
    (15, "figure15_cross_section_tnlg.png", "ΔTNLG vs Δ log India SJ3."),
    (16, "figure16_tnlg_by_nace.png", "EU-27 NLG by NACE."),
    (17, "figure17_sbs_turnover_m71_vs_F.png", "SBS turnover growth, M71 vs F."),
    (18, "figure18_sbs_emp_m71_vs_F.png", "SBS employment growth, M71 vs F."),
    (19, "figure19_tnlg_vs_m71_turnover.png", "ΔTNLG vs M71 turnover change."),
    (20, "figure20_m71_turnover_levels.png", "M71 turnover levels."),
    (21, "figure21_bls_naics54.png", "US CES NAICS 54 (too broad)."),
    (22, "figure22_uk_india_china_sj3.png", "UK–India and UK–China SJ3 corridors, 2019 = 100."),
    (23, "figure23_uk_india_china_service_growth.png", "UK–India and UK–China service growth by category."),
]


def copy_tree(src: Path, dst: Path, skip=()):
    dst.mkdir(parents=True, exist_ok=True)
    for p in src.rglob("*"):
        if not p.is_file():
            continue
        rel = str(p.relative_to(src)).replace("\\", "/")
        if any(s in rel for s in skip):
            continue
        if rel.endswith(".zip"):
            continue
        q = dst / rel
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, q)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    copy_tree(SRC / "data", OUT / "data", skip=("batis_chunk",))
    copy_tree(SRC / "tables", OUT / "tables")
    copy_tree(SRC / "figures", OUT / "figures")
    copy_tree(SRC / "scripts", OUT / "scripts")
    for name in [
        "results.json",
        "results_nlg.json",
        "results_industry.json",
        "EXPERIMENTS_RUN.md",
        "MANIFEST.csv",
    ]:
        if (SRC / name).exists():
            shutil.copy2(SRC / name, OUT / name)

    ms = OUT / "manuscript"
    ms.mkdir(parents=True)
    (ms / "figures").mkdir(parents=True)
    for name in [
        "Study4_Manuscript.md",
        "Study4_Concise_Manuscript.md",
        "article_body.md",
        "tables_for_article.md",
        "CN_full_article.md",
        "CN_Concise_Manuscript.md",
        "CN_novelty_and_claims.md",
    ]:
        src = SRC / "manuscript" / name
        if src.exists():
            shutil.copy2(src, ms / name)
            shutil.copy2(src, OUT / name)
    for p in (SRC / "figures").glob("*.png"):
        shutil.copy2(p, ms / "figures" / p.name)

    shutil.copy2(SRC / "manuscript" / "Study4_Manuscript.md", OUT / "Study4_Manuscript.md")

    lines = [
        "# Supplementary figures 1–23\n",
        "From: *How Does the Civil Engineering Industry Economy Change under an AI Shock? The United Kingdom’s Service Links with India and China*\n",
    ]
    for n, fn, cap in CAPTIONS:
        lines += [f"## Figure {n}\n", cap + "\n", f"![Figure {n}](figures/{fn})\n"]
    (OUT / "FIGURES.md").write_text("\n".join(lines))

    for name in ["DATA_INVENTORY.md", "DATA_SOURCES.md"]:
        if (SRC / name).exists():
            shutil.copy2(SRC / name, OUT / name)

    (OUT / "OPEN_IN_EDITOR.md").write_text(
        """# Open these files in the editor (not the zip)

After `git pull`, open:

1. [`Study4_Manuscript.md`](Study4_Manuscript.md) — primary English article, about 8,000 words
2. [`CN_full_article.md`](CN_full_article.md) — complete Chinese article
3. [`Study4_Concise_Manuscript.md`](Study4_Concise_Manuscript.md) — optional short English version
4. [`CN_Concise_Manuscript.md`](CN_Concise_Manuscript.md) — 可选中文精简稿
5. [`FIGURES.md`](FIGURES.md) — supplementary figures 1–23 (the article embeds 5)
6. [`tables_for_article.md`](tables_for_article.md) — all tables

Folders: [`figures/`](figures/) · [`tables/`](tables/) · [`data/`](data/) · [`scripts/`](scripts/)

Compiled HTML (browser): [`index.html`](index.html)

Word (from HTML): [`Study4_Manuscript.docx`](Study4_Manuscript.docx) · [`CN_full_article.docx`](CN_full_article.docx)

Package inventory: [`PACKAGE_INVENTORY.md`](PACKAGE_INVENTORY.md) · checksums: [`SHA256SUMS.txt`](SHA256SUMS.txt)

Do **not** open `Study4.zip` in Cursor. Unzip it in Finder / Explorer; the top of the archive is `Study4_Manuscript.md`.
"""
    )
    (OUT / "README.md").write_text(
        """# How Does the Civil Engineering Industry Economy Change under an AI Shock?

The United Kingdom’s Service Links with India and China — **complete article folder**

**Open in the editor (not the zip):**

- `OPEN_IN_EDITOR.md` — this folder’s entry list
- `Study4_Manuscript.docx` — English working copy used to compile this folder; the **journal submission files** are in [`../Study4_IJCM_Submission/`](../Study4_IJCM_Submission/)
- `Study4_Manuscript.md` — editor-readable English article in IJCM layout (abstract, keywords, numbered sections, disclosure, data availability, tables, figures)
- `CN_full_article.md` — Chinese companion article (not the IJCM file)
- `CN_full_article.docx` — Word, Chinese
- `Study4_Concise_Manuscript.docx` — optional short English version
- `CN_Concise_Manuscript.docx` — 可选中文精简稿
- `tables_for_article.md` — all article tables
- `FIGURES.md` — supplementary figures 1–23; only 5 are embedded in the main article
- `figures/` — PNG files
- `tables/` — CSV tables
- `data/` — official series used in the paper
- `scripts/` — all download, analysis, compilation and packaging scripts
- `results.json`, `results_nlg.json`, `results_industry.json` — machine-readable experiment results
- `EXPERIMENTS_RUN.md` — experiment record
- `index.html` — compiled HTML (figures load from `figures/`)
- `FIGURES.docx` — Word, supplementary figures 1–23
- `tables_for_article.docx` — Word, all tables
- `PACKAGE_INVENTORY.md` — package contents and file counts
- `SHA256SUMS.txt` — checksums for every packaged file except the zip itself

Zip in this folder: **`Study4.zip`**

Unzip with Finder / Explorer. After unzip you should see `Study4_Manuscript.md` at the top. Cursor cannot preview zip files.
"""
    )
    (OUT / "ZIP_PATH.md").write_text(
        "The complete zip is in this folder:\n\n`Study4_Article_Complete/Study4.zip`\n"
    )

    subprocess.check_call(
        [sys.executable, str(Path(__file__).resolve().parent / "compile_article.py"), str(OUT)]
    )

    package_files = sorted(
        p for p in OUT.rglob("*")
        if p.is_file() and p.name not in {ZIP_NAME, "PACKAGE_INVENTORY.md", "SHA256SUMS.txt"}
    )
    inventory = [
        "# Complete package inventory",
        "",
        "Primary English article: `Study4_Manuscript.docx` / `Study4_Manuscript.md` / `Study4_Manuscript.html`.",
        "",
        f"- Figures: {len(list((OUT / 'figures').glob('*.png')))} PNG",
        f"- Tables: {len(list((OUT / 'tables').glob('*.csv')))} CSV",
        f"- Data files: {len([p for p in (OUT / 'data').rglob('*') if p.is_file()])}",
        f"- Manuscript-support files: {len([p for p in (OUT / 'manuscript').rglob('*') if p.is_file()])}",
        f"- Reproduction scripts: {len([p for p in (OUT / 'scripts').rglob('*') if p.is_file()])}",
        f"- Files in package before zip: {len(package_files) + 2}",
        "",
        "## Included files",
        "",
    ]
    inventory.extend(f"- `{p.relative_to(OUT).as_posix()}`" for p in package_files)
    (OUT / "PACKAGE_INVENTORY.md").write_text("\n".join(inventory) + "\n", encoding="utf-8")

    checksum_files = sorted(
        p for p in OUT.rglob("*")
        if p.is_file() and p.name not in {ZIP_NAME, "SHA256SUMS.txt"}
    )
    checksums = []
    for p in checksum_files:
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        checksums.append(f"{digest}  {p.relative_to(OUT).as_posix()}")
    (OUT / "SHA256SUMS.txt").write_text("\n".join(checksums) + "\n", encoding="utf-8")

    zip_path = OUT / ZIP_NAME
    if zip_path.exists():
        zip_path.unlink()
    subprocess.check_call(
        [
            "zip", "-r", "-X", str(zip_path),
            "README.md", "OPEN_IN_EDITOR.md", "ZIP_PATH.md",
            "PACKAGE_INVENTORY.md", "SHA256SUMS.txt", "Study4_Manuscript.md",
            "Study4_Concise_Manuscript.md", "CN_Concise_Manuscript.md",
            "article_body.md", "tables_for_article.md", "CN_full_article.md",
            "CN_novelty_and_claims.md", "FIGURES.md",
            "DATA_INVENTORY.md", "DATA_SOURCES.md",
            "index.html", "Study4_Manuscript.html", "CN_full_article.html",
            "Study4_Concise_Manuscript.html", "CN_Concise_Manuscript.html",
            "FIGURES.html", "tables_for_article.html",
            "Study4_Manuscript.docx", "CN_full_article.docx",
            "Study4_Concise_Manuscript.docx", "CN_Concise_Manuscript.docx",
            "FIGURES.docx", "tables_for_article.docx",
            "figures", "tables", "data", "scripts", "manuscript",
            "results.json", "results_nlg.json", "results_industry.json",
            "EXPERIMENTS_RUN.md", "MANIFEST.csv",
        ],
        cwd=OUT,
    )
    subprocess.check_call(["unzip", "-t", str(zip_path)], stdout=subprocess.DEVNULL)

    print("folder", OUT)
    print("zip", zip_path, zip_path.stat().st_size)
    print("figures", len(list((OUT / "figures").glob("*.png"))))
    print("tables", len(list((OUT / "tables").glob("*.csv"))))
    print("manuscripts", [p.name for p in OUT.glob("*.md")])


if __name__ == "__main__":
    main()
