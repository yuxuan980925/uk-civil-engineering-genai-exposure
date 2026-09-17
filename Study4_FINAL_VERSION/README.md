# Study 4: GenAI and the cross-border civil engineering economy

**This folder is the final version** (repository root: `Study4_FINAL_VERSION/`).

Unpacked data, tables, figures 1–21, manuscripts, scripts, and `zips/` live here.

Duplicate zip copies: `Study4_zip_packages/` and `Study4_zip_packages/Study4_FINAL_VERSION/`. Working files: `Study4_Global_AI_Civil_Engineering_Economy/`.

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

Full article (title: how the civil engineering industry economy changes under an AI shock, cross-country): `manuscript/Study4_Manuscript.md`. Chinese full text: `manuscript/CN_full_article.md`. This article does **not** use IJCM LLM scores as the shock.

**Preferred shock is Eurostat E_AI_TNLG.** Trade: Post×ΔTNLG 0.009 (0.005); India 0.021***. **Industry:** SBS log M71 turnover Post-2024×ΔTNLG −0.007**; employment 0.000. Do not claim A-country 2121 causes B-country GDP.
