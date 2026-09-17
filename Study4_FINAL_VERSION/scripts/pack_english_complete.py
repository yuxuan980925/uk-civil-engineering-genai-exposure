#!/usr/bin/env python3
"""Build Study4_COMPLETE_ENGLISH: English article 4, all figures, all tables, zip inside the folder."""
from __future__ import annotations

import shutil
import zipfile
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = Path(__file__).resolve().parents[1]
OUT = REPO / "Study4_COMPLETE_ENGLISH"
STAMP = date.today().isoformat()
ZIP_NAME = f"Study4_Article4_complete_{STAMP}.zip"


def copy_tree(src: Path, dst: Path, skip_substrings=()):
    dst.mkdir(parents=True, exist_ok=True)
    for p in src.rglob("*"):
        if not p.is_file():
            continue
        rel = str(p.relative_to(src)).replace("\\", "/")
        if any(x in rel for x in skip_substrings):
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

    copy_tree(SRC / "data", OUT / "data", skip_substrings=("batis_chunk",))
    copy_tree(SRC / "tables", OUT / "tables")
    copy_tree(SRC / "figures", OUT / "figures")

    ms = OUT / "manuscript"
    ms.mkdir(parents=True)
    (ms / "figures").mkdir(parents=True)
    for name in ["Study4_Manuscript.md", "article_body.md", "tables_for_article.md"]:
        shutil.copy2(SRC / "manuscript" / name, ms / name)
    for p in (SRC / "figures").glob("*.png"):
        shutil.copy2(p, ms / "figures" / p.name)
        shutil.copy2(p, OUT / "figures" / p.name)
    # English article also at folder root so it opens without entering manuscript/
    shutil.copy2(SRC / "manuscript" / "Study4_Manuscript.md", OUT / "Study4_Manuscript.md")
    shutil.copy2(SRC / "manuscript" / "tables_for_article.md", OUT / "tables_for_article.md")
    shutil.copy2(SRC / "FIGURES.md", OUT / "FIGURES.md")
    for name in ["DATA_INVENTORY.md", "DATA_SOURCES.md", "results.json", "results_nlg.json", "results_industry.json"]:
        src = SRC / name
        if src.exists():
            shutil.copy2(src, OUT / name)

    n_fig = len(list((OUT / "figures").glob("*.png")))
    n_tab = len(list((OUT / "tables").glob("*.csv")))
    if n_fig < 21:
        raise SystemExit(f"figures {n_fig}")
    if n_tab < 30:
        raise SystemExit(f"tables {n_tab}")

    (OUT / "README.md").write_text(
        f"""# Study 4 complete English package

**Article 4 (English):** *How Does the Civil Engineering Industry Economy Change under an AI Shock? Evidence from a Cross-Country Stack*

This folder is the complete delivery. Open the Markdown files (not the zip) in the editor.

| Path | Contents |
|---|---|
| `Study4_Manuscript.md` | Full English article (figures and tables included) |
| `FIGURES.md` | Figures 1–21 |
| `tables_for_article.md` | Article tables in English |
| `figures/` | PNG files 1–21 |
| `tables/` | All CSV tables |
| `data/` | Official series used in the regressions |
| `manuscript/` | Same English article + figure copies |
| `{ZIP_NAME}` | **Complete zip of this folder (path is inside this folder)** |

Zip path (inside this folder):

`Study4_COMPLETE_ENGLISH/{ZIP_NAME}`

Do not treat APS SOC 2121 as causing partner-country GDP.
"""
    )
    (OUT / "ZIP_PATH.md").write_text(
        f"""# Zip path

The complete zip is stored **inside this folder**:

```
Study4_COMPLETE_ENGLISH/{ZIP_NAME}
```

Absolute path in the repository: `Study4_COMPLETE_ENGLISH/{ZIP_NAME}`

Unzip on your computer. The editor cannot preview zip files.
"""
    )

    # Zip the folder contents except any existing zip
    zip_path = OUT / ZIP_NAME
    tmp = OUT.parent / f".{ZIP_NAME}.tmp"
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in OUT.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix.lower() == ".zip":
                continue
            z.write(p, arcname=str(Path("Study4_COMPLETE_ENGLISH") / p.relative_to(OUT)))
    shutil.move(str(tmp), str(zip_path))

    # Also keep a copy in Study4_FINAL_VERSION so that working folder has the zip path
    shutil.copy2(zip_path, SRC / ZIP_NAME)
    (SRC / "zips").mkdir(exist_ok=True)
    shutil.copy2(zip_path, SRC / "zips" / ZIP_NAME)
    zip_out = REPO / "Study4_zip_packages"
    zip_out.mkdir(exist_ok=True)
    shutil.copy2(zip_path, zip_out / ZIP_NAME)

    print("folder", OUT)
    print("zip inside folder", zip_path, zip_path.stat().st_size)
    print("figures", n_fig, "tables", n_tab)


if __name__ == "__main__":
    main()
