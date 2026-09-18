Data accompanying
Who drafts and who still signs? A multi-instrument map of generative AI exposure
across 50 UK civil and environmental occupations

Manuscript submitted to International Journal of Construction Management.
Panel: 50 occupations × 3 models × 20 runs = 3,000 occupation–run observations.
Models: ChatGPT, DeepSeek, Gemini 3 Pro.

Folder contents
---------------
01_llm_panel/
  chatgpt_main_prompt_runs_1_20.csv
  deepseek_main_prompt_runs_1_20.csv
  gemini3pro_main_prompt_runs_1_20.csv
  llm_panel_3000.csv
      Run-level scores for the main prompt (the panel used in the article).

02_occupation_frame/
  occupation_frame.csv
      50 occupation labels, SOC 2020 codes and short descriptions.
  occupation_context_crosswalk.csv
      Task-family assignment, APS employment, ONS automation match, Felten AIOE
      and language-modelling proxy fields used in Tables II, IV and V, with
      occupation-level 20-run LLM means.

03_survey/
  professional_survey_raw.xlsx
      Anonymous category-level practitioner survey export.
  human_expert_category_scores.csv
      Category means used in Table III (n = 52).

04_external_indices/
  ons_automation_matches.csv
      Occupation-level ONS automation crosswalk used in the article.
  ons_automation_probability_soc2010_table9.csv
      Source ONS SOC 2010 automation-probability table.
  aps_employment_2021_2025.csv
      Annual Population Survey employment series used as weights.
  AIOE_DataAppendix.xlsx
      Felten et al. occupation AI-exposure appendix.
  Language_Modeling_AIOE_AIIE.xlsx
      Language-modelling exposure appendix used as the Webb proxy.
  AIOE_README.md
      Publisher note supplied with the Felten files.

05_prompts/
  prompt_variants.txt
      The six prompt variants. The main analysis uses main_prompt.
  chatgpt_prompt_battery_runs.csv
      ChatGPT prompt-battery runs used in the robustness checks.

06_derived/
  occupation_scores_20run.csv
      Occupation-level means by model and pooled mean (used for figures and tables).
  model_summary_20run.csv
      Model-level descriptives matching Table I.
  task_family_summary_20run.csv
      Task-family pooled means matching Table II.

07_source_workbooks/
  chatgpt.xlsx, deepseek.xlsx, gemini3pro.xlsx
      Original interface workbooks from which occupation labels were aligned.

08_figures/
  Figure1.png to Figure4.png
      300 dpi figures embedded in the manuscript.

Third-party files (ONS, APS, Felten, language-modelling appendix) remain the
property of their publishers and should be cited as in the manuscript reference
list. They are included here only as the versions used for the crosswalks.

Licence for author-generated files (LLM panel, occupation frame, survey means,
derived tables, figures, prompt text): CC BY 4.0, pending a repository DOI.
