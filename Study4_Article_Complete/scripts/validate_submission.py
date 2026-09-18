#!/usr/bin/env python3
"""Validate the complete Study 4 manuscript and IJCM submission package."""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
SOURCE = ROOT / "manuscript" / "Study4_Manuscript.md"
SUBMISSION = REPO / "Study4_IJCM_Submission"
DATA = REPO / "Data_Study4_IJCM"
ARTICLE = REPO / "Study4_Article_Complete"
OPENABLE = REPO / "Study4_Global_AI_Civil_Engineering_Economy"
DELIVERY = REPO / "uk-civil-engineering-genai-exposure"

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


def docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml")
    root = ET.fromstring(xml)
    return " ".join(node.text or "" for node in root.iter() if node.tag.endswith("}t"))


def docx_structure(path: Path) -> tuple[int, int]:
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml")
        media = [name for name in archive.namelist() if name.startswith("word/media/")]
    root = ET.fromstring(xml)
    tables = sum(1 for node in root.iter() if node.tag.endswith("}tbl"))
    return tables, len(media)


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


def validate_copies() -> int:
    source_text = SOURCE.read_text(encoding="utf-8")
    copies = [
        ARTICLE / "Study4_Manuscript.md",
        OPENABLE / "Study4_Manuscript.md",
        SUBMISSION / "00_Manuscript_as_Submitted.md",
        OPENABLE / "IJCM_Submission" / "00_Manuscript_as_Submitted.md",
    ]
    for path in copies:
        require(path.is_file(), f"missing article copy {path}")
        require(path.read_text(encoding="utf-8") == source_text, f"stale article copy {path}")
    require((OPENABLE / "Data_Study4_IJCM" / "README.txt").is_file(),
            "numbered replication package absent from openable article folder")
    for package in (ARTICLE / "Study4.zip", OPENABLE / "Study4.zip"):
        require(package.is_file(), f"missing complete article archive {package}")
        with zipfile.ZipFile(package) as archive:
            require(archive.testzip() is None, f"corrupt article archive {package}")
            require("Study4_Manuscript.md" in archive.namelist(),
                    f"article manuscript absent from archive root: {package}")
    return len(copies) + 3


def validate_delivery() -> int:
    required = [
        "00_OPEN_ME.md",
        "Study4_Complete_Manuscript.docx",
        "Study4_Complete_Manuscript.md",
        "Study4_Complete_Manuscript.html",
        "01_Title_Page_Not_for_Review.docx",
        "02_Blinded_Manuscript_for_Review.docx",
        "03_Cover_Letter.docx",
        "04_Tables.docx",
        "05_Figure_Captions.docx",
        "06_Supplementary_Figures.docx",
        "07_Supplementary_Tables.docx",
        "Supplementary_Results/FIGURES.md",
        "Supplementary_Results/tables_for_article.md",
        "Supplementary_Results/results.json",
        "Supplementary_Results/results_nlg.json",
        "Supplementary_Results/results_industry.json",
        "Data_Study4_IJCM/README.txt",
        "ZIP_CONTENTS.md",
        "Study4_COMPLETE_SUBMISSION.zip",
    ]
    for relative in required:
        path = DELIVERY / relative
        require(path.is_file() and path.stat().st_size > 0, f"missing delivery file {path}")

    manuscript = docx_text(DELIVERY / "Study4_Complete_Manuscript.docx")
    required_content = [
        "How Does the Civil Engineering Industry Economy Change",
        "Abstract",
        "Keywords",
        "Introduction",
        "Empirical design",
        "Results",
        "Discussion",
        "Conclusion",
        "References",
        "Table 1",
        "Table 6",
        "Figure 1",
        "Figure 5",
    ]
    for content in required_content:
        require(content in manuscript, f"complete Word manuscript lacks {content!r}")
    require(not re.search(r"\b(?:TODO|TBD|FIXME|LOREM)\b", manuscript, re.I),
            "draft marker in complete Word manuscript")
    tables, media = docx_structure(DELIVERY / "Study4_Complete_Manuscript.docx")
    require(tables >= 6, f"complete Word manuscript embeds {tables} tables, expected at least 6")
    require(media >= 5, f"complete Word manuscript embeds {media} figures, expected at least 5")

    figures = sorted((DELIVERY / "Figures").glob("Figure*.png"))
    require(len(figures) == 5, f"delivery folder has {len(figures)} figures, expected 5")
    supplementary_figures = sorted((DELIVERY / "Supplementary_Results" / "figures").glob("*.png"))
    supplementary_tables = sorted((DELIVERY / "Supplementary_Results" / "tables").glob("*.csv"))
    require(len(supplementary_figures) == 23,
            f"supplement has {len(supplementary_figures)} figures, expected 23")
    require(len(supplementary_tables) == 34,
            f"supplement has {len(supplementary_tables)} tables, expected 34")

    package = DELIVERY / "Study4_COMPLETE_SUBMISSION.zip"
    with zipfile.ZipFile(package) as archive:
        require(archive.testzip() is None, "complete delivery zip contains a corrupt member")
        names = set(archive.namelist())
        for member in [
            "Study4_Complete_Manuscript.docx",
            "01_Title_Page_Not_for_Review.docx",
            "02_Blinded_Manuscript_for_Review.docx",
            "03_Cover_Letter.docx",
            "04_Tables.docx",
            "05_Figure_Captions.docx",
            "06_Supplementary_Figures.docx",
            "07_Supplementary_Tables.docx",
            "Figures/Figure1.png",
            "Figures/Figure5.png",
            "Supplementary_Results/figures/figure23_uk_india_china_service_growth.png",
            "Supplementary_Results/tables/table_nlg_identification.csv",
            "Data_Study4_IJCM/README.txt",
            "ZIP_CONTENTS.md",
        ]:
            require(member in names, f"delivery zip missing {member}")
    return len(required) + len(required_content) + 6 + 14


def main() -> None:
    checks = (
        validate_markdown()
        + validate_data()
        + validate_submission()
        + validate_copies()
        + validate_delivery()
    )
    print(f"Study 4 validation passed ({checks} checks).")


if __name__ == "__main__":
    main()
