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
| ILO ISCO 2142 by country, bilateral | “Engineers in A → engineers in B” | **Not published** | cannot identify |
| Eurostat NACE **M71 SBS** turnover, emp, wages, VA, GOS | Firm-level industry economy, **includes 2024** | **Have** 2021–24, 17 members | `data/eurostat_sbs_M71_F_M.csv` |
| Eurostat NACE **M71 D1/P1** | Compensation and output | **Have**; UK D1 only to 2018 | `data/eurostat_nama_D1_P1_M71_F_M.csv` |
| ILO ISIC **M71** employment | Engineering-industry jobs in IND/CHN | **Not published** (SDMX 404) | `ilo_m71_fetch_log.csv` |
| BLS NAICS **54133** | US engineering services | Public API returned **NAICS 54 only** | `bls_engineering_ces.csv` |

**M71 2019–2023 GVA (current EUR), selected:** Belgium M71 +40.8% vs F +33.8%; Spain M71 +47.1% vs F +6.8%; Germany M71 +14.7% vs F +30.5%; Italy M71 +55.0% vs F +68.6%. Nominal values include inflation; they are not a GenAI effect.

**Regression (honest):** log M71 GVA, Post×ΔM = −0.006 (0.005), N=90. SBS log M71 turnover Post-2024×ΔTNLG = −0.007** (0.003), N=68; employment 0.000 (0.002). Construction turnover −0.010***. Domestic M71 is **not** an expansion story where NLG jumped.

## C. Cross-border civil / engineering-related trade

| Object | Needed for | Status | File / result |
|---|---|---|---|
| BaTIS **SJ3** balanced | Finest official engineering-adjacent bilateral service category; potentially digitally deliverable but not mode-identified | **Have** 2015–2024 | `data/batis_civil_related.csv` |
| BaTIS **SJ311 / SJ312** engineering services | True civil trade | **Not in BaTIS** (404) | SJ3 is the ceiling |
| BaTIS **SE** construction services | China Mode 3 | **Have** | same |
| BaTIS **SI** computer | Digital placebo | **Have** | same |
| BaTIS **SJ2** consulting, **SJ1** R&D | Professional placebos, not civil | **Have** | `data/batis_SJ1_SJ2.csv` |
| ONS Pink Book / TIC by India × engineering | UK-official Mode 1 | **Not retrieved** (ONS file URL 404 in this environment) | use BaTIS GBR←IND SJ3 |
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
| A’s professional AI adoption is associated with engineering-adjacent imports from B | Generic **TANY**: EU-16 **null** 0.000 (0.006). **TNLG 2023–24** (preferred): 0.009 (0.005), p=0.108, N=357; Post-2024 0.007**; India-only 0.021***. Event-study pre-2022 coefficients are insignificant (unlike TANY). ICT/manufacturing/admin TNLG also predict SJ3 — a **national GenAI wave**, not an M71-only shock. SI, China SE/SJ3, SJ1/SJ2, construction TNLG remain null. |
| A’s professional AI raises A’s own M71 industry | GVA to 2023: −0.007*. **SBS 2021–24:** turnover −0.007**, wages −0.009***, VA −0.006***, employment null. F turnover also −0.010***. |
| India Mode 1 vs China Mode 3 | **Have contrast** in levels (+128% vs +52%), not in the DiD. |

## E. Replication

```bash
cd Study4_FINAL_VERSION
python3 scripts/run_analysis.py
python3 scripts/run_novelty_layer.py
python3 scripts/run_nlg_shock.py
python3 scripts/run_industry_economy.py
```
