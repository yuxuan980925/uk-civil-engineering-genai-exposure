#!/usr/bin/env python3
"""Slim package: main-text figures/tables on AI exposure and the civil industry economy."""
from __future__ import annotations

import shutil
import zipfile
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = Path(__file__).resolve().parents[1]
OUT = REPO / "Study4_COMPLETE_ENGLISH"
STAMP = date.today().isoformat()
ZIP_NAME = f"Study4_Article4_maintext_{STAMP}.zip"

FIGS = [
    "figure2_uk_aps_bundle.png",
    "figure10_instruments_vs_aps.png",
    "figure12_tnlg_vs_tml.png",
    "figure13_tnlg_2024_MF.png",
    "figure16_tnlg_by_nace.png",
    "figure15_cross_section_tnlg.png",
    "figure17_sbs_turnover_m71_vs_F.png",
    "figure19_tnlg_vs_m71_turnover.png",
]
TABLES = [
    "article_T1_exposure_crosswalk.csv",
    "article_T2_uk_aps_all_soc.csv",
    "article_T12_multi_instrument.csv",
    "article_T13_nlg_shock.csv",
    "article_T16_industry_economy.csv",
    "table_tnlg_eu27.csv",
    "table_sbs_m71_growth.csv",
    "table_eloundou_civil.csv",
    "table_nlg_identification.csv",
    "table_industry_economy.csv",
    "table_uk_aps_change.csv",
]
DATA = [
    "eloundou_occ_level.csv",
    "eurostat_ai_genai_types.csv",
    "eurostat_ai_nace_placebos.csv",
    "eurostat_sbs_M71_F_M.csv",
    "panel_eu_sj3_tnlg.csv",
]


def copyf(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    for name in FIGS:
        copyf(SRC / "figures" / name, OUT / "figures" / name)
        copyf(SRC / "figures" / name, OUT / "manuscript" / "figures" / name)
    for name in TABLES:
        copyf(SRC / "tables" / name, OUT / "tables" / name)
    for name in DATA:
        copyf(SRC / "data" / name, OUT / "data" / name)
    copyf(
        SRC / "data" / "from_study1" / "aps_employment_2021_2025.csv",
        OUT / "data" / "from_study1" / "aps_employment_2021_2025.csv",
    )
    copyf(
        SRC / "tables" / "table_batis_corridors.csv",
        OUT / "tables" / "table_batis_corridors.csv",
    )

    copyf(SRC / "manuscript" / "Study4_Main_Text.md", OUT / "Study4_Manuscript.md")
    copyf(SRC / "manuscript" / "Study4_Main_Text.md", OUT / "manuscript" / "Study4_Manuscript.md")
    copyf(SRC / "manuscript" / "CN_Main_Text.md", OUT / "CN_full_article.md")
    copyf(SRC / "manuscript" / "CN_Main_Text.md", OUT / "manuscript" / "CN_full_article.md")

    figs_md = ["# Main-text figures\n", "AI exposure and the cross-country M71 / engineering-adjacent services economy.\n"]
    captions = [
        (1, FIGS[0], "UK APS polarisation (exposure)."),
        (2, FIGS[1], "Eloundou vs Felten vs APS."),
        (3, FIGS[2], "NLG vs machine learning vs construction NLG."),
        (4, FIGS[3], "2024 NLG, NACE M vs F."),
        (5, FIGS[4], "NLG by NACE."),
        (6, FIGS[5], "TNLG vs India SJ3 (Mode 1)."),
        (7, FIGS[6], "M71 vs F turnover growth."),
        (8, FIGS[7], "TNLG vs M71 turnover."),
    ]
    for n, fn, cap in captions:
        figs_md += [f"## Figure {n}\n", cap + "\n", f"![Figure {n}](figures/{fn})\n"]
    (OUT / "FIGURES.md").write_text("\n".join(figs_md))
    shutil.copy2(OUT / "FIGURES.md", OUT / "manuscript" / "FIGURES.md")

    (OUT / "README.md").write_text(
        f"""# Study 4 main-text package (slim)

AI exposure → cross-country civil engineering **industry economy** (NACE M71, engineering-adjacent SJ3).

Open Markdown, not the zip.

| Path | Contents |
|---|---|
| `Study4_Manuscript.md` | English main text (8 figures, 6 tables) |
| `CN_full_article.md` | Chinese main text, same figures |
| `FIGURES.md` | Figures 1–8 |
| `figures/` | 8 PNGs used in the main text |
| `tables/` | CSV for those tables |
| `data/` | Series behind the main-text estimates |
| `{ZIP_NAME}` | **Zip of this folder (path is inside this folder)** |

Zip: `Study4_COMPLETE_ENGLISH/{ZIP_NAME}`
"""
    )
    (OUT / "ZIP_PATH.md").write_text(
        f"""# Zip path

```
Study4_COMPLETE_ENGLISH/{ZIP_NAME}
```
"""
    )

    zip_path = OUT / ZIP_NAME
    tmp = OUT.parent / f".{ZIP_NAME}.tmp"
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in OUT.rglob("*"):
            if p.is_file() and p.suffix.lower() != ".zip":
                z.write(p, arcname=str(Path("Study4_COMPLETE_ENGLISH") / p.relative_to(OUT)))
    shutil.move(str(tmp), str(zip_path))

    # remove old bulky zip names from FINAL if present
    for old in SRC.glob("Study4_Article4_complete_*.zip"):
        old.unlink()
    shutil.copy2(zip_path, SRC / ZIP_NAME)
    (SRC / "zips").mkdir(exist_ok=True)
    shutil.copy2(zip_path, SRC / "zips" / ZIP_NAME)
    (REPO / "Study4_zip_packages").mkdir(exist_ok=True)
    shutil.copy2(zip_path, REPO / "Study4_zip_packages" / ZIP_NAME)

    print("zip", zip_path, zip_path.stat().st_size)
    print("figures", len(list((OUT / "figures").glob("*.png"))))
    print("tables", len(list((OUT / "tables").glob("*.csv"))))


if __name__ == "__main__":
    main()
