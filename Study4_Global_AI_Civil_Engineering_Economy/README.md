# Study 4: GenAI and the cross-border civil engineering economy

Complete zip (data, tables, figures, manuscript, scripts):

`release/Study4_complete_package_2026-09-17.zip`

Rebuild:

```bash
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/run_analysis.py
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/run_novelty_layer.py
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/download_ai_shocks.py
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/run_nlg_shock.py
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/inherit_legacy_instruments.py
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/build_article_assets.py
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/build_release_zip.py
```

Requires pandas, numpy, statsmodels, matplotlib.

Catalogue of have / missing series: `DATA_INVENTORY.md`.

This article does **not** use IJCM LLM occupation scores. Exposure is Eloundou; employment is ONS APS. Full paper with Tables 1–11 and Figure captions: `manuscript/Study4_Manuscript.md`.

**Preferred shock is Eurostat E_AI_TNLG (generative text) in NACE M, 2024 minus 2023**, not generic E_AI_TANY. Headline Post×ΔTNLG = 0.009 (0.005), N=357, p=0.108. Post-2024 only = 0.007**. India corridor = 0.021***. Generic TANY remains 0.000 (0.006). M71 GVA still −0.007*. Do not claim A-country 2121 causes B-country GDP.
