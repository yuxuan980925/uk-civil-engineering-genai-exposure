#!/usr/bin/env python3
"""Run every Study 4 experiment on the local official CSVs, then pack the complete zip."""
from __future__ import annotations

import runpy
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
ORDER = [
    "run_analysis.py",
    "run_novelty_layer.py",
    "inherit_legacy_instruments.py",
    "run_nlg_shock.py",
    "run_industry_economy.py",
    "run_focused_corridors.py",
    "build_article_assets.py",
]


def sync_manuscript_figures():
    src = ROOT / "figures"
    dst = ROOT / "manuscript" / "figures"
    dst.mkdir(parents=True, exist_ok=True)
    for p in src.glob("*.png"):
        shutil.copy2(p, dst / p.name)


def main():
    sys.path.insert(0, str(SCRIPTS))
    for name in ORDER:
        path = SCRIPTS / name
        print("=" * 60)
        print("RUN", path)
        runpy.run_path(str(path), run_name="__main__")
    sync_manuscript_figures()
    runpy.run_path(str(SCRIPTS / "build_focused_main_text.py"), run_name="__main__")
    print("=" * 60)
    print("PACK zip")
    runpy.run_path(str(SCRIPTS / "build_release_zip.py"), run_name="__main__")
    print("done")


if __name__ == "__main__":
    main()
