# Study 4: GenAI and the cross-border civil engineering economy

Complete zip (data, tables, figures, manuscript, scripts):

`release/Study4_complete_package_2026-09-16.zip`

Rebuild:

```bash
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/run_analysis.py
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/run_novelty_layer.py
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/build_article_assets.py
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/build_release_zip.py
```

Requires pandas, numpy, statsmodels, matplotlib.

Catalogue of have / missing series: `DATA_INVENTORY.md`.

This article does **not** use IJCM LLM occupation scores. Exposure is Eloundou; employment is ONS APS. Full paper with Tables 1–11 and Figure captions: `manuscript/Study4_Manuscript.md`.

**Headline after expanding the panel:** EU-16 Post × ΔM AI = 0.000 (0.006), N=336. EU-8 subsample = 0.019 (0.006). M71 GVA Post × ΔM = −0.006 (0.005). Report the nulls. Do not claim A-country 2121 causes B-country GDP.
