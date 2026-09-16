# Generative AI and the Cross-Border Civil Engineering Economy

**Occupation exposure, NACE M71, Mode-1 versus Mode-3 trade, and a 17-country robustness check**

Working paper · 16 September 2026  
This article is **not** a reuse of the IJCM LLM occupation panel. Exposure comes from Eloundou et al. (`occ_level.csv`). UK employment comes from ONS APS (status A). AI adoption, M71 accounts, and trade come from Eurostat, OECD–WTO BaTIS, ILOSTAT, and the World Bank. Replication: `scripts/run_analysis.py`, `run_novelty_layer.py`, `build_article_assets.py`.

**Claim boundary.** A fall in UK SOC 2121 does **not** identify a change in another country’s civil-engineer counts or GDP. ILO does not publish bilateral ISCO 2142.

---

## Abstract

Generative AI is uneven *inside* civil engineering. Eloundou β_human is 0.52 for architectural and civil drafters (O\*NET 17-3011), 0.477 for civil engineering technologists (17-3022), and 0.375 for civil engineers (17-2051). In the UK Annual Population Survey, December 2021–September 2025, CAD/drawing technicians (SOC 3120) fell 23.9%, civil engineers (2121) fell 14.3%, and building/civil technicians (3114) rose 214.5%. That is task polarisation, not a single occupation collapse.

OECD–WTO BaTIS balanced UK imports of SJ3 (technical, trade-related and other business services) from India rose from USD 2.19 billion (2019) to 4.98 billion (2024). UK imports of construction services (SE) from China rose 52%. Log UK 2121 employment and log India SJ3 imports move in opposite directions (correlation −0.89, *n* = 4).

On 16 EU importers, post-2023 × the 2021–24 *change* in Eurostat NACE M AI does **not** predict log Mode-1 SJ3 imports (0.000, s.e. 0.006, *N* = 336). An eight-country subsample is 0.019 (s.e. 0.006) but fails when the sample expands and when pre-trends are inspected. Domestic NACE M71 GVA (architectural and engineering activities) yields −0.006 (0.005). Placebos (SI, SJ1, SJ2, Chinese SE/SJ3, construction AI) are null.

The novelty is a **civil-specific stack**—Eloundou exposure × Eurostat M vs F adoption × M71 industry × GATS mode × placebos—not a recycled IJCM score.

**Keywords:** generative AI; civil engineering; NACE M71; Mode 1; BaTIS; Eurostat.

---

## 1. Introduction and novelty

The desktop Study 4 folder and `Data_IJCM/04_external_indices/` already contained Felten AIOE, language-modelling AIOE, and ONS automation. Those files are **used** in this paper as extra instruments (Table 12, Figures 10–11). LLM 1–5 scores appear only as a comparison column, not as the identification sample.

The research question is global and civil-specific: when professional establishments in country *A* adopt AI, do Mode-1 engineering-related imports from country *B* rise, and does *A*’s own M71 engineering GVA move? The occupation-to-occupation GDP story is not identified.

Novelty relative to generic AI-labour papers and relative to the IJCM draft:

1. **Within-civil exposure from Eloundou, not from an in-house LLM panel.** Drafters > technicians > licensed civil engineers (Table 1).
2. **UK employment for the full APS civil-adjacent SOC list** (16 unit groups, Table 2), not five LLM labels.
3. **NACE M71** national accounts as the engineering-consultancy industry, distinct from construction (F) and from all of professional services (M).
4. **GATS mode:** India/Philippines/Viet Nam as Mode-1 SJ3; China as Mode-3 SE. BaTIS has no SJ312.
5. **A 17-country robustness check that overturns an eight-country coefficient.**

`DATA_INVENTORY.md` lists series that do not exist (M71 AI survey; SJ311/SJ312; bilateral ISCO 2142; UK M71 after 2018).

---

## 2. Data (this study)

| Layer | Source | File |
|---|---|---|
| Exposure | Eloundou et al., official `occ_level.csv` | `data/eloundou_occ_level.csv` |
| UK employment | ONS APS SOC 2020, status A | `data/from_study1/aps_employment_2021_2025.csv` (ONS extract only) |
| Sectoral AI | Eurostat `isoc_eb_ain2` E_AI_TANY, NACE F and M | `data/eurostat_ai_raw.csv` |
| Engineering industry | Eurostat `nama_10_a64` / `_e`, NACE M71, F, M | `data/eurostat_nama_*.csv` |
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

\(\Delta M_i\) is Eurostat NACE M AI in 2024 minus 2021. Standard errors clustered by importer (within transformation). EU-16 is the headline sample; EU-8 is a fragility check. Placebos: SI, SJ1, SJ2, SE from China, SJ3 from China, F AI, and log M71 / F GVA.

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

### 4.3 European panel (Figures 4, 7, 8; Tables 5, 6, 10)

Headline EU-16 Post × ΔM = 0.000 (0.006). Event-study year × ΔM is already 0.017 (*p*=0.049) in 2018 versus 2022. EU-8 is 0.019***; it does not survive expansion. LOO stays near zero except dropping Sweden (0.010*).

### 4.4 M71 industry (Figure 9, Tables 8–9)

UK M71 GVA ends in 2018. On EU members, Post × ΔM on log M71 GVA is −0.006 (0.005). Construction GVA placebo is −0.008**. SJ2 and SJ1 trade placebos are 0.007 (0.007) and 0.003 (0.009).

### 4.5 Exporter labour (Figure 5, Table 7)

Philippines M +39.9% vs F +12.8%; Viet Nam M +28.5% vs F −1.4%; India M +13.0% vs F +33.0%. China is missing from ILO F/M.

---

## 5. Case notes

**UK–India.** No post-Brexit Eurostat M AI. The UK facts are APS polarisation plus BaTIS SJ3, not Indian GDP on 2121.

**China.** Mode-3 SE, not Mode-1 SJ3. Microsoft Copilot share undercounts domestic models.

**Germany–Poland.** Nearshore SJ3 can rise when Copilot shares look similar; Eurostat M AI still differs.

---

## 6. Limitations

SJ3 is broader than M71. No SJ312. No M71 AI survey. M71 GVA is current prices. Eight clusters in EU-8. Failed pre-trends. APS sampling error. BaTIS ends 2024. No bilateral civil-engineer census.

---

## 7. Conclusion

This paper stands on official series assembled for a *cross-border civil* question. It does not recycle IJCM LLM scores. UK CAD and civil-engineer employment fell while technicians and India SJ3 imports rose. A 16-country test of importer professional AI causing Mode-1 imports or M71 GVA is a **null**; an eight-country significant coefficient is not a result to keep.

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
