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

## Study 4 (final)

Open [`Study4_FINAL_VERSION/`](Study4_FINAL_VERSION/). That folder **replaces** the old `Study4_Global_AI_Civil_Engineering_Economy/` tree. It contains all data, tables, figures 1–21, English and Chinese articles, scripts, and zips. Estimates are generated from the official CSVs in `Study4_FINAL_VERSION/data/`.

Zip copies: [`Study4_zip_packages/`](Study4_zip_packages/).

## Licence

Author-generated data: [CC BY 4.0](LICENSE). Third-party index files remain under their publishers’ terms and must be cited from the manuscript reference list.
