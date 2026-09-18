# Experiments run from official CSVs

Date: 2026-09-17

Scripts (in order):
1. `scripts/run_analysis.py` — TANY SJ3 importer panel, APS, BaTIS corridors, event study, ILO
2. `scripts/run_novelty_layer.py` — M71 GVA, SJ1/SJ2 placebos, Eloundou
3. `scripts/inherit_legacy_instruments.py` — Felten AIOE/AIIE vs APS (instruments only)
4. `scripts/run_nlg_shock.py` — preferred E_AI_TNLG
5. `scripts/run_industry_economy.py` — SBS M71 2021–24
6. `scripts/build_article_assets.py` — article tables markdown

Headline estimates written to `results.json`, `results_nlg.json`, `results_industry.json`:

- TANY Post × ΔM 2021–24: from results.json `did_post_deltaM`
- TNLG preferred: 0.009 (0.005) N=357
- TNLG Post-2024: 0.007** (0.003) N=357
- TNLG India: 0.021*** (0.008) N=119
- SBS M71 turnover: -0.007** (0.003) N=68

EU-27 M TNLG: {'2021': 2.6, '2023': 4.55, '2024': 11.51, '2025': 17.74}

Figures 1–21 and all CSV tables were overwritten by these runs. No interpolated cells.
