#!/usr/bin/env python3
"""Pack Study4_FINAL_VERSION (working tree) into zip archives. Never deletes this folder."""
from __future__ import annotations

import csv
import hashlib
import shutil
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
STAMP = date.today().isoformat()
REL = ROOT / "release"
ZIP_OUT = REPO / "Study4_zip_packages"
PACK_NAME = f"Study4_complete_package_{STAMP}"
PACK = REL / PACK_NAME


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_tree(src: Path, dst: Path, skip_substrings=()):
    dst.mkdir(parents=True, exist_ok=True)
    for p in src.rglob("*"):
        if p.is_dir():
            continue
        rel = p.relative_to(src)
        s = str(rel)
        if any(x in s for x in skip_substrings):
            continue
        if s.endswith(".zip"):
            continue
        q = dst / rel
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, q)


def zip_folder(src: Path, zip_path: Path, arc_root: str):
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in src.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix.lower() == ".zip":
                continue
            z.write(p, arcname=str(Path(arc_root) / p.relative_to(src)))


def main():
    if REL.exists():
        shutil.rmtree(REL)
    PACK.mkdir(parents=True)

    copy_tree(ROOT / "data", PACK / "01_data", skip_substrings=("batis_chunk",))
    copy_tree(ROOT / "tables", PACK / "02_tables")
    copy_tree(ROOT / "figures", PACK / "03_figures")
    copy_tree(ROOT / "manuscript", PACK / "04_manuscript")
    copy_tree(ROOT / "scripts", PACK / "05_scripts")
    ijcm = ROOT / "00_previous_ijcm_data"
    if not ijcm.exists():
        ijcm = REPO / "Data_IJCM"
    if ijcm.exists():
        copy_tree(ijcm, PACK / "00_previous_ijcm_data")
    for name in [
        "DATA_INVENTORY.md",
        "DATA_SOURCES.md",
        "README.md",
        "00_THIS_IS_THE_FINAL_VERSION.md",
        "HOW_TO_OPEN.md",
        "results.json",
        "results_nlg.json",
        "results_industry.json",
    ]:
        src = ROOT / name
        if src.exists():
            shutil.copy2(src, PACK / name)

    fig_index = ["# Figures\n"]
    for p in sorted((PACK / "03_figures").glob("*.png")):
        fig_index.append(f"- `{p.name}`")
    (PACK / "03_figures" / "README.md").write_text("\n".join(fig_index) + "\n")

    tab_index = ["# Tables\n"]
    for p in sorted((PACK / "02_tables").glob("*.csv")):
        tab_index.append(f"- `{p.name}`")
    (PACK / "02_tables" / "README.md").write_text("\n".join(tab_index) + "\n")

    readme = f"""Study 4 complete package
========================
Built: {STAMP}

Open the git folder Study4_FINAL_VERSION/ (data/, tables/, figures/, manuscript/, scripts/).
This zip uses numbered folders for a portable snapshot.

00_previous_ijcm_data/  Occupation-paper files (Felten, ONS, APS, LLM panel). LLM scores are NOT the shock.
01_data/         Official Study 4 downloads + analysis panels (no fabricated cells)
02_tables/       All regression and descriptive tables (CSV)
03_figures/      All figures 1-21 (PNG)
04_manuscript/   Full English article + Chinese full article + tables
05_scripts/      Replication scripts

How to replicate (from Study4_FINAL_VERSION/)
---------------------------------------------
python3 scripts/run_analysis.py
python3 scripts/run_novelty_layer.py
python3 scripts/run_nlg_shock.py
python3 scripts/run_industry_economy.py

Do not treat APS SOC 2121 as causing partner-country GDP.
NACE M71 AI survey and BaTIS SJ312 do not exist.
"""
    (PACK / "README_PACKAGE.txt").write_text(readme)

    ZIP_OUT.mkdir(parents=True, exist_ok=True)
    zips_dir = ROOT / "zips"
    zips_dir.mkdir(parents=True, exist_ok=True)
    parts = [
        ("Study4_00_previous_ijcm_data.zip", PACK / "00_previous_ijcm_data", "00_previous_ijcm_data"),
        ("Study4_01_data.zip", PACK / "01_data", "01_data"),
        ("Study4_02_tables.zip", PACK / "02_tables", "02_tables"),
        ("Study4_03_figures.zip", PACK / "03_figures", "03_figures"),
        ("Study4_04_manuscript.zip", PACK / "04_manuscript", "04_manuscript"),
        ("Study4_05_scripts.zip", PACK / "05_scripts", "05_scripts"),
    ]
    zip_index = [
        "# All Study 4 zip files\n",
        "Unpacked working tree: `Study4_FINAL_VERSION/`\n",
        "Standalone zip folder: `Study4_zip_packages/`\n",
    ]
    for fname, src, arc in parts:
        if not src.exists():
            continue
        dest = ZIP_OUT / fname
        zip_folder(src, dest, arc)
        shutil.copy2(dest, zips_dir / fname)
        zip_index.append(f"- `{fname}` ({dest.stat().st_size} bytes)")
        print("part zip", dest, dest.stat().st_size)

    rows = []
    for p in sorted(PACK.rglob("*")):
        if p.is_file():
            rel = p.relative_to(PACK)
            rows.append(
                {
                    "path": str(rel).replace("\\", "/"),
                    "bytes": p.stat().st_size,
                    "sha256": sha256(p),
                }
            )
    with (PACK / "MANIFEST.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["path", "bytes", "sha256"])
        w.writeheader()
        w.writerows(rows)
    shutil.copy2(PACK / "MANIFEST.csv", ROOT / "MANIFEST.csv")

    zip_path = ZIP_OUT / f"{PACK_NAME}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in PACK.rglob("*"):
            if p.is_file():
                z.write(p, arcname=str(Path(PACK_NAME) / p.relative_to(PACK)))
    shutil.copy2(zip_path, zips_dir / zip_path.name)
    print("files", len(rows))
    print("zip", zip_path, zip_path.stat().st_size)
    zip_index.append(f"- `{PACK_NAME}.zip` ({zip_path.stat().st_size} bytes)  **complete package**")
    index_text = "\n".join(zip_index) + "\n"
    (ZIP_OUT / "ZIP_INDEX.md").write_text(index_text)
    (zips_dir / "ZIP_INDEX.md").write_text(index_text)

    zip_final = ZIP_OUT / "Study4_FINAL_VERSION"
    zip_final.mkdir(parents=True, exist_ok=True)
    for p in sorted(ZIP_OUT.glob("*.zip")):
        shutil.copy2(p, zip_final / p.name)
    shutil.copy2(ZIP_OUT / "ZIP_INDEX.md", zip_final / "ZIP_INDEX.md")
    (zip_final / "00_THIS_IS_THE_FINAL_VERSION.md").write_text(
        """# Zip copies only

The folder to open is the repository-root directory `Study4_FINAL_VERSION/`
(data, tables, figures, manuscript, scripts). This subfolder only stores zip files.
"""
    )
    print("zip folder", ZIP_OUT)
    print("local zips", zips_dir)


if __name__ == "__main__":
    main()
