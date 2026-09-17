#!/usr/bin/env python3
"""Pack every data file, table, figure, and manuscript into one complete zip."""
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
SKIP_DIR_NAMES = {"release", "zips", "__pycache__"}


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
        s = str(rel).replace("\\", "/")
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


def write_tree_into_zip(zf: zipfile.ZipFile, src: Path, arc_root: str, skip_substrings=()):
    for p in src.rglob("*"):
        if not p.is_file():
            continue
        rel = str(p.relative_to(src)).replace("\\", "/")
        if any(x in rel for x in skip_substrings):
            continue
        if rel.endswith(".zip"):
            continue
        zf.write(p, arcname=f"{arc_root}/{rel}")


def main():
    fig_dir = ROOT / "figures"
    ms_fig = ROOT / "manuscript" / "figures"
    ms_fig.mkdir(parents=True, exist_ok=True)
    pngs = sorted(fig_dir.glob("*.png"))
    tables = sorted((ROOT / "tables").glob("*.csv"))
    ms_files = sorted((ROOT / "manuscript").glob("*.md"))
    if len(pngs) < 21:
        raise SystemExit(f"expected 21 figures, found {len(pngs)}")
    if len(tables) < 30:
        raise SystemExit(f"expected 30+ tables, found {len(tables)}")
    required_ms = {
        "Study4_Manuscript.md",
        "CN_full_article.md",
        "article_body.md",
        "tables_for_article.md",
        "CN_novelty_and_claims.md",
    }
    have_ms = {p.name for p in ms_files}
    missing = required_ms - have_ms
    if missing:
        raise SystemExit(f"missing manuscripts: {missing}")
    for p in pngs:
        shutil.copy2(p, ms_fig / p.name)

    if REL.exists():
        shutil.rmtree(REL)
    PACK.mkdir(parents=True)

    # Native layout (what you open locally)
    copy_tree(ROOT / "data", PACK / "data", skip_substrings=("batis_chunk",))
    copy_tree(ROOT / "tables", PACK / "tables")
    copy_tree(ROOT / "figures", PACK / "figures")
    copy_tree(ROOT / "manuscript", PACK / "manuscript")
    copy_tree(ROOT / "scripts", PACK / "scripts")
    ijcm = ROOT / "00_previous_ijcm_data"
    if not ijcm.exists():
        ijcm = REPO / "Data_IJCM"
    if ijcm.exists():
        copy_tree(ijcm, PACK / "00_previous_ijcm_data")

    # Numbered aliases so older unzip instructions still work
    copy_tree(PACK / "data", PACK / "01_data")
    copy_tree(PACK / "tables", PACK / "02_tables")
    copy_tree(PACK / "figures", PACK / "03_figures")
    copy_tree(PACK / "manuscript", PACK / "04_manuscript")
    copy_tree(PACK / "scripts", PACK / "05_scripts")

    for name in [
        "DATA_INVENTORY.md",
        "DATA_SOURCES.md",
        "README.md",
        "00_THIS_IS_THE_FINAL_VERSION.md",
        "HOW_TO_OPEN.md",
        "00_OPEN_IN_EDITOR.md",
        "FIGURES.md",
        "README_PACKAGE.txt",
        "results.json",
        "results_nlg.json",
        "results_industry.json",
        "EXPERIMENTS_RUN.md",
    ]:
        src = ROOT / name
        if src.exists():
            shutil.copy2(src, PACK / name)

    (PACK / "03_figures" / "README.md").write_text(
        "# Figures\n\n" + "\n".join(f"- `{p.name}`" for p in pngs) + "\n"
    )
    (PACK / "figures" / "README.md").write_text(
        "# Figures\n\n" + "\n".join(f"- `{p.name}`" for p in pngs) + "\n"
    )
    (PACK / "02_tables" / "README.md").write_text(
        "# Tables\n\n" + "\n".join(f"- `{p.name}`" for p in tables) + "\n"
    )
    (PACK / "tables" / "README.md").write_text(
        "# Tables\n\n" + "\n".join(f"- `{p.name}`" for p in tables) + "\n"
    )

    (PACK / "README_PACKAGE.txt").write_text(
        f"""Study 4 COMPLETE package
========================
Built: {STAMP}

This zip contains ALL data, ALL tables, ALL figures 1-21, ALL manuscripts,
scripts, and machine-readable results. Tables and figures were generated by
running the experiment scripts on the official CSVs in data/.

Layout (same as Study4_FINAL_VERSION/)
--------------------------------------
data/          Official series + analysis panels
tables/        Every CSV table
figures/       Figures 1-21 PNG
manuscript/    Study4_Manuscript.md, article_body.md, CN_full_article.md,
               CN_novelty_and_claims.md, tables_for_article.md, plus figures/
scripts/       Replication (run_all_experiments.py)
00_previous_ijcm_data/  Occupation-paper files (not the DiD shock)
results*.json  Estimates
01_data ... 05_scripts  Numbered copies of the same files

python3 scripts/run_all_experiments.py

Do not treat APS SOC 2121 as causing partner-country GDP.
"""
    )

    rows = []
    for p in sorted(PACK.rglob("*")):
        if p.is_file():
            rel = str(p.relative_to(PACK)).replace("\\", "/")
            rows.append({"path": rel, "bytes": p.stat().st_size, "sha256": sha256(p)})
    with (PACK / "MANIFEST.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["path", "bytes", "sha256"])
        w.writeheader()
        w.writerows(rows)
    shutil.copy2(PACK / "MANIFEST.csv", ROOT / "MANIFEST.csv")

    ZIP_OUT.mkdir(parents=True, exist_ok=True)
    zips_dir = ROOT / "zips"
    zips_dir.mkdir(parents=True, exist_ok=True)

    parts = [
        ("Study4_00_previous_ijcm_data.zip", PACK / "00_previous_ijcm_data", "00_previous_ijcm_data"),
        ("Study4_01_data.zip", PACK / "data", "data"),
        ("Study4_02_tables.zip", PACK / "tables", "tables"),
        ("Study4_03_figures.zip", PACK / "figures", "figures"),
        ("Study4_04_manuscript.zip", PACK / "manuscript", "manuscript"),
        ("Study4_05_scripts.zip", PACK / "scripts", "scripts"),
    ]
    zip_index = [
        "# All Study 4 zip files\n",
        "Complete archive for download (do not open in the IDE): `zips/Study4_complete_package_*.zip`\n",
        "To read in Cursor, open `00_OPEN_IN_EDITOR.md`, `FIGURES.md`, and `manuscript/`.\n",
    ]
    for fname, src, arc in parts:
        dest = ZIP_OUT / fname
        zip_folder(src, dest, arc)
        shutil.copy2(dest, zips_dir / fname)
        zip_index.append(f"- `{fname}` ({dest.stat().st_size} bytes)")
        print("part zip", dest.name, dest.stat().st_size)

    zip_path = ZIP_OUT / f"{PACK_NAME}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in PACK.rglob("*"):
            if p.is_file():
                z.write(p, arcname=str(Path(PACK_NAME) / p.relative_to(PACK)))
    shutil.copy2(zip_path, zips_dir / zip_path.name)

    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
    n_png = sum(1 for n in names if n.endswith(".png") and "/figures/" in n and "/manuscript/" not in n and "/03_" not in n)
    n_tab = sum(1 for n in names if n.endswith(".csv") and "/tables/" in n and "/02_" not in n)
    n_ms = sum(1 for n in names if n.endswith(".md") and "/manuscript/" in n and "/04_" not in n)
    if n_png < 21:
        raise SystemExit(f"complete zip missing figures: {n_png}")
    if n_tab < 30:
        raise SystemExit(f"complete zip missing tables: {n_tab}")
    for req in required_ms:
        if not any(n.endswith("/manuscript/" + req) for n in names):
            raise SystemExit(f"complete zip missing {req}")

    zip_index.append(
        f"- `{PACK_NAME}.zip` ({zip_path.stat().st_size} bytes)  **COMPLETE: data+tables+figures+manuscripts**"
    )
    index_text = "\n".join(zip_index) + "\n"
    (ZIP_OUT / "ZIP_INDEX.md").write_text(index_text)
    (zips_dir / "ZIP_INDEX.md").write_text(index_text)
    (ROOT / "ZIP_INDEX.md").write_text(index_text)

    zip_final = ZIP_OUT / "Study4_FINAL_VERSION"
    zip_final.mkdir(parents=True, exist_ok=True)
    for p in sorted(ZIP_OUT.glob("*.zip")):
        shutil.copy2(p, zip_final / p.name)
    shutil.copy2(ZIP_OUT / "ZIP_INDEX.md", zip_final / "ZIP_INDEX.md")
    print("complete zip", zip_path, zip_path.stat().st_size)
    print("native figures in zip", n_png, "tables", n_tab, "manuscript md", n_ms)
    print("files packed", len(rows))


if __name__ == "__main__":
    main()
