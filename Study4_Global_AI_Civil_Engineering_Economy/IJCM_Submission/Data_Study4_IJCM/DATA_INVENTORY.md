# Study 4 data inventory: what the design needs, what we have, what does not exist

Retrieved 17 September 2026. No interpolated occupation, M71, or GDP cells.

The innovation is **not** “more countries in a generic AI-GDP regression.” It is a **civil-specific stack** that other AI-labour papers do not use together:

1. **Task exposure inside civil engineering** (drafters / technicians / licensed engineers)
2. **Sectoral GenAI adoption** — preferred **E_AI_TNLG**, not generic TANY; M vs F vs J/C/N; M71 AI unpublished
3. **Industry outcome at NACE M71** (architectural and engineering activities), not all of ISIC M and not ISIC F
4. **Cross-border delivery proxies** (digitally deliverable SJ3 from India/PH/VN vs project-based SE from China). BaTIS does not directly identify GATS modes of supply.
5. **Placebos on the same importers** (SI computer, SJ1 R&D, SJ2 consulting, F AI, F GVA)

If a series is missing, the inventory says so. That missingness is part of the contribution: it defines the claim boundary.

## A. Civil-specific AI shock

| Object | Needed for | Status | File / result |
|---|---|---|---|
| ILO–NASK ISCO 2142 | Task potential of civil engineers | Cite ILO WP 140 (0.30, Not Exposed); appendix not re-downloaded here | manuscript |
| Eloundou β_human 17-2051 / 17-3011 / 17-3022 | Drafter vs engineer gap | **Have** | `data/eloundou_occ_level.csv`; 0.375 / 0.52 / 0.477 |
| Felten AIOE / LM-AIOE / AIIE | Pre-GenAI occupation and construction-industry exposure | **Have** (copied from Data_IJCM, used in Table 12 / Fig 10–11) | `data/from_legacy_study4/` |
| ONS automation probability | Pre-GenAI routine-task proxy | **Have** | same |
| Previous LLM 1–5 panel | Robustness column only | Copied, not used as the shock | `occupation_scores_20run.csv` |
| Eurostat E_AI_TANY NACE **M** | Professional-services AI (contains M71 firms); **generic**, mixes ML and GenAI | **Have** 2021/23/24/25, 18 geos | `data/eurostat_ai_raw.csv` |
| Eurostat E_AI_TANY NACE **F** | On-site construction placebo | **Have** | same |
| Eurostat **E_AI_TNLG** NACE M/F | **Preferred GenAI shock**: natural-language generation | **Have** 2021/23/24/25 | `data/eurostat_ai_genai_types.csv` (611 rows) |
| Eurostat E_AI_TML / TTM / TIR | Technology placebos (ML, text mining, image recognition) | **Have** | same |
| Eurostat E_AI_TPVSG | Pictures/video/sound GenAI | **Have 2025 only** (no 2023–24 change) | same |
| Eurostat TNLG NACE **C/J/N** | Sector placebos (manufacturing, ICT, admin) | **Have** | `data/eurostat_ai_nace_placebos.csv` |
| Eurostat TNLG NACE **K** | Finance placebo | **Does not exist** (empty API) | — |
| Eurostat E_AI_TANY NACE **M71** | Engineering-consultancy AI | **Does not exist** in `isoc_eb_ain2` (HTTP 400) | — |
| OWID ChatGPT users | Global GenAI diffusion timeline | **404** on catalog/grapher CSVs | `data/owid_fetch_log.csv` |
| IMF AI Preparedness Index | Cross-country snapshot | Datamapper API returned empty JSON | `data/imf_aipi_fetch_log.csv` |
| OECD ICT_BUS AI | Non-EU enterprise AI | SDMX 404 | `data/oecd_ict_fetch_log.csv` |
| World Bank internet / broadband / R&D | Digital context, **not** a GenAI shock | **Have** | `data/wb_IT_NET_*.csv`, `wb_GB_XPD_*.csv` |
| Microsoft AI User Share | 2025–26 cross-country snapshot only | **Have** | `data/ms_ai_diffusion_q1_2026.csv` |
| Microsoft as 2015–24 shock | Overlap with BaTIS | **Cannot** — years do not overlap | — |

## B. Civil industry (not “construction” and not “all professionals”)

| Object | Needed for | Status | File / result |
|---|---|---|---|
| Eurostat NACE **M71 GVA** | Architectural & engineering value added | **Have** (current EUR); UK only to **2018** | `data/eurostat_nama_gva_M71_F_M.csv` |
| Eurostat NACE **M71 employment** | Same industry, people | **Have** | `data/eurostat_nama_emp_M71_F_M.csv` |
| Eurostat NACE F GVA/emp | On-site placebo | **Have** | same |
| Eurostat NACE M GVA/emp | Broader professional placebo | **Have** | same |
| World Bank construction VA `NV.IND.CONS.ZS` | Macro construction | **Invalid indicator** (API 120) | do not invent |
| World Bank GDP, services %, industry % | Macro background only | **Have** | `data/wb_*.json` |
| ILO ISIC F vs M employment | Exporter labour markets | **Have** 17 areas; **China empty** | `data/ilo_emp_FM.csv` |
| ILO ISCO 2142 by country, bilateral | “Engineers in A → engineers in B” | **Not published** (SDMX 404 at 2142/214/21/2) | `09_relocation_probe/ilo_occupation_fetch_log.csv` |
| Eurostat LFS ISCO-08 **two-digit** (`lfsa_egai2d`) | Closest published occupation group (OC21 science and engineering professionals) | **Have** 2015–2024 | `09_relocation_probe/eurostat_lfsa_occ2d.csv`. OC21 Post×ΔTNLG −0.001 (0.004) |
| Eurostat NACE **M71 SBS** turnover, emp, wages, VA, GOS | Firm-level industry economy, **includes 2024** | **Have** 2021–24, 17 members | `data/eurostat_sbs_M71_F_M.csv` |
| Eurostat SBS **M7112** engineering consultancy | Tighter domestic industry than M71 | **Have** 2021–24 employment, output, wages, VA | `09_relocation_probe/eurostat_sbs_M7112_engineering.csv`. Employment 0.000; output −0.008** |
| Inward FATS M71 by controlling country | Mode 3 / commercial presence | **Ends 2020**; India unpublished | `09_relocation_probe/eurostat_fats_M71.csv` |
| Eurostat NACE **M71 D1/P1** | Compensation and output | **Have**; UK D1 only to 2018 | `data/eurostat_nama_D1_P1_M71_F_M.csv` |
| ILO ISIC **M71** employment | Engineering-industry jobs in IND/CHN | **Not published** (SDMX 404) | `ilo_m71_fetch_log.csv` |
| BLS NAICS **54133** | US engineering services | Public API returned **NAICS 54 only** | `bls_engineering_ces.csv` |

**M71 2019–2023 GVA (current EUR), selected:** Belgium M71 +40.8% vs F +33.8%; Spain M71 +47.1% vs F +6.8%; Germany M71 +14.7% vs F +30.5%; Italy M71 +55.0% vs F +68.6%. Nominal values include inflation; they are not a GenAI effect.

**Regression (honest):** log M71 GVA, Post×ΔM = −0.006 (0.005), N=90. SBS log M71 turnover Post-2024×ΔTNLG = −0.007** (0.003), N=68; employment 0.000 (0.002). Construction turnover −0.010***. Domestic M71 is **not** an expansion story where NLG jumped.

## C. Cross-border civil / engineering-related trade

| Object | Needed for | Status | File / result |
|---|---|---|---|
| BaTIS **SJ3** balanced | Finest official engineering-adjacent bilateral service category; potentially digitally deliverable but not mode-identified | **Have** 2015–2024 | `data/batis_civil_related.csv` |
| BaTIS **SJ311 / SJ312** engineering services | True civil trade | **Not in BaTIS** (404) | Eurostat ITS is the source |
| Eurostat ITS **SJ312 / SJ31 / SJ311** (`bop_its6_det`) | Reporter-published engineering / architectural services, 2015–2024 | **Have** IN, CN_X_HK, PH; **VN empty**; UK ITS to **2019** only | `09_relocation_probe/eurostat_its_engineering.csv` (6,338 cells). India SJ312 Post×ΔTNLG 0.026* (0.014), N=96; China SJ312 −0.062** (0.027) |
| Eurostat ITS SJ312 placebo partners (US, UK, CH, JP, extra-EU) | Generic engineering-import boom? | **Have**; all Post×ΔTNLG **null** | `09_relocation_probe/eurostat_its_sj312_placebos.csv` |
| BaTIS **SI** computer | Digital placebo | **Have** | same |
| BaTIS **SJ2** consulting, **SJ1** R&D | Professional placebos, not civil | **Have** | `data/batis_SJ1_SJ2.csv` |
| ONS Pink Book / TIC by India × engineering | UK-official Mode 1 | **Not retrieved** (ONS file URL 404 in this environment) | use BaTIS GBR←IND SJ3; Eurostat UK ITS ends 2019 |
| BaTIS adjustment **N** (reported) vs **B** (balanced) | Robustness to imputation | **Have** in the existing extract. EU←India SJ3 reported **ends 2023** | `03_trade/batis_civil_related.csv`; `09_relocation_probe/tables/uk_corridors_B_vs_N.csv` |
| China SAFE construction vs other business | Direct mode-of-supply comparison | Not pulled; BaTIS SE used as a project-based service comparison only | — |
| RBI/NITI India engineering-export totals | Institutional context | Not in this git snapshot | optional PDF, not used in regressions |

**SJ2/SJ1 placebos:** Post×ΔM on log SJ2 = 0.007 (0.007); SJ1 = 0.003 (0.009); same N=336 as SJ3 null. The trade interaction is not hiding in neighbouring EBOPS headings.

UK←India SJ3 2019→2024: 2,187 → 4,979 USD million (+128%). UK←China SE: +52%.

## D. Chain that the user asked for, mapped to data

| Hypothesis | Data verdict |
|---|---|
| A’s civil engineers fall because of GenAI | UK APS 2121 −14.3%; CAD 3120 −23.9%; technicians 3114 +214.5%. Consistent with **task polarisation**, not identified as caused by GenAI (no occupation-level AI adoption). |
| That fall causes B’s civil-engineer counts to change | **Cannot test.** No bilateral ISCO 2142. |
| That fall causes B’s GDP to change | **Cannot test** with APS 2121 as a shock (reverse causality / joint trends). |
| A’s professional AI adoption is associated with engineering-adjacent imports from B | Generic **TANY**: EU-16 **null**. **TNLG 2023–24** India SJ3 (BaTIS B) **0.021\*\*\*** (0.008). Newly retrieved **Eurostat ITS SJ312** 0.026* (0.014), N=96. Chinese SJ312 **−0.062\*\*** (0.027). Architectural SJ311 null. Pooled SI −0.002; India-only SI −0.009*. |
| Indian SJ3 vs Chinese SE | Level contrast remains (+128% vs +52%). **DiD relocation index** log(IN SJ3)−log(CN SE) **0.029\*\*** (0.013); ITS log(IN SJ312)−log(CN SJ312) **0.101\*\*\*** (0.035). 2022–24 cross-section of the BaTIS index is null; event-study 2019 is significant. Not mode-identified. |
| A’s professional AI raises A’s own M71 industry | GVA to 2023: −0.007*. **SBS 2021–24:** turnover −0.007**, wages −0.009***, VA −0.006***, employment null. F turnover also −0.010***. |

## E. Replication

```bash
cd Study4_FINAL_VERSION
python3 scripts/run_analysis.py
python3 scripts/run_novelty_layer.py
python3 scripts/run_nlg_shock.py
python3 scripts/run_industry_economy.py
python3 Data_Study4_IJCM/07_scripts/download_relocation_series.py
python3 Data_Study4_IJCM/07_scripts/run_relocation_experiments.py
python3 Data_Study4_IJCM/07_scripts/download_corroboration.py
python3 Data_Study4_IJCM/07_scripts/run_corroboration_experiments.py
python3 Data_Study4_IJCM/07_scripts/download_uk_india.py
python3 Data_Study4_IJCM/07_scripts/run_uk_india_experiments.py
python3 Data_Study4_IJCM/07_scripts/download_ai_impact.py
python3 Data_Study4_IJCM/07_scripts/run_ai_impact_experiments.py
```

Relocation probe (reset RQs): `RELOCATION_RESEARCH_DESIGN.md` and `09_relocation_probe/`.
Corroboration (independent re-fetch + M7112 + placebos): `CORROBORATION.md`.
UK–India two-country formulas: `UK_INDIA_MEASUREMENT.md` and `10_uk_india/`.
AI-shock impact redesign: `AI_SHOCK_IMPACT.md` and `11_ai_shock_impact/`.

## F. UK–India two-country re-retrieval (21 September 2026)

| Object | Status | File / result |
|---|---|---|
| BaTIS GBR↔IND and GBR/IND↔W, SJ3/SE/SI/SJ1/SJ2, B and N | **Have** B 2015–24; IND↔GBR N **404**; UK←IN SE N only 5 years | `10_uk_india/batis_uk_india.csv` |
| World Bank GDP / services / industry / R&D / exports | **Have** (context) | `10_uk_india/wb_uk_india.csv` |
| ONS Pink Book API | **Decommissioned** | `10_uk_india/ons_pinkbook_fetch_log.csv` |
| DDI, NSP, TMI, partner share, DiG, stacked 2×2 | **Have**; no interpolation | `10_uk_india/tables/` |
| UK←IN SJ3 2019→2024 | 2,187 → 4,979 (+128%); DDI 0.981 → 0.986; India share 4.2% → 6.9% | formula (1), (5) |
| DiG 2019–24 / 2022–24 / 2019–22 | **+0.21 / −0.95 / +1.15** | formula (7) |
| Stacked 2×2 UK←IN SJ3 vs SE | **0.112 (0.277)**, N=20, n.s. | formula (8) |
| Stacked 2×2 IN←UK SJ3 vs SE | **0.292\*\* (0.148)** | formula (8) |
| APS 2121 / 3120 / 3114 | −12.5% / −21.0% / +197% | formulas (9)–(10) |

Claim: association / corridor mix. Not causal civil relocation.
