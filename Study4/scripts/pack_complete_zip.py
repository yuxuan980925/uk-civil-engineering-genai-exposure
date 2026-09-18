#!/usr/bin/env python3
"""Pack the openable Study 4 folder into one complete zip (files at archive root)."""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import zipfile
from datetime import date
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
REPO = SRC.parent
STAMP = date.today().isoformat()
ZIP_NAME = "Study4.zip"
DATED_NAME = f"Study4_complete_package_{STAMP}.zip"
SKIP_SUFFIXES = {".zip"}
SKIP_NAMES = {".DS_Store", "Thumbs.db"}
REQUIRED = [
    "Study4_Manuscript.md",
    "Study4_Manuscript.docx",
    "CN_full_article.md",
    "CN_full_article.docx",
    "index.html",
    "FIGURES.md",
    "tables_for_article.md",
    "IJCM_Submission/01_Title_Page_Not_for_Review.docx",
    "IJCM_Submission/02_Blinded_Manuscript_for_Review.docx",
    "IJCM_Submission/03_Cover_Letter.docx",
    "IJCM_Submission/04_Tables.docx",
    "IJCM_Submission/05_Figure_Captions.docx",
    "IJCM_Submission/Figures/Figure1.png",
    "figures/figure22_uk_india_china_sj3.png",
    "figures/figure23_uk_india_china_service_growth.png",
]


def iter_files(root: Path):
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if p.name in SKIP_NAMES or p.suffix.lower() in SKIP_SUFFIXES:
            continue
        rel = p.relative_to(root).as_posix()
        if "batis_chunk" in rel or "__pycache__" in rel:
            continue
        yield p, rel


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_zip(dest: Path) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()
    n = 0
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path, rel in iter_files(SRC):
            zf.write(path, arcname=rel)
            n += 1
    return n


def main():
    missing = [r for r in REQUIRED if not (SRC / r).exists()]
    if missing:
        raise SystemExit("missing required files:\n" + "\n".join(missing))
    pngs = list((SRC / "figures").glob("*.png"))
    if len(pngs) < 23:
        raise SystemExit(f"expected 23 figures, found {len(pngs)}")

    (SRC / "ZIP_PATH.md").write_text(
        "\n".join(
            [
                "Complete Study 4 zip (download and unzip locally; do not open in the editor):",
                "",
                f"- `{SRC.name}/{ZIP_NAME}`",
                f"- `Study4_zip_packages/{ZIP_NAME}`",
                f"- `Study4_zip_packages/{DATED_NAME}`",
                "",
                "After unzipping, `Study4_Manuscript.md` is at the top of the archive.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    staging = REPO / "Study4_zip_packages" / ZIP_NAME
    n = write_zip(staging)
    subprocess.check_call(["unzip", "-t", str(staging)], stdout=subprocess.DEVNULL)

    names = set()
    with zipfile.ZipFile(staging) as zf:
        names = set(zf.namelist())
    missing_in_zip = [r for r in REQUIRED if r not in names]
    if missing_in_zip:
        raise SystemExit("zip missing:\n" + "\n".join(missing_in_zip))
    if "Study4_Manuscript.md" not in names:
        raise SystemExit("archive root must contain Study4_Manuscript.md")

    dated = REPO / "Study4_zip_packages" / DATED_NAME
    shutil.copy2(staging, dated)
    shutil.copy2(staging, SRC / ZIP_NAME)
    article = REPO / "Study4_Article_Complete"
    if article.is_dir():
        shutil.copy2(staging, article / ZIP_NAME)
    fv_zips = REPO / "Study4_FINAL_VERSION" / "zips"
    fv_zips.mkdir(parents=True, exist_ok=True)
    shutil.copy2(staging, fv_zips / ZIP_NAME)
    shutil.copy2(staging, fv_zips / DATED_NAME)

    digest = sha256(staging)
    sidecar = (
        f"SHA256 (`{ZIP_NAME}`): `{digest}`\n"
        f"Files inside: {n}\n"
        f"Size: {staging.stat().st_size} bytes\n"
    )
    (SRC / "ZIP_PATH.md").write_text(
        (SRC / "ZIP_PATH.md").read_text(encoding="utf-8") + sidecar,
        encoding="utf-8",
    )
    (REPO / "Study4_zip_packages" / "Study4.sha256").write_text(
        f"{digest}  {ZIP_NAME}\n{digest}  {DATED_NAME}\n",
        encoding="utf-8",
    )
    print("zip", staging, staging.stat().st_size)
    print("files", n)
    print("sha256", digest)
    print("root_ok", "Study4_Manuscript.md" in names)
    print("ijcm_ok", "IJCM_Submission/02_Blinded_Manuscript_for_Review.docx" in names)
    print("figures", sum(1 for x in names if x.startswith("figures/") and x.endswith(".png")))


if __name__ == "__main__":
    main()
