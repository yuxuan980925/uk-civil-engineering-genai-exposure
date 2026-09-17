# Study 4: GenAI and the cross-border civil engineering economy

Complete zip (data, tables, figures, manuscript, scripts):

`release/Study4_complete_package_2026-09-17.zip`

Rebuild:

```bash
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/run_analysis.py
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/run_novelty_layer.py
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/download_ai_shocks.py
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/download_m71_economy.py
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/run_nlg_shock.py
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/run_industry_economy.py
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/inherit_legacy_instruments.py
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/build_article_assets.py
python3 Study4_Global_AI_Civil_Engineering_Economy/scripts/build_release_zip.py
```

Requires pandas, numpy, statsmodels, matplotlib.

Catalogue of have / missing series: `DATA_INVENTORY.md`.

This article does **not** use IJCM LLM occupation scores. Exposure is Eloundou; employment is ONS APS. Full paper: `manuscript/Study4_Manuscript.md`.

**Preferred shock is Eurostat E_AI_TNLG.** Trade: Post×ΔTNLG 0.009 (0.005); India 0.021***. **Industry:** SBS log M71 turnover Post-2024×ΔTNLG −0.007**; employment 0.000. Do not claim A-country 2121 causes B-country GDP.
