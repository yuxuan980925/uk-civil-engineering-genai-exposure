# Who drafts and who still signs?

Replication data for a manuscript submitted to *International Journal of Construction Management*:

**Who drafts and who still signs? A multi-instrument map of generative AI exposure across 50 UK civil and environmental occupations**

Corresponding author: Yuxuan Chai (`yuxuanchai98@outlook.com`), University of Strathclyde.

## Data availability

The files that support the findings are in [`Data_IJCM/`](Data_IJCM/). The panel is 50 occupations × 3 models × 20 runs = 3,000 occupation–run observations (ChatGPT, DeepSeek, Gemini 3 Pro). Occupation-level means match Table I of the manuscript (ChatGPT 3.56, DeepSeek 2.76, Gemini 3 Pro 3.02).

| Folder | Contents |
|---|---|
| `Data_IJCM/01_llm_panel/` | Run-level main-prompt scores |
| `Data_IJCM/02_occupation_frame/` | SOC 2020 labels, task families, ONS / Felten / Webb / APS crosswalk |
| `Data_IJCM/03_survey/` | Anonymous practitioner survey (n = 52) |
| `Data_IJCM/04_external_indices/` | ONS, APS and published AI-exposure appendices used for matching |
| `Data_IJCM/05_prompts/` | Prompt variants and ChatGPT prompt-battery runs |
| `Data_IJCM/06_derived/` | Occupation, model and task-family summaries |
| `Data_IJCM/07_source_workbooks/` | Original model workbooks |
| `Data_IJCM/08_figures/` | Figures 1–4 |

See `Data_IJCM/README.txt` for the file-level inventory.

## Study 4 (IJCM submission)

Manuscript submitted to *International Journal of Construction Management*:

**How Does the Civil Engineering Industry Economy Change under an AI Shock? The United Kingdom’s Service Links with India and China**

Corresponding author: Yuxuan Chai (`yuxuanchai98@outlook.com`), University of Strathclyde.

The single-folder submission handoff is
[`uk-civil-engineering-genai-exposure/`](uk-civil-engineering-genai-exposure/).
Open `Study4_Complete_Manuscript.docx`; the complete archive is
`uk-civil-engineering-genai-exposure/Study4_COMPLETE_SUBMISSION.zip` (17 journal files).

Full replication data (raw/processed series, scripts, supplementary figures/tables)
is on GitHub at
[`uk-civil-engineering-genai-exposure/replication/`](uk-civil-engineering-genai-exposure/replication/)
and duplicated at repo root [`Data_Study4_IJCM/`](Data_Study4_IJCM/).

After `git pull`, open the restored folder [`Study4_Global_AI_Civil_Engineering_Economy/`](Study4_Global_AI_Civil_Engineering_Economy/) (markdown, HTML, figures, and Word). That directory is no longer a pointer; the article files sit inside it.

The journal upload set is [`Study4_IJCM_Submission/`](Study4_IJCM_Submission/), in the same role as Study 1: a formatted manuscript plus a numbered replication package.

| File / folder | Role |
|---|---|
| `01_Title_Page_Not_for_Review.docx` | Title, author, affiliation, correspondence, declarations (not for review) |
| `02_Blinded_Manuscript_for_Review.docx` | Anonymous article: abstract, keywords, numbered text, six tables, five figures |
| `03_Cover_Letter.docx` | Letter to the editor |
| `04_Tables.docx` | Editable Tables 1–6 |
| `05_Figure_Captions.docx` | Captions for Figures 1–5 |
| `Figures/Figure1.png`–`Figure5.png` | Separate 300 dpi figures |
| `Data_Study4_IJCM/` | Numbered replication data (01–08), matching `Data_IJCM/` |
| `00_Manuscript_as_Submitted.docx` | Identified author copy |

The same numbered data package is also at [`Data_Study4_IJCM/`](Data_Study4_IJCM/). See `Data_Study4_IJCM/README.txt` for the file-level inventory.

| Open in editor | Path |
|---|---|
| English article | [`Study4_Global_AI_Civil_Engineering_Economy/Study4_Manuscript.md`](Study4_Global_AI_Civil_Engineering_Economy/Study4_Manuscript.md) |
| Chinese article | [`Study4_Global_AI_Civil_Engineering_Economy/CN_full_article.md`](Study4_Global_AI_Civil_Engineering_Economy/CN_full_article.md) |
| Folder index | [`Study4_Global_AI_Civil_Engineering_Economy/index.html`](Study4_Global_AI_Civil_Engineering_Economy/index.html) |
| Blinded Word | [`Study4_Global_AI_Civil_Engineering_Economy/IJCM_Submission/02_Blinded_Manuscript_for_Review.docx`](Study4_Global_AI_Civil_Engineering_Economy/IJCM_Submission/02_Blinded_Manuscript_for_Review.docx) |

Working copies and extra experiments remain in [`Study4_FINAL_VERSION/`](Study4_FINAL_VERSION/) and [`Study4_Article_Complete/`](Study4_Article_Complete/).

## Licence

Author-generated data: [CC BY 4.0](LICENSE). Third-party index files remain under their publishers’ terms and must be cited from the manuscript reference list.
