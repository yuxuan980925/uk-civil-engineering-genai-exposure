#!/usr/bin/env python3
"""Assemble a self-contained Study 4 zip: data, figures, tables, manuscript, scripts."""
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


def main():
    if REL.exists():
        shutil.rmtree(REL)
    PACK.mkdir(parents=True)

    copy_tree(ROOT / "data", PACK / "01_data", skip_substrings=("batis_chunk",))
    copy_tree(ROOT / "tables", PACK / "02_tables")
    copy_tree(ROOT / "figures", PACK / "03_figures")
    copy_tree(ROOT / "manuscript", PACK / "04_manuscript")
    copy_tree(ROOT / "scripts", PACK / "05_scripts")
    for name in [
        "DATA_INVENTORY.md",
        "DATA_SOURCES.md",
        "README.md",
        "results.json",
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

Folder layout
-------------
01_data/         Official downloads + analysis panel (no fabricated cells)
02_tables/       All regression and descriptive tables (CSV)
03_figures/      All figures (PNG)
04_manuscript/   English paper + Chinese claim boundary
05_scripts/      Replication: run_analysis.py then run_novelty_layer.py
DATA_INVENTORY.md  Have / missing / cannot-exist catalogue
DATA_SOURCES.md    APIs and retrieval date
results.json       Machine-readable headline estimates

How to replicate
----------------
python3 05_scripts/run_analysis.py
python3 05_scripts/run_novelty_layer.py
python3 05_scripts/run_nlg_shock.py
python3 05_scripts/run_industry_economy.py

Scripts expect this package to sit as Study4_Global_AI_Civil_Engineering_Economy/
(data/ tables/ figures/ next to scripts/). If you unzip only this package, copy
01_data -> data, 02_tables is output, or run from the git repo instead.

Claim boundary
--------------
Do not treat APS SOC 2121 as causing partner-country GDP or ISCO 2142 counts.
EU-16 Post x Delta M on Mode-1 SJ3 is a null; EU-8 is sample-dependent.
NACE M71 AI survey and BaTIS SJ312 do not exist.
"""
    (PACK / "README_PACKAGE.txt").write_text(readme)

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

    zip_path = REL / f"{PACK_NAME}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in PACK.rglob("*"):
            if p.is_file():
                z.write(p, arcname=str(Path(PACK_NAME) / p.relative_to(PACK)))
    print("files", len(rows))
    print("zip", zip_path, zip_path.stat().st_size)
    print("dir", PACK)


if __name__ == "__main__":
    main()
