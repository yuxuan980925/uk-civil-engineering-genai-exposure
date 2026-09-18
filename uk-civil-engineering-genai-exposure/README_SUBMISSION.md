# International Journal of Construction Management — Study 4 submission set

This folder is the complete journal package for Study 4, in the same role as
`Data_IJCM/` plus the submitted manuscript for Study 1.

## Upload these files to ScholarOne / Taylor & Francis

1. `01_Title_Page_Not_for_Review.docx` — title, author, affiliation, correspondence, declarations. Mark **not for review**.
2. `02_Blinded_Manuscript_for_Review.docx` — anonymous main manuscript (title, abstract, keywords, numbered text, disclosure, data availability, APA 7 references, six tables, five figures). Double-spaced 12-pt Times New Roman, 2.54 cm margins, line and page numbers.
3. `03_Cover_Letter.docx` — letter to the editor.
4. `04_Tables.docx` — editable copies of Tables 1–6.
5. `05_Figure_Captions.docx` — captions for Figures 1–5.
6. `Figures/Figure1.png` … `Figure5.png` — separate 300 dpi files.
7. `06_Supplementary_Figures.docx` and `07_Supplementary_Tables.docx` — supplementary material.

An identified author copy is `Study4_Complete_Manuscript.docx`.

The archive `Study4_COMPLETE_SUBMISSION.zip` contains only the journal submission set above (not replication scripts or raw data). Full replication data is in [`replication/`](../uk-civil-engineering-genai-exposure/replication/) on GitHub (and duplicated at repo root [`Data_Study4_IJCM/`](../Data_Study4_IJCM/)).

## Journal format applied

- Research article for the *International Journal of Construction Management* (Taylor & Francis, ISSN 1562-3599 / 2331-2327).
- Unstructured abstract (about 230 words) and six keywords.
- Numbered sections: Introduction; Literature review; Data; Empirical design; Results; Discussion; Limitations; Conclusion.
- End matter: Author contribution; Funding; Ethics statement; Disclosure statement; Data availability statement; References.
- In-text citations and reference list in APA 7th author–date form (accepted by Taylor & Francis format-free / Your Paper Your Way; production will apply the journal template after acceptance).
- Tables numbered Table 1–Table 6 with titles above and notes below.
- Figures numbered Figure 1–Figure 5, 300 dpi, captions listed separately.
- Double-anonymous review: the blinded file contains no author name, email, affiliation or acknowledgements.

## Required human check

Confirm funding, competing-interest and originality statements in ScholarOne if any detail has changed.

## Validate the package

After rebuilding, run
`python3 Study4_FINAL_VERSION/scripts/validate_submission.py` from the repository
root checkout. The validator checks the article sections, figure links and
resolution, anonymisation, data tables, checksums and zip integrity.

## Licence

Author-generated files: CC BY 4.0. Third-party statistics remain under their publishers’ terms.
