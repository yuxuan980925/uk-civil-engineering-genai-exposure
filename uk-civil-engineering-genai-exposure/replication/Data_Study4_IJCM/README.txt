Data accompanying
How Does the Civil Engineering Industry Economy Change under an AI Shock? The United Kingdom’s Service Links with India and China

Manuscript submitted to International Journal of Construction Management.
Corresponding author: Yuxuan Chai (yuxuanchai98@outlook.com), University of Strathclyde.

The article uses retrieved official series. No country, industry or trade cell is interpolated.
Preferred shock: Eurostat E_AI_TNLG, NACE M, 2024 minus 2023.
Industry outcomes: Eurostat NACE M71. Trade: OECD–WTO BaTIS, adjustment B.
Country focus: UK–India and UK–China; EU-17 is the estimation panel only.
See DATA_COMPLIANCE_AUDIT.md for the independent recompute of Tables 1–6.
See RESEARCH_SCOPE.md and RELOCATION_RESEARCH_DESIGN.md for the reset
research question and what these series can and cannot identify.

Folder contents
---------------
01_ai_shock/
  Eurostat enterprise AI series (TANY, TNLG and technology/sector placebos) and
  logs of unsuccessful pulls (OWID, IMF AIPI, OECD ICT_BUS).

02_industry_accounts/
  Structural business statistics and national accounts for NACE M71, F and M;
  ILOSTAT ISIC F/M employment; BLS engineering comparison (NAICS 54, too broad).

03_trade/
  OECD–WTO BaTIS UK–India and UK–China corridors (SJ3, SE, SI), broader civil-related
  extracts, and the EU importer panels used in the regressions.

04_external_indices/
  Eloundou occupation scores and Study 1 / legacy indices used only as context.
  They are not the generative shock.

05_derived/
  Machine-readable estimates (results*.json) and derived tables matching the article.

06_tables/
  Table1.csv–Table6.csv, the six tables in the main manuscript.

07_scripts/
  Retrieval, estimation and submission-build scripts.

08_figures/
  Figure1.png to Figure5.png (300 dpi), the figures embedded in the manuscript.

09_relocation_probe/
  New official retrievals for the reset relocation question: Eurostat ITS
  engineering services (SJ312), LFS two-digit occupations, ILO 2142 attempts,
  SBS M7112, ITS placebo partners, FATS coverage, experiment tables and figures.
  Missing cells are logged, not filled. See CORROBORATION.md.

Third-party files (Eurostat, OECD–WTO, ILO, ONS, Felten, Eloundou) remain the
property of their publishers and should be cited as in the manuscript reference
list. They are included only as the versions used for the analysis.

Licence for author-generated files (derived tables, figures, scripts, corridor
extracts prepared for this article): CC BY 4.0.
