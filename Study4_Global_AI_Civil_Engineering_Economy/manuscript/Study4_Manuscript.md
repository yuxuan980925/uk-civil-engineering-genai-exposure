# Generative AI and the Cross-Border Civil Engineering Economy

**Occupation exposure, NACE M71, Mode-1 versus Mode-3 trade, and a 17-country robustness check**

Working paper · 17 September 2026  
This article is **not** a reuse of the IJCM LLM occupation panel. Exposure comes from Eloundou et al. (`occ_level.csv`). UK employment comes from ONS APS (status A). The **preferred AI shock** is Eurostat `E_AI_TNLG` (natural-language generation) in NACE M, 2024 minus 2023. Generic `E_AI_TANY` is the comparison that mixes machine learning with GenAI. M71 accounts and trade come from Eurostat, OECD–WTO BaTIS, ILOSTAT, and the World Bank. Replication: `scripts/run_analysis.py`, `run_novelty_layer.py`, `run_nlg_shock.py`, `build_article_assets.py`.

**Claim boundary.** A fall in UK SOC 2121 does **not** identify a change in another country’s civil-engineer counts or GDP. ILO does not publish bilateral ISCO 2142.

---

## Abstract

Generative AI is uneven *inside* civil engineering. Eloundou β_human is 0.52 for architectural and civil drafters (O\*NET 17-3011), 0.477 for civil engineering technologists (17-3022), and 0.375 for civil engineers (17-2051). In the UK Annual Population Survey, December 2021–September 2025, CAD/drawing technicians (SOC 3120) fell 23.9%, civil engineers (2121) fell 14.3%, and building/civil technicians (3114) rose 214.5%. That is task polarisation, not a single occupation collapse.

OECD–WTO BaTIS balanced UK imports of SJ3 (technical, trade-related and other business services) from India rose from USD 2.19 billion (2019) to 4.98 billion (2024). UK imports of construction services (SE) from China rose 52%. Log UK 2121 employment and log India SJ3 imports move in opposite directions (correlation −0.89, *n* = 4).

Generic Eurostat “any AI” (E_AI_TANY) in NACE M does **not** predict log Mode-1 SJ3 (0.000, s.e. 0.006, *N* = 336). The **generative** item does. EU-27 professional NLG use rose 4.55% (2023) → 11.51% (2024) → 17.74% (2025); construction stayed 0.58 → 2.42 → 3.25. Post-2023 × ΔM TNLG 2023–24 is 0.009 (0.005), *p*=0.108, *N*=357. Restricting post to 2024 gives 0.007**. The India corridor is 0.021***. Domestic **NACE M71 industry accounts that now include 2024** (Eurostat SBS net turnover, wages, value added) move the other way: Post-2024 × ΔTNLG on log M71 turnover is −0.007** (*N*=68); wages −0.009***; employment is a null. Construction turnover is also −0.010***. The civil-engineering *industry* in high-NLG Europe did not expand with the shock; Mode-1 SJ3 from India is the corridor that did.

The novelty is a **civil-specific stack**—Eloundou exposure × **generative NLG versus older AI types** × Eurostat M vs F vs J/C/N × **M71 SBS industry economy (turnover, jobs, wages)** × GATS mode × placebos—not a recycled IJCM score.

**Keywords:** generative AI; civil engineering; NACE M71; Mode 1; BaTIS; Eurostat.

---

## 1. Introduction and novelty

The desktop Study 4 folder and `Data_IJCM/04_external_indices/` already contained Felten AIOE, language-modelling AIOE, and ONS automation. Those files are **used** in this paper as extra instruments (Table 12, Figures 10–11). LLM 1–5 scores appear only as a comparison column, not as the identification sample.

The research question is cross-country and industry-level: when professional establishments in country *A* adopt **generative** NLG, does *A*’s own architectural and engineering industry (NACE M71) change in turnover, jobs, and wages, and do Mode-1 engineering-related imports from country *B* (especially India) rise? APS 2121 is not used as a shock to partner GDP.

Novelty relative to generic AI-labour papers and relative to the IJCM draft:

1. **Within-civil exposure from Eloundou, not from an in-house LLM panel.** Drafters > technicians > licensed civil engineers (Table 1).
2. **UK employment for the full APS civil-adjacent SOC list** (16 unit groups, Table 2), not five LLM labels.
3. **NACE M71** national accounts as the engineering-consultancy industry, distinct from construction (F) and from all of professional services (M).
4. **GATS mode:** India/Philippines/Viet Nam as Mode-1 SJ3; China as Mode-3 SE. BaTIS has no SJ312.
5. **A 17-country robustness check that overturns an eight-country TANY coefficient.**
7. **M71 structural business statistics for 2021–2024** (turnover, employment, wages, value added, GOS), so the industry-economy test includes the 2024 NLG year that national-accounts GVA (ends 2023) cannot.

`DATA_INVENTORY.md` lists series that do not exist (M71 AI survey; SJ311/SJ312; bilateral ISCO 2142; UK M71 after 2018).

---

## 2. Data (this study)

| Layer | Source | File |
|---|---|---|
| Exposure | Eloundou et al., official `occ_level.csv` | `data/eloundou_occ_level.csv` |
| UK employment | ONS APS SOC 2020, status A | `data/from_study1/aps_employment_2021_2025.csv` (ONS extract only) |
| Sectoral AI (generic) | Eurostat `isoc_eb_ain2` E_AI_TANY, NACE F and M | `data/eurostat_ai_raw.csv` |
| **GenAI types (preferred)** | E_AI_TNLG / TML / TTM / TIR / TPVSG, NACE F/M | `data/eurostat_ai_genai_types.csv` |
| Sector placebos | Same indicators, NACE C/J/N (K unpublished) | `data/eurostat_ai_nace_placebos.csv` |
| Engineering industry (accounts) | Eurostat `nama_10_a64` / `_e`, NACE M71, F, M | `data/eurostat_nama_*.csv` |
| Engineering industry (enterprises) | Eurostat SBS `sbs_ovw_act` / `sbs_sc_ovw`, M71 vs F vs M, 2021–24 | `data/eurostat_sbs_M71_F_M.csv` |
| Compensation / output | `nama_10_a64` D1 and P1 | `data/eurostat_nama_D1_P1_M71_F_M.csv` |
| US professional services (too broad) | BLS CES NAICS 54; 54133 not returned | `data/bls_engineering_ces.csv` |
| Trade | OECD–WTO BaTIS, adjustment B, SJ3/SE/SI/SJ1/SJ2 | `data/batis_*.csv` |
| Exporter labour | ILOSTAT ISIC F and M | `data/ilo_emp_FM.csv` |
| Macro background | World Bank WDI | `data/wb_*.json` |
| Diffusion snapshot | Microsoft Q1 2026 (not a 2015–24 shock) | `data/ms_ai_diffusion_q1_2026.csv` |

SOC–O\*NET matches used here: 2121→17-2051; 3114→17-3022; 3120→17-3011. Other APS codes have no clean Eloundou civil match and are left unmatched.

---

## 3. Design

For EU importers *i*, Mode-1 partners *j* ∈ {IND, PHL, VNM}, *t* = 2018…2024:

\[
\log M^{SJ3}_{ijt}=\alpha_i+\delta_t+\gamma_j+\beta(\mathbf{1}[t\ge 2023]\times \Delta M_i)+\varepsilon_{ijt}.
\]

The **preferred** \(\Delta M_i\) is Eurostat NACE M **E_AI_TNLG** in 2024 minus 2023 (the ChatGPT diffusion year in the survey). Generic TANY 2024 minus 2021 remains the comparison. Standard errors clustered by importer (within transformation). Portugal has TNLG in 2024 but missing TANY M 2024, so the TNLG panel is 17 importers (*N*=357) and TANY is 16 (*N*=336). Placebos: TML/TTM/TIR; F/C/J/N TNLG; SI; SJ1/SJ2; SE and SJ3 from China; log M71 GVA; **SBS M71 vs F turnover/employment/wages**.

A second equation is the **domestic industry**:

\[
\log Y^{M71}_{it}=\alpha_i+\delta_t+\beta(\mathbf{1}[t\ge 2024]\times \Delta TNLG_i)+\varepsilon_{it},
\]

with \(Y\) ∈ {net turnover, persons employed, wages, value added, GOS} from SBS, 2021–2024, 17 countries. Construction (F) is the on-site placebo.

---

## 4. Results

### 4.1 UK polarisation (Figure 2, Table 2)

Among 16 APS civil-adjacent unit groups, the largest declines are quality-control/planning engineers (−25.3%), CAD/drawing technicians (−23.9%), chartered surveyors (−21.7%), and civil engineers (−14.3%). The largest increase is building and civil engineering technicians (+214.5%). CAD technicians are the high-Eloundou match (0.52) and contracted more than civil engineers (0.375).

### 4.1b Instruments already in the previous Study 4 / IJCM external folder (Figures 10–11, Table 12)

The desktop Study 4 folder and `Data_IJCM/04_external_indices/` already contained Felten AIOE, language-modelling AIOE, and ONS automation probabilities. Those files are copied into `data/from_legacy_study4/` and used as **additional instruments**, not as a substitute for Eloundou.

They do not all rank occupations the same way. Felten AIOE (2021, pre-ChatGPT applications) scores civil engineers **higher** (1.283) than architectural and civil drafters (0.923) and civil engineering technicians (0.932). Eloundou GPT exposure, ONS automation probability, and the earlier LLM panel rank drafters/CAD **above** licensed civil engineers. UK APS 2021–25 follows the GenAI ranking for CAD versus 2121 (CAD −23.9%, engineers −14.3%), not the 2021 AIOE ranking. Technicians are high on Eloundou and ONS automation but **rose** 214.5%—a reminder that exposure is not incidence.

Felten **industry** scores (AIIE) for NAICS 23 construction are mostly **negative** (highway construction −1.30; other heavy civil −1.10; building exterior contractors −1.76). That matches Eurostat: construction enterprises barely use AI. The civil *professional* story is not the on-site construction story.

The previous LLM panel is reported in Table 12 only as a robustness column (civil engineer 3.0, CAD 4.33). It is not the identification sample.

### 4.2 Trade corridors (Figure 3, Table 4)

UK←India SJ3 +128%; UK←China SE +52%; UK←India SI +113%. Germany←Poland SJ3 +54% (nearshore). US←India SJ3 only +8%. Four-year correlation of UK log 2121 with log India SJ3 = −0.89.

### 4.3 European panel, generic TANY (Figures 4, 7, 8; Tables 5, 6, 10)

Headline EU-16 Post × ΔM TANY = 0.000 (0.006). Event-study year × ΔTANY is already 0.017 (*p*=0.049) in 2018 versus 2022. EU-8 is 0.019***; it does not survive expansion. LOO stays near zero except dropping Sweden (0.010*). Generic “any AI” is the wrong shock for a *generative* question.

### 4.3b Preferred shock: generative NLG (Figures 12–16; Tables 13–15)

EU-27 NACE M NLG: 2.60 (2021), 4.55 (2023), **11.51 (2024)**, 17.74 (2025). Construction NLG: 0.99, 0.58, 2.42, 3.25. ICT (J) NLG is higher still (11.14 → 25.83 in 2023–24). 2024 M TNLG leaders: Denmark 34.06, Finland 30.02, Sweden 29.61, Netherlands 22.01; France 3.90; Romania 3.73.

On 17 EU importers × India/Philippines/Viet Nam:

- Post (≥2023) × ΔM TNLG 2023–24: 0.009 (0.005), *p*=0.108, *N*=357.
- Post = 2024 only × same Δ: 0.007** (0.003).
- India only: 0.021***. Philippines and Viet Nam are not.
- Horse race TNLG vs TML: TNLG 0.015***; TML −0.026*.
- TTM and TIR placebos: 0.004 and −0.010, both null.
- SI, China SE, China SJ3, SJ1, SJ2: all null.
- Construction F TNLG: 0.015 (0.020), null.
- NACE J/C/N TNLG: 0.009**, 0.017**, 0.015**. The Mode-1 association is **not unique to NACE M**.
- Cross-section Δ log India SJ3 2022–24 on ΔTNLG: 0.017***, *N*=17.
- EU-8 TNLG: 0.029*** — still sample-dependent if taken alone.
- log M71 GVA Post × ΔTNLG: −0.007* (GVA only through 2023, so this cannot capture a 2024 output response).

Event study (year × ΔTNLG, omit 2022): 2018 0.007 (0.014); 2019 0.003 (0.012); 2020 0.014 (0.013); 2021 0.009 (0.011); 2023 0.016** (*p*=0.041); 2024 0.015 (*p*=0.072). Pre-trends that failed for TANY are **not** significant for TNLG.

What this does *not* say: UK APS 2121 does not identify Indian GDP. TNLG in M is still a professional-services survey cell, not M71. J/C/N significance means we report a GenAI *country* shock correlated with Mode-1 SJ3, concentrated on India, with construction and computer-services placebos quiet — not a proven M71 outsourcing causal effect.

### 4.4 M71 industry economy (Figures 9, 17–20; Tables 8–9, 16–17)

National-accounts M71 GVA still ends in 2023 for the DiD: Post × ΔTNLG = −0.007* (0.004). Construction GVA −0.008** under TANY.

**New SBS 2021–2024** (current EUR) is the industry-economy test that overlaps the 2024 NLG jump:

| Country pattern (turnover 2021–24) | M71 | F construction |
|---|---|---|
| Romania | +78.9% | +64.9% |
| Greece | +74.7% | +98.6% |
| Portugal | +63.3% | +41.5% |
| Italy | +44.4% | +32.2% |
| Germany | +16.5% | +12.5% |
| Sweden | +1.8% | −0.5% |

Levels rose almost everywhere; that is not a GenAI effect (inflation and recovery). The **DiD** asks whether they rose *faster* where NLG jumped:

- log M71 turnover Post-2024 × ΔTNLG: −0.007** (0.003), *N*=68
- log M71 wages: −0.009***
- log M71 value added: −0.006***
- log M71 employment: −0.000 (0.002) — **jobs did not fall with the NLG jump**
- log F turnover placebo: −0.010***
- log all-professional M turnover: −0.005**
- Cross-section 2023–24 M71 turnover % on ΔTNLG: −0.002 (0.001), *N*=17, not significant
- nama D1 compensation and P1 output through 2023: about −0.009**, and construction is more negative

China Mode-3 SE sums 2019→2024: low-TNLG EU destinations 572→946 USD mn (+65%); high-TNLG destinations 680→1003 (+47%). Mode-3 construction from China did **not** reallocate toward high-NLG importers.

ILO still does not publish ISIC M71 employment (404). BLS public API returned CES NAICS **54** (all professional/technical), not 54133 engineering services; that series is too broad to be a civil outcome.

**Industry takeaway.** In this 17-country window, a larger professional NLG jump is associated with *slower* nominal M71 turnover and wage growth, not a boom, and construction looks similar. Employment in M71 is flat in the DiD. The cross-border movement that lines up with NLG is **India Mode-1 SJ3**, not domestic engineering output and not China Mode-3 SE.

### 4.5 Exporter labour (Figure 5, Table 7)

Philippines M +39.9% vs F +12.8%; Viet Nam M +28.5% vs F −1.4%; India M +13.0% vs F +33.0%. China is missing from ILO F/M.

---

## 5. Case notes

**UK–India.** No post-Brexit Eurostat M AI. The UK facts are APS polarisation plus BaTIS SJ3, not Indian GDP on 2121.

**China.** Mode-3 SE, not Mode-1 SJ3. Microsoft Copilot share undercounts domestic models.

**Germany–Poland.** Nearshore SJ3 can rise when Copilot shares look similar; Eurostat M AI still differs.

---

## 6. Limitations

SJ3 is broader than M71. No SJ312. No M71 AI survey. SBS and nama are current prices (inflation is in the residual). TNLG in J/C/N also predicts SJ3. Construction SBS turnover is also negative in the DiD, so the domestic slowdown is not M71-unique. 17 clusters. ILO M71 and BLS 54133 are unpublished or not returned. APS 2121 is not a partner-GDP shock.

---

## 7. Conclusion

This paper is a **new** Study 4 on official series: generative NLG as the shock, NACE M71 as the civil *industry*, and GATS mode as the cross-border channel. It does not recycle IJCM LLM scores. UK CAD and civil-engineer employment fell while technicians and India SJ3 imports rose. Generic TANY is a null on Mode-1 SJ3. TNLG is associated with **India Mode-1 SJ3**, not with a domestic M71 boom: SBS 2024 turnover and wages grow *slower* where NLG jumped, employment is flat, and construction looks similar. China Mode-3 SE did not shift toward high-NLG importers. APS 2121 is not a shock to partner GDP.

---

## Figure captions

Files in `figures/`.

**Figure 1.** Eurostat enterprise AI use, EU-27, NACE M professional services vs NACE F construction, 2021–2025 (`figure1_eurostat_M_vs_F.png`).

**Figure 2.** UK APS employment change for 16 civil-adjacent SOC 2020 unit groups, Dec 2021–Sep 2025. Bars with Eloundou matches are highlighted (`figure2_uk_aps_bundle.png`).

**Figure 3.** UK BaTIS balanced imports: India SJ3, China SE, India SI (`figure3_uk_trade.png`).

**Figure 4.** Event study, year × importer ΔM AI, omit 2022 (`figure4_event_study.png`).

**Figure 5.** ILO ISIC M vs F employment growth, 2019–2024 (`figure5_ilo_M_vs_F.png`).

**Figure 6.** EU-importer sums: Mode-1 SJ3 vs China SE (`figure6_eu_mode1_vs_china.png`).

**Figure 7.** Cross-section: ΔM AI vs Δ log India SJ3, 2022–24 (`figure7_cross_section.png`).

**Figure 8.** Leave-one-importer-out coefficients (`figure8_loo.png`).

**Figure 9.** NACE M71 vs F GVA, 2019–2023, current EUR (`figure9_m71_vs_F_gva.png`).

**Figure 10.** UK APS employment change versus Eloundou β_human and versus Felten AIOE for matched SOC codes (`figure10_instruments_vs_aps.png`).

**Figure 11.** Felten AIIE for US construction NAICS 23 (`figure11_aiie_construction.png`).

**Figure 12.** EU-27 Eurostat AI *types*: NACE M NLG vs machine learning vs text mining vs construction NLG (`figure12_tnlg_vs_tml.png`).

**Figure 13.** 2024 NLG use, NACE M versus F, by country (`figure13_tnlg_2024_MF.png`).

**Figure 14.** Event study, year × importer ΔM TNLG 2023–24, omit 2022 (`figure14_event_study_tnlg.png`).

**Figure 15.** Cross-section: ΔM TNLG 2023–24 vs Δ log India SJ3, 2022–24 (`figure15_cross_section_tnlg.png`).

**Figure 16.** EU-27 NLG by NACE M, J, C, N, F (`figure16_tnlg_by_nace.png`).

**Figure 17.** SBS net turnover growth 2021–24, NACE M71 vs F (`figure17_sbs_turnover_m71_vs_F.png`).

**Figure 18.** SBS employment growth 2021–24, NACE M71 vs F (`figure18_sbs_emp_m71_vs_F.png`).

**Figure 19.** ΔTNLG 2023–24 vs M71 turnover change 2023–24 (`figure19_tnlg_vs_m71_turnover.png`).

**Figure 20.** M71 net turnover levels, selected members (`figure20_m71_turnover_levels.png`).

**Figure 21.** US CES NAICS 54 only (not 54133) (`figure21_bls_naics54.png`).

---


---

## Article tables (generated from official series)

LLM occupation scores from the IJCM paper are **not** used. Exposure is Eloundou et al. matched to SOC 2020; employment is ONS APS.

### Table 1. Civil occupation exposure (Eloundou occ_level.csv)

| SOC2020 | UK occupation | O*NET | O*NET title | Eloundou β_human | Eloundou β_model |
|---|---|---|---|---|---|
| 2121 | Civil engineers | 17-2051.00 | Civil Engineers | 0.375 | 0.446 |
| 3114 | Building and civil engineering technicians | 17-3022.00 | Civil Engineering Technologists and Technicians | 0.477 | 0.591 |
| 3120 | CAD, drawing and architectural technicians | 17-3011.00 | Architectural and Civil Drafters | 0.520 | 0.540 |

### Table 2. UK APS employment, civil-adjacent SOC 2020 (Dec 2021–Sep 2025)

| SOC2020 | occupation | emp_2021_12 | emp_2025_09 | change_pct | Eloundou β_human |
|---|---|---|---|---|---|
| 2481 | Quality control and planning engineers | 47,000 | 35,100 | -25.3 |  |
| 3120 | CAD, drawing and architectural technicians | 72,900 | 55,500 | -23.9 | 0.520 |
| 2454 | Chartered surveyors | 76,500 | 59,900 | -21.7 |  |
| 2121 | Civil engineers | 115,800 | 99,200 | -14.3 | 0.375 |
| 2453 | Quantity surveyors | 63,000 | 54,200 | -14.0 |  |
| 3581 | Inspectors of standards and regulations | 48,000 | 46,700 | -2.7 |  |
| 2455 | Construction project managers and related professionals | 107,500 | 112,300 | 4.5 |  |
| 2452 | Chartered architectural technologists, planning officers and consultants | 52,000 | 57,100 | 9.8 |  |
| 3541 | Estimators, valuers and assessors | 55,400 | 61,300 | 10.6 |  |
| 3582 | Health and safety managers and officers | 75,400 | 89,300 | 18.4 |  |
| 2127 | Engineering project managers and project engineers | 62,100 | 78,600 | 26.6 |  |
| 2483 | Environmental health professionals | 9,000 | 11,400 | 26.7 |  |
| 2114 | Physical scientists | 26,200 | 34,900 | 33.2 |  |
| 2129 | Engineering professionals n.e.c. | 70,500 | 110,700 | 57.0 |  |
| 2152 | Environment professionals | 45,300 | 80,700 | 78.1 |  |
| 3114 | Building and civil engineering technicians | 5,500 | 17,300 | 214.5 | 0.477 |

### Table 3. Eurostat enterprise AI use, NACE M vs F (%)

| country | iso3 | ai_F_2021 | ai_F_2023 | ai_F_2024 | ai_F_2025 | ai_M_2021 | ai_M_2023 | ai_M_2024 | ai_M_2025 |
|---|---|---|---|---|---|---|---|---|---|
| Austria | AUT | 3.12 | 4.28 | 7.35 | 14.89 | 20.93 | 25.82 | 39.59 | 52.8 |
| Belgium | BEL | 8.3 | 5.17 | 11.08 | 20.25 | 20.24 | 28.28 | 42.92 | 57.11 |
| Czechia | CZE | 0.35 | 1.34 | 2.35 | 7.84 | 9.28 | 9.42 | 22.09 | 33.31 |
| Denmark | DNK | 8.87 | 3.23 | 11.7 | 23.93 | 39.22 | 23.58 | 44.9 | 63.71 |
| Finland | FIN | 9.39 | 5.18 | 11.26 | 24.01 | 29.63 | 31.54 | 48.46 | 74.75 |
| France | FRA | 4.09 | 2.09 | 3.14 | 9.52 | 15.23 | 13.75 | 17.47 | 32.5 |
| Germany | DEU | 8.29 | 4.48 | 10.01 | 14.28 | 25.54 | 26.34 | 42.29 | 48.3 |
| Greece | GRC | 2.82 | 3.4 | 5.17 | 6.96 | 9.2 | 8.67 | 21.02 | 30.81 |
| Hungary | HUN | 0.55 | 1.8 | 4.27 | 4.53 | 3.71 | 5.24 | 17.3 | 22.86 |
| Ireland | IRL | 0.27 | 5.92 | 6.24 | 9.2 | 13.59 | 15.77 | 27.25 | 31.76 |
| Italy | ITA | 5.24 | 2.62 | 5.24 | 10.39 | 8.68 | 9.23 | 19.56 | 35.72 |
| Netherlands | NLD | 7.39 | 4.72 | 8.88 | 21.29 | 20.05 | 24.8 | 39.78 | 54.98 |
| Poland | POL | 0.35 | 1.23 | 2.01 | 2.35 | 6.48 | 9.05 | 14.45 | 22.16 |
| Portugal | PRT | 1.06 | 2.92 | 2.74 | 4.74 | 10.38 | 10.68 | — | 25.68 |
| Romania | ROU | 0.05 | 0.13 | 0.18 | 2.65 | 6.68 | 7.21 | 9.06 | 15.6 |
| Spain | ESP | 3.77 | 4.63 | 4.43 | 11.26 | 13.72 | 16.14 | 26.07 | 38.35 |
| Sweden | SWE | 2.32 | 2.78 | 13.15 | 14.9 | 16.47 | 20.69 | 53.71 | 64.88 |

### Table 4. BaTIS balanced corridors (USD million)

| series | usd_mn_2019 | usd_mn_2024 | pct |
|---|---|---|---|
| UK ← India SJ3 (Mode 1) | 2186.6 | 4979.3 | 127.7 |
| UK ← China SE (Mode 3) | 118.5 | 179.8 | 51.7 |
| UK ← India SI (computer) | 2215.3 | 4723.0 | 113.2 |
| US ← India SJ3 | 2398.0 | 2584.5 | 7.8 |
| Germany ← India SJ3 | 659.6 | 925.9 | 40.4 |
| Germany ← Poland SJ3 (nearshore) | 1516.0 | 2327.7 | 53.5 |
| Australia ← India SJ3 | 167.3 | 250.4 | 49.6 |
| Netherlands ← India SJ3 | 830.9 | 967.2 | 16.4 |
| France ← India SJ3 | 524.0 | 830.1 | 58.4 |

### Table 5. Identification (log SJ3 unless noted)

| Specification | Coefficient (s.e.) | N | Note |
|---|---|---|---|
| (1) Post × M-AI 2024 | 0.002 (0.003) | 336 | EU importers × IND/PHL/VNM; TWFE |
| (2) Post × ΔM 2021–24 [headline] | 0.000 (0.006) | 336 | Preferred: GenAI window is the 2023–24 jump |
| (3) Horse race: Post × ΔM | 0.001 (0.008) | 336 | Same regression as (4) |
| (4) Horse race: Post × ΔF | -0.004 (0.029) | 336 | Construction AI change, controlling for M |
| (5) Placebo SI Mode-1 | -0.002 (0.007) | 336 | Computer services from same partners |
| (6) Placebo SE from China | -0.002 (0.007) | 112 | Mode-3 construction services |
| (7) Placebo SJ3 from China | 0.009 (0.010) | 112 | SJ3 from China |
| (8) Placebo SE from Mode-1 | -0.009 (0.014) | 336 | Construction services from IND/PHL/VNM |
| (9) Post × (M−F) 2024 gap | 0.003 (0.004) | 336 | Professional minus construction AI |
| (10) Time-varying M-AI 2021/23/24 | 0.003 (0.003) | 150 | Eurostat years overlapping BaTIS |
| (11) Placebo time-varying F-AI | -0.010 (0.010) | 153 | Construction AI |
| (12) Drop 2020–21 | 0.002 (0.004) | 240 | Omit COVID years |
| (13) Fake post=2020 × ΔM, sample 2018–21 | -0.000 (0.005) | 192 | Pre-trend placebo |
| (14) IHS(value), Post × ΔM | 0.001 (0.006) | 336 | arcsinh instead of log |
| (15) WLS by 2019 SJ3 value | -0.007 (0.009) | 336 | Larger corridors weighted more |
| (H) India only, Post × ΔM | 0.005 (0.005) | 112 | Partner = IND |
| (H) Philippines only, Post × ΔM | -0.014 (0.014) | 112 | Partner = PHL |
| (H) Viet Nam only, Post × ΔM | 0.010 (0.006) | 112 | Partner = VNM |
| (16) Cross-section Δlog IN SJ3 22–24 on ΔM | 0.007 (0.004) | 16 | No FE; one obs per importer |
| (17) EU-8 only: Post × ΔM 2021–24 | 0.019*** (0.006) | 168 | DEU FRA NLD POL ITA ESP IRL ROU; fragility check |
| (18) EU-8 only: time-varying M-AI | 0.023** (0.010) | 72 | Same 8 importers, 2021/23/24 |

### Table 6. Event study: year × ΔM (omit 2022)

| year | coef | se | p |
|---|---|---|---|
| 2018.0 | 0.017 | 0.009 | 0.049 |
| 2019.0 | 0.011 | 0.01 | 0.275 |
| 2020.0 | 0.017 | 0.011 | 0.106 |
| 2021.0 | 0.011 | 0.012 | 0.333 |
| 2022.0 | 0.0 | 0.0 | 1.0 |
| 2023.0 | 0.011 | 0.004 | 0.005 |
| 2024.0 | 0.013 | 0.005 | 0.016 |

### Table 7. ILO ISIC M vs F employment, 2019–2024 (%)

| country | pct_M | pct_F |
|---|---|---|
| United Arab Emirates | 17.0 | 53.3 |
| Australia | 9.2 | 13.6 |
| Germany | -4.1 | -5.5 |
| Spain | 28.4 | 10.6 |
| France | 22.6 | 5.7 |
| United Kingdom | 21.8 | -7.6 |
| India | 13.0 | 33.0 |
| Ireland | 51.5 | 17.1 |
| Italy | 5.5 | 21.5 |
| Netherlands | 37.8 | 16.8 |
| Philippines | 39.9 | 12.8 |
| Poland | 30.4 | 0.3 |
| Romania | 13.0 | 17.6 |
| Singapore | 8.6 | 5.0 |
| United States | 7.1 | 5.0 |
| Viet Nam | 28.5 | -1.4 |

### Table 8. NACE M71 vs F GVA, 2019–2023 current EUR (%)

| country | iso3 | F | M | M71 |
|---|---|---|---|---|
| Austria | AUT | 23.7 | 21.5 | 16.1 |
| Belgium | BEL | 33.8 | 32.0 | 40.8 |
| Czechia | CZE | 45.5 | 41.0 | 47.1 |
| Denmark | DNK | 15.6 | 21.7 | 34.2 |
| Finland | FIN | -0.3 | 16.7 | 13.0 |
| France | FRA | 15.9 | 13.5 | 14.0 |
| Germany | DEU | 30.5 | 26.1 | 14.7 |
| Greece | GRC | 80.6 | 41.4 | 39.3 |
| Hungary | HUN | 45.2 | 35.7 | 38.5 |
| Ireland | IRL | 43.4 | 74.8 | 70.0 |
| Italy | ITA | 68.6 | 33.9 | 55.0 |
| Netherlands | NLD | 33.8 | 33.7 | 29.2 |
| Poland | POL | 18.4 | 41.6 | 28.9 |
| Portugal | PRT | 41.7 | 51.4 | 63.1 |
| Romania | ROU | 82.7 | 50.6 | 63.5 |
| Spain | ESP | 6.8 | 28.5 | 47.1 |
| Sweden | SWE | 12.2 | 18.9 | — |

### Table 9. M71 GVA and SJ1/SJ2 placebos

| Specification | Coefficient (s.e.) | N |
|---|---|---|
| (M71) log GVA Post × ΔM | -0.006 (0.005) | 90 |
| (F) log GVA Post × ΔM placebo | -0.008** (0.004) | 96 |
| (M71) time-varying M-AI 2021/23 | 0.000 (0.004) | 32 |
| (trade) SJ2 consulting placebo Post × ΔM | 0.007 (0.007) | 336 |
| (trade) SJ1 R&D placebo Post × ΔM | 0.003 (0.009) | 336 |

### Table 10. Leave-one-importer-out, Post × ΔM

| dropped | country | display | n |
|---|---|---|---|
| AUT | Austria | 0.001 (0.006) | 315 |
| BEL | Belgium | 0.000 (0.006) | 315 |
| CZE | Czechia | 0.001 (0.005) | 315 |
| DEU | Germany | 0.001 (0.006) | 315 |
| DNK | Denmark | 0.002 (0.006) | 315 |
| ESP | Spain | 0.001 (0.006) | 315 |
| FIN | Finland | -0.000 (0.005) | 315 |
| FRA | France | -0.002 (0.005) | 315 |
| GRC | Greece | 0.001 (0.006) | 315 |
| HUN | Hungary | 0.000 (0.006) | 315 |
| IRL | Ireland | 0.001 (0.005) | 315 |
| ITA | Italy | 0.000 (0.006) | 315 |
| NLD | Netherlands | -0.001 (0.005) | 315 |
| POL | Poland | 0.001 (0.006) | 315 |
| PRT | Portugal | 0.000 (0.006) | 336 |
| ROU | Romania | -0.002 (0.005) | 315 |
| SWE | Sweden | 0.010* (0.006) | 315 |

### Table 11. Importer AI intensity (Eurostat pp)

| iso3 | ai_M_2024 | ai_F_2024 | ai_M_2021 | ai_F_2021 | dM | dF | gap24 | country |
|---|---|---|---|---|---|---|---|---|
| AUT | 39.59 | 7.35 | 20.93 | 3.12 | 18.66 | 4.23 | 32.24 | Austria |
| BEL | 42.92 | 11.08 | 20.24 | 8.3 | 22.68 | 2.78 | 31.84 | Belgium |
| CZE | 22.09 | 2.35 | 9.28 | 0.35 | 12.81 | 2.0 | 19.74 | Czechia |
| DEU | 42.29 | 10.01 | 25.54 | 8.29 | 16.75 | 1.72 | 32.28 | Germany |
| DNK | 44.9 | 11.7 | 39.22 | 8.87 | 5.68 | 2.83 | 33.2 | Denmark |
| ESP | 26.07 | 4.43 | 13.72 | 3.77 | 12.35 | 0.66 | 21.64 | Spain |
| FIN | 48.46 | 11.26 | 29.63 | 9.39 | 18.83 | 1.87 | 37.2 | Finland |
| FRA | 17.47 | 3.14 | 15.23 | 4.09 | 2.24 | -0.95 | 14.33 | France |
| GRC | 21.02 | 5.17 | 9.2 | 2.82 | 11.82 | 2.35 | 15.85 | Greece |
| HUN | 17.3 | 4.27 | 3.71 | 0.55 | 13.59 | 3.72 | 13.03 | Hungary |
| IRL | 27.25 | 6.24 | 13.59 | 0.27 | 13.66 | 5.97 | 21.01 | Ireland |
| ITA | 19.56 | 5.24 | 8.68 | 5.24 | 10.88 | 0.0 | 14.32 | Italy |
| NLD | 39.78 | 8.88 | 20.05 | 7.39 | 19.73 | 1.49 | 30.9 | Netherlands |
| POL | 14.45 | 2.01 | 6.48 | 0.35 | 7.97 | 1.66 | 12.44 | Poland |
| PRT | — | 2.74 | 10.38 | 1.06 | — | 1.68 | — | Portugal |
| ROU | 9.06 | 0.18 | 6.68 | 0.05 | 2.38 | 0.13 | 8.88 | Romania |
| SWE | 53.71 | 13.15 | 16.47 | 2.32 | 37.24 | 10.83 | 40.56 | Sweden |

### Table 13. Generative NLG shock (log SJ3 unless noted)

| Specification | Coefficient (s.e.) | N | Note |
|---|---|---|---|
| (N1) Post×ΔM TNLG 2023–24 [preferred GenAI shock] | 0.009 (0.005) | 357 | NLG jump is the ChatGPT window; EU × IND/PHL/VNM |
| (N2) Post2024×ΔM TNLG 2023–24 | 0.007** (0.003) | 357 | Treat only 2024 as post (BaTIS ends 2024) |
| (N3) Post×ΔM TNLG 2021–24 | 0.007 (0.005) | 357 | Comparable window to generic TANY ΔM |
| (N4) Post× TNLG M 2024 level | 0.006 (0.004) | 357 | Level not change |
| (N5) Placebo Post×ΔF TNLG 2023–24 | 0.015 (0.020) | 357 | Construction enterprises using NLG |
| (N6) Horse: Post×ΔM TNLG | 0.015*** (0.004) | 357 | Same regression as N7 |
| (N7) Horse: Post×ΔM TML (ML placebo) | -0.026* (0.014) | 357 | Machine learning, not generative NLG |
| (N8) Placebo Post×ΔM TTM 2023–24 | 0.004 (0.008) | 357 | Text mining (also jumped; not NLG) |
| (N9) Placebo Post×ΔM TIR 2023–24 | -0.010 (0.020) | 357 | Image recognition |
| (N10) Comparison Post×ΔM TANY 2021–24 | 0.000 (0.006) | 336 | Generic any-AI; mixes ML and GenAI |
| (N11) Placebo SI Post×ΔM TNLG | -0.002 (0.006) | 357 | Computer services from same partners |
| (N12) Placebo China SE Post×ΔM TNLG | -0.008 (0.009) | 119 | Mode-3 construction from China |
| (N13) Placebo China SJ3 Post×ΔM TNLG | 0.005 (0.010) | 119 | SJ3 from China |
| (N14) Placebo Post×ΔJ TNLG 2023–24 | 0.009** (0.004) | 357 | ICT sector NLG (NACE J), not M71-containing M |
| (N15) Placebo Post×ΔC TNLG 2023–24 | 0.017** (0.008) | 357 | Manufacturing NLG |
| (N16) Placebo Post×ΔN TNLG 2023–24 | 0.015** (0.007) | 357 | Administrative/support NLG |
| (NH) India only Post×ΔM TNLG 2023–24 | 0.021*** (0.008) | 119 | Partner = IND |
| (NH) Philippines only Post×ΔM TNLG 2023–24 | -0.007 (0.015) | 119 | Partner = PHL |
| (NH) Viet Nam only Post×ΔM TNLG 2023–24 | 0.011 (0.008) | 119 | Partner = VNM |
| (N17) EU-8 Post×ΔM TNLG 2023–24 | 0.029*** (0.006) | 168 | Same fragile eight-country sample as TANY EU-8 |
| (N18) Cross-section Δlog IN SJ3 22–24 on ΔTNLG 23–24 | 0.017*** (0.004) | 17 | No FE; one obs per importer |
| (N19) log M71 GVA Post×ΔM TNLG 2023–24 | -0.007* (0.004) | 96 | Domestic architectural & engineering GVA; GVA only to 2023 |
| (N20) SJ2 consulting Post×ΔM TNLG | 0.006 (0.011) | 357 | Same importers/partners as SJ3 |
| (N20) SJ1 R&D Post×ΔM TNLG | 0.007 (0.011) | 357 | Same importers/partners as SJ3 |

### Table 14. Event study: year × ΔM TNLG 2023–24 (omit 2022)

| year | coef | se | p |
|---|---|---|---|
| 2018.0 | 0.007 | 0.014 | 0.606 |
| 2019.0 | 0.003 | 0.012 | 0.779 |
| 2020.0 | 0.014 | 0.013 | 0.294 |
| 2021.0 | 0.009 | 0.011 | 0.409 |
| 2022.0 | 0.0 | 0.0 | 1.0 |
| 2023.0 | 0.016 | 0.008 | 0.041 |
| 2024.0 | 0.015 | 0.008 | 0.072 |

### Table 15. EU-27 Eurostat AI types by NACE (% of enterprises, 10+)

| nace | indic | 2021 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| C | E_AI_TANY | 6.93 | 6.79 | 10.57 | 17.27 |
| C | E_AI_TIR | 2.16 | 2.23 | 2.74 | 3.14 |
| C | E_AI_TML | 1.67 | 1.73 | 2.73 | 3.66 |
| C | E_AI_TNLG | 0.85 | 1.19 | 3.53 | 7.09 |
| C | E_AI_TPVSG | — | — | — | 7.54 |
| C | E_AI_TTM | 1.62 | 1.82 | 4.58 | 9.42 |
| F | E_AI_TIR | 1.17 | 0.82 | 1.49 | 2.27 |
| F | E_AI_TML | 0.68 | 0.43 | 0.83 | 1.62 |
| F | E_AI_TNLG | 0.99 | 0.58 | 2.42 | 3.25 |
| F | E_AI_TPVSG | — | — | — | 4.47 |
| F | E_AI_TTM | 1.43 | 0.98 | 2.81 | 6.09 |
| J | E_AI_TANY | 25.37 | 29.53 | 48.72 | 62.52 |
| J | E_AI_TIR | 8.56 | 9.87 | 13.54 | 15.97 |
| J | E_AI_TML | 15.14 | 16.28 | 25.66 | 28.58 |
| J | E_AI_TNLG | 6.34 | 11.14 | 25.83 | 42.23 |
| J | E_AI_TPVSG | — | — | — | 35.53 |
| J | E_AI_TTM | 11.54 | 14.25 | 30.11 | 42.22 |
| M | E_AI_TIR | 3.98 | 4.18 | 7.35 | 6.81 |
| M | E_AI_TML | 6.46 | 6.82 | 11.35 | 12.46 |
| M | E_AI_TNLG | 2.6 | 4.55 | 11.51 | 17.74 |
| M | E_AI_TPVSG | — | — | — | 18.72 |
| M | E_AI_TTM | 6.13 | 6.92 | 15.61 | 25.22 |
| N | E_AI_TANY | 7.19 | 8.33 | 14.33 | 19.86 |
| N | E_AI_TIR | 1.88 | 1.9 | 2.96 | 4.01 |
| N | E_AI_TML | 1.63 | 2.31 | 3.96 | 4.43 |
| N | E_AI_TNLG | 1.11 | 2.52 | 4.96 | 8.58 |
| N | E_AI_TPVSG | — | — | — | 9.48 |
| N | E_AI_TTM | 2.35 | 3.56 | 8.06 | 12.2 |

### Table 16. M71 industry economy under TNLG (SBS 2021–24 and nama)

| Specification | Coefficient (s.e.) | N | Note |
|---|---|---|---|
| (I1) log M71 turnover Post2024×ΔTNLG | -0.007** (0.003) | 68 | SBS sbs_sc_ovw M71 NETTUR_MEUR; country+year FE |
| (I2) log M71 employment Post2024×ΔTNLG | -0.000 (0.002) | 68 | SBS sbs_ovw_act M71 EMP_NR; country+year FE |
| (I3) log M71 wages Post2024×ΔTNLG | -0.009*** (0.003) | 68 | SBS sbs_ovw_act M71 WAGE_MEUR; country+year FE |
| (I4) log M71 value added Post2024×ΔTNLG | -0.006*** (0.002) | 68 | SBS sbs_ovw_act M71 AV_MEUR; country+year FE |
| (I5) log M71 GOS Post2024×ΔTNLG | -0.003 (0.005) | 68 | SBS sbs_ovw_act M71 GOS_MEUR; country+year FE |
| (I6) log F turnover Post2024×ΔTNLG placebo | -0.010*** (0.003) | 68 | SBS sbs_sc_ovw F NETTUR_MEUR; country+year FE |
| (I7) log F employment Post2024×ΔTNLG placebo | -0.003 (0.002) | 68 | SBS sbs_ovw_act F EMP_NR; country+year FE |
| (I8) log M turnover Post2024×ΔTNLG placebo | -0.005** (0.002) | 68 | SBS sbs_sc_ovw M NETTUR_MEUR; country+year FE |
| (I9) log M71 turnover Post2023×ΔTNLG | -0.009** (0.004) | 68 | SBS sbs_sc_ovw M71 NETTUR_MEUR; country+year FE |
| (I10) Δlog≈ M71 turnover 2023–24 on ΔTNLG | -0.002 (0.001) | 17 | Cross-section; LHS is percent/100 |
| (I11) M71 employment % 2023–24 on ΔTNLG | -0.000 (0.001) | 17 | Cross-section; LHS percent/100 |
| (I12) log M71 compensation Post×ΔTNLG | -0.009** (0.004) | 96 | nama_10_a64 current EUR; series ends 2023 so misses 2024 NLG year |
| (I12) log M71 output Post×ΔTNLG | -0.009*** (0.003) | 96 | nama_10_a64 current EUR; series ends 2023 so misses 2024 NLG year |
| (I12) log F compensation Post×ΔTNLG | -0.011*** (0.004) | 102 | nama_10_a64 current EUR; series ends 2023 so misses 2024 NLG year |
| (I12) log F output Post×ΔTNLG | -0.014*** (0.004) | 102 | nama_10_a64 current EUR; series ends 2023 so misses 2024 NLG year |

### Table 17. SBS growth, NACE M71 vs F, 2021–2024

| country | M71 turnover 21–24 % | F turnover 21–24 % | M71 emp 21–24 % | F emp 21–24 % | ΔTNLG M 23–24 |
|---|---|---|---|---|---|
| Austria | 21.6 | 14.6 | 3.1 | -0.0 | 8.2 |
| Belgium | 26.0 | 30.4 | 7.5 | 4.9 | 11.3 |
| Czechia | 31.6 | 32.1 | 6.8 | 3.4 | 10.3 |
| Germany | 16.5 | 12.5 | 2.0 | -0.5 | 6.3 |
| Denmark | 26.2 | 10.9 | 15.7 | 2.7 | 25.7 |
| Spain | 35.0 | 34.4 | 6.8 | 1.8 | 7.5 |
| Finland | 17.1 | -5.0 | 2.0 | -5.8 | 18.8 |
| France | 15.5 | 12.1 | 12.6 | 3.2 | 2.6 |
| Greece | 74.7 | 98.6 | 13.2 | 25.3 | 5.4 |
| Hungary | 13.0 | 17.1 | -0.9 | -0.7 | 3.4 |
| Ireland | 35.9 | 31.2 | 24.3 | 23.0 | 8.6 |
| Italy | 44.4 | 32.2 | 12.6 | 11.8 | 6.6 |
| Netherlands | 23.5 | 22.6 | 10.9 | 8.7 | 14.3 |
| Poland | 41.4 | 35.0 | 1.0 | -1.5 | 3.6 |
| Portugal | 63.3 | 41.5 | 16.6 | 21.3 | 6.2 |
| Romania | 78.9 | 64.9 | 11.4 | 0.3 | -1.3 |
| Sweden | 1.8 | -0.5 | -2.3 | -9.2 | 21.2 |
