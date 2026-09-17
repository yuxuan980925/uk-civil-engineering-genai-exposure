#!/usr/bin/env python3
"""Rebuild the complete Study 4 folder and zip: all data, figures, tables, all manuscripts."""
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
ALL_MANUSCRIPTS = [
    "Study4_Manuscript.md",
    "article_body.md",
    "tables_for_article.md",
    "CN_full_article.md",
    "CN_novelty_and_claims.md",
]


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
    copy_tree(SRC / "scripts", OUT / "scripts", skip_substrings=("__pycache__",))
    ijcm = SRC / "00_previous_ijcm_data"
    if ijcm.exists():
        copy_tree(ijcm, OUT / "00_previous_ijcm_data")

    ms = OUT / "manuscript"
    ms.mkdir(parents=True)
    (ms / "figures").mkdir(parents=True)
    missing_ms = []
    for name in ALL_MANUSCRIPTS:
        src = SRC / "manuscript" / name
        if not src.exists():
            missing_ms.append(name)
            continue
        shutil.copy2(src, ms / name)
        shutil.copy2(src, OUT / name)
    if missing_ms:
        raise SystemExit(f"missing manuscripts: {missing_ms}")
    for p in (SRC / "figures").glob("*.png"):
        shutil.copy2(p, ms / "figures" / p.name)

    for name in [
        "DATA_INVENTORY.md",
        "DATA_SOURCES.md",
        "FIGURES.md",
        "results.json",
        "results_nlg.json",
        "results_industry.json",
        "EXPERIMENTS_RUN.md",
    ]:
        src = SRC / name
        if src.exists():
            shutil.copy2(src, OUT / name)

    n_fig = len(list((OUT / "figures").glob("*.png")))
    n_tab = len(list((OUT / "tables").glob("*.csv")))
    n_data = sum(1 for p in (OUT / "data").rglob("*") if p.is_file())
    n_ms = len(list((OUT / "manuscript").glob("*.md")))
    if n_fig < 21:
        raise SystemExit(f"figures {n_fig}")
    if n_tab < 30:
        raise SystemExit(f"tables {n_tab}")
    if n_ms < 5:
        raise SystemExit(f"manuscripts {n_ms}")

    (OUT / "README.md").write_text(
        f"""# Study 4 complete package (Article 4)

Full English article, Chinese manuscripts, all figures 1–21, all tables, all data.

Open Markdown/CSV in the editor. The zip is binary; unzip it on disk.

| Path | Contents |
|---|---|
| `Study4_Manuscript.md` | Full English article |
| `article_body.md` | English article (same series) |
| `CN_full_article.md` | Chinese full article |
| `CN_novelty_and_claims.md` | Chinese claims note |
| `tables_for_article.md` | Article tables |
| `FIGURES.md` | Figures 1–21 gallery |
| `figures/` | PNG files 1–21 |
| `tables/` | All CSV tables |
| `data/` | Official series (no fabricated cells) |
| `manuscript/` | All manuscripts + figure copies |
| `00_previous_ijcm_data/` | Previous occupation-paper files (not the DiD shock) |
| `scripts/` | Replication scripts |
| `{ZIP_NAME}` | **Complete zip of this folder (stored inside this folder)** |

Zip path:

`Study4_COMPLETE_ENGLISH/{ZIP_NAME}`

Do not treat APS SOC 2121 as causing partner-country GDP.
"""
    )
    (OUT / "ZIP_PATH.md").write_text(
        f"""# Zip path

The complete zip is **inside this folder**:

```
Study4_COMPLETE_ENGLISH/{ZIP_NAME}
```

It contains all data, all figures, all tables, and all manuscripts
(English + Chinese).
"""
    )

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

    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
    for req in ALL_MANUSCRIPTS:
        if not any(n.endswith("/manuscript/" + req) or n.endswith("/" + req) for n in names):
            raise SystemExit(f"zip missing manuscript {req}")
    n_png = sum(1 for n in names if n.endswith(".png") and "/manuscript/" not in n)
    n_csv = sum(1 for n in names if "/tables/" in n and n.endswith(".csv"))
    n_dat = sum(1 for n in names if "/data/" in n and not n.endswith("/"))
    if n_png < 21:
        raise SystemExit(f"zip figures {n_png}")
    if n_csv < 30:
        raise SystemExit(f"zip tables {n_csv}")

    shutil.copy2(zip_path, SRC / ZIP_NAME)
    (SRC / "zips").mkdir(exist_ok=True)
    shutil.copy2(zip_path, SRC / "zips" / ZIP_NAME)
    zip_out = REPO / "Study4_zip_packages"
    zip_out.mkdir(exist_ok=True)
    shutil.copy2(zip_path, zip_out / ZIP_NAME)

    print("folder", OUT)
    print("zip", zip_path, zip_path.stat().st_size)
    print("disk figures", n_fig, "tables", n_tab, "data", n_data, "manuscripts", n_ms)
    print("zip figures", n_png, "tables", n_csv, "data files", n_dat, "entries", len(names))


if __name__ == "__main__":
    main()
