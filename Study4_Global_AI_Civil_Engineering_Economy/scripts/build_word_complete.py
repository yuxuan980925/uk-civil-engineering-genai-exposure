#!/usr/bin/env python3
"""Build Word-format Study 4 files (manuscript, figures, tables, results) in one folder."""
from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
WORD = ROOT / "Word"
RESULTS = ROOT / "results"
MAX_ROWS = 40
MAX_COLS = 10


def set_run_font(run, size=11, bold=False, name="Times New Roman"):
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = name
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn("w:eastAsia"), "Times New Roman")


def add_p(doc, text, *, bold=False, size=11, italic=False, center=False):
    p = doc.add_paragraph()
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold)
    run.italic = italic
    return p


def add_grid(doc, headers, rows, font=9):
    headers = [str(h) if h is not None else "" for h in headers]
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.style = "Table Grid"
    for j, header in enumerate(headers):
        cell = tbl.rows[0].cells[j]
        cell.text = ""
        run = cell.paragraphs[0].add_run(header)
        set_run_font(run, size=font, bold=True)
    for r, row in enumerate(rows, 1):
        for c, value in enumerate(row):
            cell = tbl.rows[r].cells[c]
            cell.text = ""
            run = cell.paragraphs[0].add_run("" if value is None else str(value))
            set_run_font(run, size=font)
    doc.add_paragraph()


def read_csv(path: Path):
    with path.open(encoding="utf-8", errors="replace", newline="") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        return [], []
    return rows[0], rows[1:]


def trim(headers, rows):
    note = []
    if len(headers) > MAX_COLS:
        note.append(f"showing first {MAX_COLS} of {len(headers)} columns; full file is in tables/")
        headers = headers[:MAX_COLS]
        rows = [r[:MAX_COLS] for r in rows]
    if len(rows) > MAX_ROWS:
        note.append(f"showing first {MAX_ROWS} of {len(rows)} rows; full file is in tables/")
        rows = rows[:MAX_ROWS]
    return headers, rows, "; ".join(note)


def copy_named(src: Path, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def identification_rows(items):
    headers = ["Specification", "Coefficient", "N", "Note"]
    rows = []
    for item in items:
        rows.append(
            [
                item.get("spec", ""),
                item.get("display", ""),
                item.get("n", ""),
                item.get("note", ""),
            ]
        )
    return headers, rows


def build_all_tables():
    doc = Document()
    add_p(doc, "Study 4 — all tables", bold=True, size=16, center=True)
    add_p(
        doc,
        "Article Tables 1–6 are first. Experiment CSV tables follow. "
        "Wide or long files are truncated in Word; the complete CSV is in tables/.",
        italic=True,
        size=11,
    )

    ijcm = ROOT / "IJCM_Submission" / "04_Tables.docx"
    add_p(doc, "A. Article Tables 1–6 (IJCM)", bold=True, size=14)
    add_p(
        doc,
        "The editable six-table Word file is Word/09_IJCM_Tables.docx "
        f"(copied from {ijcm.name}).",
        size=11,
    )

    add_p(doc, "B. All experiment CSV tables", bold=True, size=14)
    for path in sorted((ROOT / "tables").glob("*.csv")):
        headers, rows = read_csv(path)
        headers, rows, note = trim(headers, rows)
        add_p(doc, path.name, bold=True, size=12)
        if note:
            add_p(doc, note, italic=True, size=9)
        if headers:
            add_grid(doc, headers, rows)
    dest = WORD / "04_All_Tables.docx"
    doc.save(dest)
    copy_named(dest, ROOT / "04_All_Tables.docx")
    return dest


def build_results_docx():
    doc = Document()
    add_p(doc, "Study 4 — experimental results", bold=True, size=16, center=True)
    add_p(
        doc,
        "Machine-readable copies: results/results.json, results_nlg.json, results_industry.json.",
        italic=True,
    )
    run_md = (ROOT / "EXPERIMENTS_RUN.md").read_text(encoding="utf-8")
    add_p(doc, "Experiment log", bold=True, size=14)
    for line in run_md.splitlines():
        add_p(doc, line, size=11)

    mapping = [
        ("Any-AI (TANY) identification", ROOT / "results.json", "identification"),
        ("NLG (TNLG) identification", ROOT / "results_nlg.json", "identification"),
        ("SBS M71 industry-economy identification", ROOT / "results_industry.json", "identification"),
    ]
    for title, path, key in mapping:
        data = json.loads(path.read_text(encoding="utf-8"))
        add_p(doc, title, bold=True, size=14)
        if path.name == "results_nlg.json":
            eu = data.get("eu27_M_TNLG", {})
            add_p(doc, f"EU-27 NACE M TNLG: 2021={eu.get('2021')}, 2023={eu.get('2023')}, 2024={eu.get('2024')}, 2025={eu.get('2025')}.")
            add_p(doc, f"Preferred shock: {data.get('preferred_shock', '')}")
        if path.name == "results_industry.json":
            add_p(doc, f"Identified object: {data.get('identified_object', '')}")
            add_p(doc, f"Cannot identify: {data.get('cannot_identify', '')}")
        headers, rows = identification_rows(data.get(key, []))
        add_grid(doc, headers, rows)

    nlg = json.loads((ROOT / "results_nlg.json").read_text(encoding="utf-8"))
    if "uk_india_china" in nlg:
        add_p(doc, "UK–India and UK–China corridors", bold=True, size=14)
        items = nlg["uk_india_china"]
        if isinstance(items, list) and items and isinstance(items[0], dict):
            headers = list(items[0].keys())
            rows = [[item.get(h, "") for h in headers] for item in items]
            headers, rows, note = trim(headers, rows)
            if note:
                add_p(doc, note, italic=True, size=9)
            add_grid(doc, headers, rows)

    dest = WORD / "05_Experimental_Results.docx"
    doc.save(dest)
    copy_named(dest, ROOT / "05_Experimental_Results.docx")
    return dest


def assemble_word_folder():
    if WORD.exists():
        shutil.rmtree(WORD)
    WORD.mkdir(parents=True)
    RESULTS.mkdir(parents=True, exist_ok=True)

    copies = {
        "01_English_Manuscript.docx": ROOT / "Study4_Manuscript.docx",
        "02_Chinese_Manuscript.docx": ROOT / "CN_full_article.docx",
        "03_All_Figures.docx": ROOT / "FIGURES.docx",
        "06_IJCM_Title_Page.docx": ROOT / "IJCM_Submission" / "01_Title_Page_Not_for_Review.docx",
        "07_IJCM_Blinded_Manuscript.docx": ROOT / "IJCM_Submission" / "02_Blinded_Manuscript_for_Review.docx",
        "08_IJCM_Cover_Letter.docx": ROOT / "IJCM_Submission" / "03_Cover_Letter.docx",
        "09_IJCM_Tables.docx": ROOT / "IJCM_Submission" / "04_Tables.docx",
        "10_IJCM_Figure_Captions.docx": ROOT / "IJCM_Submission" / "05_Figure_Captions.docx",
        "11_IJCM_Identified_Manuscript.docx": ROOT / "IJCM_Submission" / "00_Manuscript_as_Submitted.docx",
        "12_Supplementary_Tables.docx": ROOT / "tables_for_article.docx",
    }
    missing = [f"{k} <- {v}" for k, v in copies.items() if not v.exists()]
    if missing:
        raise SystemExit("missing Word sources:\n" + "\n".join(missing))
    for name, src in copies.items():
        copy_named(src, WORD / name)

    for name in ["results.json", "results_nlg.json", "results_industry.json", "EXPERIMENTS_RUN.md", "MANIFEST.csv"]:
        src = ROOT / name
        if src.exists():
            copy_named(src, RESULTS / name)

    tables = build_all_tables()
    results_docx = build_results_docx()

    # verify media counts
    import zipfile

    def n_media(path: Path) -> int:
        with zipfile.ZipFile(path) as zf:
            return sum(1 for n in zf.namelist() if n.startswith("word/media/"))

    en = n_media(WORD / "01_English_Manuscript.docx")
    cn = n_media(WORD / "02_Chinese_Manuscript.docx")
    figs = n_media(WORD / "03_All_Figures.docx")
    if en < 5 or cn < 5:
        raise SystemExit(f"manuscripts missing figures: EN={en} CN={cn}")
    if figs < 23:
        raise SystemExit(f"FIGURES.docx expected 23 images, found {figs}")

    readme = """# Study 4 完整文件夹（Word）

打开本文件夹中的 **Word/**。正文、图、表都是 .docx。不要打开 zip。

## Word 文件

| 文件 | 内容 |
|---|---|
| [Word/01_English_Manuscript.docx](Word/01_English_Manuscript.docx) | 英文正文（含文中 5 张图） |
| [Word/02_Chinese_Manuscript.docx](Word/02_Chinese_Manuscript.docx) | 中文正文（含文中 5 张图） |
| [Word/03_All_Figures.docx](Word/03_All_Figures.docx) | 全部 23 张图 |
| [Word/04_All_Tables.docx](Word/04_All_Tables.docx) | 全部实验 CSV 表（Word） |
| [Word/05_Experimental_Results.docx](Word/05_Experimental_Results.docx) | 实验结果（TANY / TNLG / SBS） |
| [Word/07_IJCM_Blinded_Manuscript.docx](Word/07_IJCM_Blinded_Manuscript.docx) | IJCM 匿名审稿稿 |
| [Word/09_IJCM_Tables.docx](Word/09_IJCM_Tables.docx) | IJCM 文中 Table 1–6 |
| [Word/06_IJCM_Title_Page.docx](Word/06_IJCM_Title_Page.docx) | 标题页 |
| [Word/08_IJCM_Cover_Letter.docx](Word/08_IJCM_Cover_Letter.docx) | Cover letter |
| [Word/12_Supplementary_Tables.docx](Word/12_Supplementary_Tables.docx) | 补充表格 Word |

## 数据与实验结果（同一文件夹）

| 路径 | 内容 |
|---|---|
| `data/` | Eurostat / BaTIS / SBS 等原始检索文件 |
| `Data_Study4_IJCM/` | 编号复制数据 01–08 |
| `tables/` | 全部实验 CSV（完整、未截断） |
| `figures/` | 全部 PNG 原图 |
| `results/` | `results.json`、`results_nlg.json`、`results_industry.json` |
| `IJCM_Submission/` | 投稿 Word + Figure1–5（300 dpi） |

Corresponding author: Yuxuan Chai (`yuxuanchai98@outlook.com`), University of Strathclyde.
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")
    (ROOT / "OPEN_IN_EDITOR.md").write_text(readme, encoding="utf-8")
    (WORD / "README.md").write_text(readme, encoding="utf-8")

    print("word_dir", WORD)
    print("tables_docx", tables, tables.stat().st_size)
    print("results_docx", results_docx, results_docx.stat().st_size)
    print("media EN/CN/FIGS", en, cn, figs)
    print("word_files", sorted(p.name for p in WORD.glob("*.docx")))


if __name__ == "__main__":
    assemble_word_folder()
