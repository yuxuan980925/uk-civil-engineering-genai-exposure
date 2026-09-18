#!/usr/bin/env python3
"""Validate the complete Study 4 manuscript and IJCM submission package."""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
SOURCE = ROOT / "manuscript" / "Study4_Manuscript.md"
SUBMISSION = REPO / "Study4_IJCM_Submission"
DATA = REPO / "Data_Study4_IJCM"

REQUIRED_SECTIONS = [
    "## Abstract",
    "## 1. Introduction",
    "## 2. Literature review",
    "## 3. Data",
    "## 4. Empirical design",
    "## 5. Results",
    "## 6. Discussion",
    "## 7. Limitations",
    "## 8. Conclusion",
    "## Author contribution",
    "## Funding",
    "## Ethics statement",
    "## Disclosure statement",
    "## Data availability statement",
    "## References",
    "## Tables",
    "## Figure captions",
    "## Figures",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"validation failed: {message}")


def validate_markdown() -> int:
    text = SOURCE.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        require(section in text, f"missing manuscript section {section!r}")
    require(not re.search(r"\b(?:TODO|TBD|FIXME|LOREM)\b", text, re.I), "draft marker in manuscript")
    for number in range(1, 7):
        require(f"**Table {number}.**" in text, f"missing Table {number}")
    for number in range(1, 6):
        require(f"**Figure {number}.**" in text, f"missing Figure {number} caption")
    links = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    require(len(links) == 5, f"expected 5 embedded figures, found {len(links)}")
    for link in links:
        require((SOURCE.parent / link).is_file(), f"broken manuscript image link {link}")
    abstract = text.split("## Abstract", 1)[1].split("**Keywords:**", 1)[0]
    abstract_words = re.findall(r"[A-Za-z0-9Δ×β−-]+", abstract)
    require(150 <= len(abstract_words) <= 250, f"abstract has {len(abstract_words)} words")
    require("do not directly identify GATS modes" in text, "BaTIS mode-of-supply limitation absent")
    return 1 + len(REQUIRED_SECTIONS) + 6 + 5 + len(links)


def validate_data() -> int:
    checked = 0
    for name in ("results.json", "results_nlg.json", "results_industry.json"):
        path = ROOT / name
        require(path.is_file(), f"missing {path}")
        json.loads(path.read_text(encoding="utf-8"))
        checked += 1
    for number in range(1, 7):
        path = DATA / "06_tables" / f"Table{number}.csv"
        require(path.is_file() and path.stat().st_size > 0, f"missing or empty {path}")
        checked += 1
    corridor = DATA / "03_trade" / "batis_uk_india_china.csv"
    require(corridor.is_file(), "missing focused UK–India/China corridor data")
    rows = corridor.read_text(encoding="utf-8").splitlines()
    require(len(rows) == 121, f"expected header + 120 corridor rows, found {len(rows)}")
    return checked + 1


def validate_submission() -> int:
    required = [
        "00_Manuscript_as_Submitted.docx",
        "00_Manuscript_as_Submitted.md",
        "01_Title_Page_Not_for_Review.docx",
        "02_Blinded_Manuscript_for_Review.docx",
        "02_Blinded_Manuscript_for_Review.md",
        "03_Cover_Letter.docx",
        "04_Tables.docx",
        "05_Figure_Captions.docx",
        "README_SUBMISSION.md",
        "FORMAT_CHECK.txt",
        "PACKAGE_INVENTORY.md",
        "SHA256SUMS.txt",
        "Study4_IJCM_Submission.zip",
    ]
    for relative in required:
        path = SUBMISSION / relative
        require(path.is_file() and path.stat().st_size > 0, f"missing or empty {path}")

    blinded = (SUBMISSION / "02_Blinded_Manuscript_for_Review.md").read_text(encoding="utf-8")
    require(not re.search(r"Yuxuan Chai|Strathclyde|yuxuanchai98", blinded, re.I),
            "identity remains in blinded manuscript")
    require(
        not re.search(r"(?:Indian|pooled) Mode-1|Mode-3 construction", blinded, re.I),
        "unsupported GATS mode claim remains",
    )

    for number in range(1, 6):
        path = SUBMISSION / "Figures" / f"Figure{number}.png"
        require(path.is_file(), f"missing {path}")
        with Image.open(path) as image:
            dpi = image.info.get("dpi", (0, 0))
            require(min(dpi) >= 299, f"{path.name} is below 300 dpi: {dpi}")

    checksum_lines = (SUBMISSION / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
    for line in checksum_lines:
        expected, relative = line.split("  ", 1)
        path = SUBMISSION / relative
        require(path.is_file(), f"checksummed file missing: {relative}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == expected, f"checksum mismatch: {relative}")

    with zipfile.ZipFile(SUBMISSION / "Study4_IJCM_Submission.zip") as archive:
        require(archive.testzip() is None, "submission zip contains a corrupt member")
        names = set(archive.namelist())
        require("02_Blinded_Manuscript_for_Review.docx" in names,
                "blinded manuscript absent from submission zip")

    return len(required) + 1 + 5 + len(checksum_lines) + 1


def main() -> None:
    checks = validate_markdown() + validate_data() + validate_submission()
    print(f"Study 4 validation passed ({checks} checks).")


if __name__ == "__main__":
    main()
