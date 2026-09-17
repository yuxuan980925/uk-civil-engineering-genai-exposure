Study 4 complete package
========================
Built: 2026-09-17

Folder layout
-------------
00_previous_ijcm_data/  Old occupation-paper files (Felten, ONS, APS, LLM panel). LLM scores are NOT the shock.
01_data/         Official Study 4 downloads + analysis panels (no fabricated cells)
02_tables/       All regression and descriptive tables (CSV)
03_figures/      All figures 1-21 (PNG)
04_manuscript/   Full English article + Chinese full article + tables
05_scripts/      Replication scripts
99_all_zips/     Component zips (data, tables, figures, manuscript, scripts, IJCM)
                 The same files live in the standalone folder Study4_zip_packages/
DATA_INVENTORY.md  Have / missing / cannot-exist catalogue
DATA_SOURCES.md    APIs and retrieval date
results*.json      Machine-readable estimates (TANY, TNLG, M71 SBS)

How to replicate
----------------
python3 05_scripts/run_analysis.py
python3 05_scripts/run_novelty_layer.py
python3 05_scripts/run_nlg_shock.py
python3 05_scripts/run_industry_economy.py

Scripts expect this package to sit as Study4_Global_AI_Civil_Engineering_Economy/
(data/ tables/ figures/ next to scripts/). If you unzip only this package, copy
01_data -> data, 02_tables is output, or run from the git repo instead.

Claim boundary
--------------
Do not treat APS SOC 2121 as causing partner-country GDP or ISCO 2142 counts.
EU-16 Post x Delta M on Mode-1 SJ3 is a null; EU-8 is sample-dependent.
NACE M71 AI survey and BaTIS SJ312 do not exist.
