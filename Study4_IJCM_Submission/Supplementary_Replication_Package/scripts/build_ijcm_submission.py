#!/usr/bin/env python3
"""Build a submission-ready IJCM file set from the Study 4 manuscript."""
from __future__ import annotations

import re
import shutil
import subprocess
import hashlib
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "Study4_FINAL_VERSION"
SOURCE = STUDY / "manuscript" / "Study4_Manuscript.md"
OUT = ROOT / "Study4_IJCM_Submission"
TITLE = (
    "How Does the Civil Engineering Industry Economy Change under an AI Shock? "
    "The United Kingdom’s Service Links with India and China"
)
MAIN_FIGURES = [
    ("Figure_1_UK_India_China_SJ3.png", "figure22_uk_india_china_sj3.png"),
    ("Figure_2_UK_India_China_service_growth.png", "figure23_uk_india_china_service_growth.png"),
    ("Figure_3_EU_NLG_adoption.png", "figure12_tnlg_vs_tml.png"),
    ("Figure_4_Indian_SJ3_NLG_association.png", "figure15_cross_section_tnlg.png"),
    ("Figure_5_M71_turnover_growth.png", "figure17_sbs_turnover_m71_vs_F.png"),
]


def style_document(document: Document) -> None:
    section = document.sections[0]
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)
    normal = document.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing = 1.5
    normal.paragraph_format.space_after = Pt(0)


def make_reference_doc(path: Path) -> None:
    document = Document()
    style_document(document)
    for name in ["Title", "Heading 1", "Heading 2", "Heading 3"]:
        style = document.styles[name]
        style.font.name = "Times New Roman"
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    document.styles["Title"].font.size = Pt(16)
    document.styles["Heading 1"].font.size = Pt(14)
    document.styles["Heading 2"].font.size = Pt(12)
    document.save(path)


def pandoc(source: Path, dest: Path, reference: Path) -> None:
    subprocess.check_call(
        [
            "pandoc",
            str(source),
            "--from=markdown+tex_math_dollars",
            "--to=docx",
            "--output",
            str(dest),
            f"--resource-path={source.parent}:{STUDY}",
            f"--reference-doc={reference}",
        ]
    )


def blinded_text(text: str) -> str:
    lines = text.splitlines()
    # Remove the identified byline and working-paper date immediately below title.
    keep = [lines[0]] + lines[4:]
    text = "\n".join(keep)
    text = text.replace(
        "Replication files are in `Study4_Article_Complete/` "
        "(open `Study4_Manuscript.md`, `CN_full_article.md`, `FIGURES.md`, "
        "and `tables_for_article.md` in the editor — not the zip). Figures, "
        "tables, and official data are in `figures/`, `tables/`, and `data/` "
        "in that folder. Missing series are catalogued in `DATA_INVENTORY.md`; "
        "their absence is part of the claim boundary.",
        "Replication materials, including data, code, figures and supplementary "
        "tables, are available to the editor and will be deposited in an "
        "appropriate public repository on acceptance. Missing series are "
        "documented in the supplementary material.",
    )
    # Safety check against identity references from the manuscript header.
    return re.sub(r"(?im)^.*(?:Yuxuan Chai|Strathclyde|yuxuanchai98@outlook\.com).*\n?", "", text)


def write_title_page(path: Path) -> None:
    document = Document()
    style_document(document)
    p = document.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(TITLE)
    run.bold = True
    run.font.size = Pt(16)
    document.add_paragraph()
    document.add_paragraph("Yuxuan Chai", style="Heading 1")
    document.add_paragraph("University of Strathclyde")
    document.add_paragraph("Corresponding author: Yuxuan Chai")
    document.add_paragraph("Email: yuxuanchai98@outlook.com")
    document.add_paragraph("Journal: International Journal of Construction Management")
    document.add_page_break()
    document.add_heading("Declarations for the editor", level=1)
    document.add_paragraph(
        "Author contribution: Yuxuan Chai is the sole author of this manuscript."
    )
    document.add_paragraph(
        "Data and code availability: The replication package includes retrieved "
        "Eurostat and OECD–WTO BaTIS series, generated tables and figures, and "
        "analysis scripts. Third-party source material remains subject to the "
        "publishers’ terms."
    )
    document.add_paragraph(
        "Ethics: This study analyses published aggregate statistical series and "
        "does not involve human participants, personal data or animal subjects."
    )
    document.add_paragraph(
        "Funding and competing interests: These declarations must be confirmed "
        "by the corresponding author in the journal’s submission system before "
        "submission; no funding or conflict statement was supplied in the "
        "repository materials."
    )
    document.save(path)


def write_cover_letter(path: Path) -> None:
    document = Document()
    style_document(document)
    document.add_paragraph("Dear Editor,")
    document.add_paragraph(
        f"I am submitting the manuscript “{TITLE}” for consideration in the "
        "International Journal of Construction Management."
    )
    document.add_paragraph(
        "The manuscript examines how the initial diffusion of natural-language "
        "generation is associated with architectural and engineering activity "
        "and with the United Kingdom’s services relationships with India and "
        "China. It distinguishes NACE M71 engineering consultancies from "
        "construction and separates technical-business, construction and "
        "computer service flows. The evidence uses retrieved Eurostat and "
        "OECD–WTO BaTIS data, with full replication materials supplied."
    )
    document.add_paragraph(
        "The corresponding author must confirm in the submission portal that "
        "the work is original, is not under consideration elsewhere, that all "
        "authors approve submission, and that funding and competing-interest "
        "declarations are complete. Those confirmations are not inferred or "
        "made by this file."
    )
    document.add_paragraph("Sincerely,")
    document.add_paragraph("Yuxuan Chai")
    document.save(path)


def write_readme(path: Path) -> None:
    path.write_text(
        f"""# International Journal of Construction Management submission set

## Upload these files

1. `01_Blinded_Manuscript_for_Review.docx` — anonymous main manuscript: title, abstract, keywords, text, references, five embedded figures and six embedded tables.
2. `02_Title_Page_Not_for_Review.docx` — author and affiliation details, correspondence information, and editor declarations. Designate as **not for review** if the journal requires double-anonymous review.
3. `03_Cover_Letter.docx` — editor letter. Confirm the bracket-free administrative statements in ScholarOne before submitting.
4. `Figures/` — five separate, numbered, anonymised PNG figure files.
5. `Supplementary_Replication_Package/` — data, results, code and full supplementary tables/figures.

## Required human confirmations

The repository does not establish funding, conflicts of interest, prior publication or all-author approval. The corresponding author must complete those mandatory declarations in ScholarOne and revise the title page/letter if needed. Do not submit until these have been confirmed.

## Format checks performed

- Main manuscript uses a 12-point Times New Roman, 1.5-line-spaced Word reference style with 2.54 cm margins.
- The blinded manuscript contains no author name, email, affiliation, repository URL or identifiable acknowledgement.
- The manuscript contains five main-text figures and six main-text tables.
- The primary evidence uses retrieved Eurostat and OECD–WTO BaTIS data; detailed data/code are included as supplementary material.

Taylor & Francis commonly requests a title page, main manuscript, figure files, tables and supplementary material; anonymous review requirements vary by journal. Confirm IJCM’s current author instructions in the submission system before uploading.
""",
        encoding="utf-8",
    )


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "Figures").mkdir(parents=True)
    reference = OUT / ".ijcm-reference.docx"
    make_reference_doc(reference)

    text = SOURCE.read_text(encoding="utf-8")
    blinded = OUT / "01_Blinded_Manuscript_for_Review.md"
    blinded.write_text(blinded_text(text), encoding="utf-8")
    pandoc(blinded, OUT / "01_Blinded_Manuscript_for_Review.docx", reference)
    write_title_page(OUT / "02_Title_Page_Not_for_Review.docx")
    write_cover_letter(OUT / "03_Cover_Letter.docx")
    write_readme(OUT / "README_SUBMISSION.md")

    for number, source_name in MAIN_FIGURES:
        shutil.copy2(STUDY / "figures" / source_name, OUT / "Figures" / number)

    supplementary = OUT / "Supplementary_Replication_Package"
    shutil.copytree(ROOT / "Study4_Article_Complete", supplementary)
    # Avoid recursive inclusion when rebuilding from a tree that may contain the kit.
    for hidden in supplementary.rglob(".*.word.html"):
        hidden.unlink()
    reference.unlink()
    files = sorted(p for p in OUT.rglob("*") if p.is_file())
    (OUT / "PACKAGE_INVENTORY.md").write_text(
        "# Submission package inventory\n\n"
        f"- Submission files: 3 Word documents plus this guide\n"
        f"- Separate anonymised figures: {len(MAIN_FIGURES)} PNG\n"
        f"- Supplementary replication files: {len(files) - 4 - len(MAIN_FIGURES)}\n"
        f"- Files before archive: {len(files) + 2}\n\n"
        "## Included files\n\n"
        + "\n".join(f"- `{p.relative_to(OUT).as_posix()}`" for p in files)
        + "\n",
        encoding="utf-8",
    )
    checksum_files = sorted(p for p in OUT.rglob("*") if p.is_file() and p.name != "SHA256SUMS.txt")
    (OUT / "SHA256SUMS.txt").write_text(
        "\n".join(
            f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(OUT).as_posix()}"
            for p in checksum_files
        )
        + "\n",
        encoding="utf-8",
    )
    zip_path = ROOT / "Study4_IJCM_Submission.zip"
    if zip_path.exists():
        zip_path.unlink()
    subprocess.check_call(
        ["zip", "-r", "-X", str(zip_path), "."],
        cwd=OUT,
        stdout=subprocess.DEVNULL,
    )
    subprocess.check_call(["unzip", "-t", str(zip_path)], stdout=subprocess.DEVNULL)
    print(OUT)
    print(zip_path)


if __name__ == "__main__":
    main()
